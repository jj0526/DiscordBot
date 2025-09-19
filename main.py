import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="?", intents=intents)
bot.remove_command('help')

async def main():
    await bot.load_extension("music_cog")
    await bot.load_extension("roll_dice")
    await bot.load_extension("help_cog")
    await bot.load_extension("quality_cog")
    await bot.start(os.getenv('DISCORD_TOKEN'))

asyncio.run(main())
