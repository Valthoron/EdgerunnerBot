import random

import d20
import discord

from discord.ext import commands
from game.character import Character
from game.dice import CriticalType, roll
from game.gsheet import GoogleSheet
from pymongo.collection import Collection
from pymongo.results import UpdateResult


def get_article(noun: str) -> str:
    noun = noun.lower()

    if noun.startswith("the"):
        return ""

    if noun[0] in ["a", "e", "i", "o", "u"]:
        return "an"

    return "a"


def with_article(noun: str) -> str:
    return f"{get_article(noun)} {noun}"


def find_total_maximum(node) -> tuple[int, int]:
    total = 0
    maximum = 0

    if type(node) is d20.expression.BinOp:
        lefttotal, leftmaximum = find_total_maximum(node.left)
        righttotal, rightmaximum = find_total_maximum(node.right)
        total += lefttotal + righttotal
        maximum += leftmaximum + rightmaximum
    elif type(node) is d20.expression.UnOp:
        optotal, opmaximum = find_total_maximum(node.operand)
        total += optotal
        maximum += opmaximum
    elif type(node) is d20.expression.Dice:
        dice: d20.expression.Dice = node
        total += dice.total
        maximum += dice.num * dice.size

    return total, maximum


class Sheet(commands.Cog):
    def __init__(self, bot):
        self._bot = bot
        self._characters: Collection = bot.mdb.characters

    @commands.command(name="import")
    async def import_sheet(self, context: commands.Context, url: str | None):
        if url is None:
            await context.send("Please provide a Google Spreadsheet URL for the character.")
            return

        # Load character from character sheet
        character = GoogleSheet().load_character_from_url(url)

        # Deactivate all existing characters
        await self._characters.update_many(
            {
                "owner": context.author.id
            },
            {
                "$set": {"active": False}
            }
        )

        # Upsert new character
        result: UpdateResult = await self._characters.update_one(
            {
                "owner": context.author.id,
                "cid": character.id
            },
            {
                "$set": {"active": True} | character.to_dict()
            },
            upsert=True
        )

        if result.matched_count == 0:
            response = f"Imported character sheet for {character.name}."
        else:
            response = f"Updated character sheet for {character.name}."

        await context.send(response)

    @commands.command(name="update")
    async def update_character(self, context: commands.Context, *character_name):
        character_dict = {}

        if not character_name:
            # Use the currently active character
            character_dict = await self._characters.find_one(
                {
                    "owner": context.author.id,
                    "active": True
                }
            )

            if character_dict is None:
                await context.send("Could not find currently active character. Please activate one or specify character name.")
                return
        else:
            # Find character by name
            character_dict = await self._characters.find_one(
                {
                    "owner": context.author.id,
                    "name": {"$regex": f"^{character_name}", "$options": "i"}
                }
            )

            if character_dict is None:
                await context.send(f"Could not find character \"{character_name}\".")
                return

        # Load character from character sheet
        key = character_dict["cid"]
        character = GoogleSheet().load_character_from_key(key)

        # Deactivate all existing characters
        await self._characters.update_many(
            {
                "owner": context.author.id
            },
            {
                "$set": {"active": False}
            }
        )

        # Upsert new character
        result: UpdateResult = await self._characters.update_one(
            {
                "owner": context.author.id,
                "cid": character.id
            },
            {
                "$set": {"active": True} | character.to_dict()
            },
            upsert=True
        )

        await context.send(f"Updated character sheet for {character.name}.")

    @commands.command(name="character", aliases=["char", "activate"])
    async def activate_character(self, context: commands.Context, *character_name):
        if not character_name:
            # Respond with currently active character's name
            character_dict = await self._characters.find_one(
                {
                    "owner": context.author.id,
                    "active": True
                }
            )

            if character_dict is None:
                await context.send("Could not find currently active character.")
                return

            character_name = character_dict["name"]
            await context.send(f"Currently active character is {character_name}.")
            return

        character_name = " ".join(character_name)

        # Find and activate character
        character_dict = await self._characters.find_one_and_update(
            {
                "owner": context.author.id,
                "name": {"$regex": f"^{character_name}", "$options": "i"}
            },
            {
                "$set": {"active": True}
            }
        )

        if character_dict is None:
            await context.send(f"Could not find character \"{character_name}\".")
            return

        # Deactivate all other characters
        character_cid = character_dict["cid"]
        await self._characters.update_many(
            {
                "owner": context.author.id,
                "cid": {"$ne": character_cid}
            },
            {
                "$set": {"active": False}
            }
        )

        character_name = character_dict["name"]
        await context.send(f"Activated character {character_name}.")

    @commands.command(name="delete", aliases=["remove"])
    async def delete_character(self, context: commands.Context, *character_name):
        if not character_name:
            await context.send("Please provide the character name to delete.")
            return

        character_name = " ".join(character_name)

        # Find and remove the character
        result = await self._characters.find_one_and_delete(
            {
                "owner": context.author.id,
                "name": {"$regex": f"^{character_name}$", "$options": "i"}
            }
        )

        if result is None:
            await context.send(f"Could not find character \"{character_name}\". Please type the full, exact name of the character to delete.")
            return

        character_name = result["name"]
        await context.send(f"Deleted character {character_name}.")

    @ commands.command(name="check", aliases=["ch", "skill", "sk"])
    async def skill_check(self, context: commands.Context, *skill_name):
        # Load currently active character
        character_dict = await self._characters.find_one(
            {
                "owner": context.author.id,
                "active": True
            }
        )

        if character_dict is None:
            await context.send("Could not find currently active character.")
            return

        if not skill_name:
            await context.send("Please specify skill name to perform a check.")
            return

        character = Character.from_dict(character_dict)

        # Find skill
        skill_name = " ".join(skill_name)
        skill_list = character.find_skill(skill_name)

        if len(skill_list) == 0:
            await context.send(f"No skill found for \"{skill_name}\".")
            return
        elif len(skill_list) > 1:
            response = f"Found multiple matching skills for \"{skill_name}\":\n"

            for skill in skill_list:
                response += f"\u2022 {skill.name}\n"

            response += "Please use a more specific name."
            await context.send(response)
            return

        skill = skill_list[0]

        # Perform skill check
        roll_result = roll(skill.base)

        # Prepare response embed
        embed = discord.Embed()
        embed.title = f"{character.handle} makes {with_article(skill.name)} check!"
        embed.description = str(roll_result)
        embed.color = 0x00c000

        if character.portrait:
            embed.set_thumbnail(url=character.portrait)

        # Critical roll callout
        if roll_result.critical_type is CriticalType.SUCCESS:
            embed.description += "\n\n:boom: *Critical success!*"
        elif roll_result.critical_type is CriticalType.FAILURE:
            embed.description += "\n\n:thumbsdown: *Critical failure!*"

        # Send response
        await context.send(embed=embed)
        await context.message.delete()

    @ commands.command(name="attack", aliases=["a"])
    async def attack(self, context: commands.Context, *attack_name):
        # Load currently active character
        character_dict = await self._characters.find_one(
            {
                "owner": context.author.id,
                "active": True
            }
        )

        if character_dict is None:
            await context.send("Could not find currently active character.")
            return

        if not attack_name:
            await context.send("Please specify attack name to make an attack.")
            return

        character = Character.from_dict(character_dict)

        # Find attack
        attack_name = " ".join(attack_name)
        attack_list = character.find_attack(attack_name)

        if len(attack_list) == 0:
            await context.send(f"No attack found for \"{attack_name}\".")
            return
        elif len(attack_list) > 1:
            response = f"Found multiple matching attacks for \"{attack_name}\":\n"

            for attack in attack_list:
                response += f"\u2022 {attack.name}\n"

            response += "Please use a more specific name."
            await context.send(response)
            return

        attack = attack_list[0]

        # Perform attack and damage roll
        attack_roll_result = roll(attack.total)
        damage_roll_result = d20.roll(attack.damage)

        # Prepare response embed
        embed = discord.Embed()
        embed.title = f"{character.handle} makes {with_article(attack.name)} attack!"
        embed.description = "**Attack:** " + str(attack_roll_result)
        embed.description += "\n**Damage:** " + str(damage_roll_result)
        embed.color = 0xc00000

        if character.portrait:
            embed.set_thumbnail(url=character.portrait)

        # Critical roll callout
        if attack_roll_result.critical_type is CriticalType.SUCCESS:
            embed.description += "\n\n:boom: *Critical success!*"
        elif attack_roll_result.critical_type is CriticalType.FAILURE:
            embed.description += "\n\n:thumbsdown: *Critical failure!*"

        # Nice damage callout
        damage_total, damage_maximum = find_total_maximum(damage_roll_result.expr.roll)
        if damage_total >= (0.8 * damage_maximum):
            if attack_roll_result.critical_type is CriticalType.SUCCESS:
                callout = random.choice(["BOOM SHAKALAKA", "IT'S ON FIRE", "SUCK ON THAT", "BITCHIN'", "SUPERCALIFRAGILISTICEXPIALIDOCIOUS"])
                embed.description += f"\n\n:fire: *{callout}!*"
            elif attack_roll_result.critical_type is CriticalType.FAILURE:
                embed.description += "\n\n:eyes: *Nice damage, though...*"
            else:
                embed.description += "\n\n:gun: *Nice damage!*"

        # Send response
        await context.send(embed=embed)
        await context.message.delete()


async def setup(bot):
    await bot.add_cog(Sheet(bot))
