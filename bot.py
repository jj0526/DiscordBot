import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="?", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

@bot.command(name="roll_dice", help="Simulates rolling dice.")
async def roll(ctx, number_of_sides: int, member : discord.Member = None):
    if member is None:
        member = ctx.author
    diceNum = str(random.choice(range(1, number_of_sides + 1)))
    await ctx.send(f"{ctx.author.mention} rolled "+ diceNum + "!")

