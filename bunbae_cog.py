import nextcord
from nextcord.ext import commands
import random

class bunbae_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="bunbae", aliases=["분배", "분배금"], help="Simulates rolling dice.")
    async def roll_dice(self, ctx, num_of_people: int, price: int, member: nextcord.Member = None):
        if member is None:
            member = ctx.author
        
        
        # y = x+0.95(p-1)x+50*n
        
        # 본인 : x-50
        # 다른이 : x*0.95
        await ctx.send(f"{member.mention} rolled {}!")

'''
def setup(bot):
    bot.add_cog(roll_dice(bot))
'''