import asyncio
import os

import discord
import motor.motor_asyncio

from discord.ext import commands
from discord.ext.commands import CommandNotFound
from dotenv import load_dotenv
from pymongo.database import Database

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
MONGO_USER = os.getenv("MONGO_BOT_USER")
MONGO_PASSWORD = os.getenv("MONGO_BOT_PASSWORD")

COGS = ["cogs.dice", "cogs.sheet"]


class Chummer(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.mclient = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@localhost:58027/edgerunner")
        self.mdb: Database = self.mclient["edgerunner"]


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
