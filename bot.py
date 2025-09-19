# bot.py
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


@bot.command(name="uwu", help="Gives you an random uwu emoji")
async def uwu_print(ctx):
    uwu_list = [
        "(◡ w ◡)",
        "(。U⁄ ⁄ω⁄ ⁄ U。)",
        "(„ᵕᴗᵕ„)",
        "(◡ ω ◡)",
        "( ͡U ω ͡U )",
        " ( ｡ᵘ ᵕ ᵘ ｡)",
        "(ᵘﻌᵘ)",
        "(灬´ᴗ`灬)",
    ]

    response = random.choice(uwu_list)
    await ctx.send(response)


@bot.command(name="roll_dice", help="Simulates rolling dice.")
async def roll(ctx, number_of_sides: int, member : discord.Member = None):
    if member is None:
        member = ctx.author
    diceNum = str(random.choice(range(1, number_of_sides + 1)))
    await ctx.send(f"{ctx.author.mention} rolled "+ diceNum + "!")


@bot.command(name="create-channel")
@commands.has_role("Uncle Bob")
async def create_channel(ctx, channel_name="real-python"):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f"Creating a new channel: {channel_name}")
        await guild.create_text_channel(channel_name)

bot.run(TOKEN)