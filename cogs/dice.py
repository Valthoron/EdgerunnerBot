import d20

from discord.ext import commands

from game.dice import CriticalType, roll


class VerboseMDStringifier(d20.MarkdownStringifier):
    def _str_expression(self, node):
        return f"**{node.comment or 'Result'}**: {self._stringify(node.roll)}\n**Total**: {int(node.total)}"


class PersistentRollContext(d20.RollContext):
    def __init__(self, max_rolls=1000, max_total_rolls=None):
        super().__init__(max_rolls)
        self.max_total_rolls = max_total_rolls or max_rolls
        self.total_rolls = 0

    def count_roll(self, n=1):
        super().count_roll(n)
        self.total_rolls += 1
        if self.total_rolls > self.max_total_rolls:
            raise d20.TooManyRolls("Too many dice rolled.")


class Dice(commands.Cog):
    def __init__(self, bot):
        self._bot: commands.Bot = bot

    @commands.command(name="croll")
    async def croll(self, context: commands.Context, bonus: int | None = None, *label):
        response = f"{context.author.mention} :game_die:"

        if bonus is None:
            await context.send("Please specify bonus to make a roll.")
            return

        if not label:
            label_text = "Dice"
        else:
            label_text = " ".join(label)

        roll_result = roll(bonus)

        response = f"{context.author.mention} :game_die:\n"
        response += f"**{label_text}**: {roll_result.dice_string()}\n"
        response += f"**Total**: {roll_result.total}\n"

        if roll_result.critical_type is CriticalType.SUCCESS:
            response += ":boom: *Critical success!*"
        elif roll_result.critical_type is CriticalType.FAILURE:
            response += ":thumbsdown: *Critical failure!*"

        await context.send(response)

    @commands.command(name="roll", aliases=["r"])
    async def roll_cmd(self, context: commands.Context, *, dice: str = "1d20"):
        roll_result = d20.roll(dice, allow_comments=True, stringifier=VerboseMDStringifier())

        response = f"{context.author.mention}  :game_die:\n{str(roll_result)}"

        await context.send(response)

    @commands.command(name="multiroll", aliases=["rr"])
    async def rr(self, ctx, iterations: int, *, dice):
        await self._roll_many(ctx, iterations, dice)

    @staticmethod
    async def _roll_many(ctx, iterations, roll_str):
        if iterations < 1 or iterations > 100:
            return await ctx.send("Too many or too few iterations.")

        results = []
        ast = d20.parse(roll_str, allow_comments=True)
        roller = d20.Roller(context=PersistentRollContext())

        for _ in range(iterations):
            res = roller.roll(ast)
            results.append(res)

        header = f"Rolling {iterations} iterations..."
        footer = f"{sum(o.total for o in results)} total."

        if ast.comment:
            header = f"{ast.comment}: {header}"

        result_strs = "\n".join(str(o) for o in results)

        out = f"{header}\n{result_strs}\n{footer}"

        if len(out) > 1500:
            one_result = str(results[0])
            out = f"{header}\n{one_result}\n[{len(results) - 1} results omitted for output size.]\n{footer}"

        await ctx.send(f"{ctx.author.mention}\n{out}")

    async def cog_before_invoke(self, context: commands.Context):
        await context.message.delete()


async def setup(bot):
    await bot.add_cog(Dice(bot))
