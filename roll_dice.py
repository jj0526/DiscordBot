import nextcord
from nextcord.ext import commands
import random

class roll_dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="roll_dice", aliases=["주사위", "주사위 던지기", "dice"], help="Simulates rolling dice.")
    async def roll_dice(self, ctx, number_of_sides: int, member: nextcord.Member = None):
        if member is None:
            member = ctx.author
        diceNum = str(random.choice(range(1, number_of_sides + 1)))
        await ctx.send(f"{member.mention} rolled {diceNum}!")

'''
def setup(bot):
    bot.add_cog(roll_dice(bot))
'''