import random

from discord.ext import commands


class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["c"])
    async def croll(self, context: commands.Context, bonus: int | None = None, *label):
        response = f"{context.author.mention} :game_die:"

        if bonus is None:
            bonus = 0

        if not label:
            label_text = "Dice"
        else:
            label_text = " ".join(label)

        roll = random.choice(range(1, 11))
        total = roll + bonus
        crit_text = ""
        flavor_text = None

        if roll == 10:
            crit_roll = random.choice(range(1, 11))
            total += crit_roll
            crit_text = f" + 1d10 ({crit_roll})"
            flavor_text = ":boom: *Critical Success!*"
        elif roll == 1:
            crit_roll = random.choice(range(1, 11))
            total -= crit_roll
            crit_text = f" - 1d10 ({crit_roll})"
            flavor_text = ":thumbsdown: *Critical Failure!*"

        response = f"{context.author.mention} :game_die:\n"
        response += f"**{label_text}**: 1d10 ({roll}) + {bonus}{crit_text}\n"
        response += f"**Total**: {total}\n"

        if flavor_text is not None:
            response += flavor_text

        await context.send(response)

    async def cog_before_invoke(self, context: commands.Context):
        await context.message.delete()


async def setup(bot):
    await bot.add_cog(Dice(bot))
