import random

from game.dice import roll, CriticalType

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

        roll_result = roll(bonus)

        response = f"{context.author.mention} :game_die:\n"
        response += f"**{label_text}**: {roll_result.dice_string()}\n"
        response += f"**Total**: {roll_result.total}\n"

        if roll_result.critical_type is CriticalType.SUCCESS:
            response += ":boom: *Critical Success!*"
        elif roll_result.critical_type is CriticalType.FAILURE:
            response += ":thumbsdown: *Critical Failure!*"

        await context.send(response)

    async def cog_before_invoke(self, context: commands.Context):
        await context.message.delete()


async def setup(bot):
    await bot.add_cog(Dice(bot))
