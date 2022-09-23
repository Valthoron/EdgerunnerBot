from discord.ext import commands
from game.gsheet import GoogleSheet


class Sheet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="import")
    async def import_sheet(self, context: commands.Context, url: str | None):
        if url is None:
            url = "https://docs.google.com/spreadsheets/d/12txYDE-BdNE7An8sRXCtzd0GxaByiiX5uImOJZsVXgY/"

        char = GoogleSheet().load_character(url)

        response = f"{char.name}"
        await context.send(response)


async def setup(bot):
    await bot.add_cog(Sheet(bot))
