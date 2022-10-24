import discord
import game.dice

from discord.ext import commands
from game.character import Character
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
        character = GoogleSheet().load_character(url)

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
            await context.send(f"Could not find character \"{character_name}\". Please type in the full, exact name of the character to delete.")
            return

        character_name = result["name"]
        await context.send(f"Deleted character {character_name}.")

    @ commands.command(name="check")
    async def skill_check(self, context: commands.Context, *skill_name):
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

        roll_result = game.dice.roll(skill.base)

        embed = discord.Embed()
        embed.title = f"{character.handle} makes {with_article(skill.name)} check!"
        embed.description = str(roll_result)
        embed.color = 0x00ff00

        if character.portrait:
            embed.set_thumbnail(url=character.portrait)

        await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Sheet(bot))