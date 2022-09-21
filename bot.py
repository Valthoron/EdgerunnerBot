import asyncio
import os

import discord

from discord.ext import commands
from discord.ext.commands import CommandNotFound
from dotenv import load_dotenv

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

COGS = ["cogs.dice"]


class Chummer(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)


intents = discord.Intents(messages=True, message_content=True)
bot = Chummer(command_prefix="!", intents=intents, activity=discord.Game(name="Cyberpunk RED"))


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return

    raise error


async def load_extensions():
    for cog in COGS:
        await bot.load_extension(cog)

asyncio.run(load_extensions())

bot.run(DISCORD_BOT_TOKEN)
