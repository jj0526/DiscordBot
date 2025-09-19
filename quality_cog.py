from discord.ext import commands
import discord
import random

class quality_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="quality", aliases=["품질", "품질작", "tap_quality"], help="tap your quality.")
    async def tapQuality(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        random_num = random.randint(0, 100000) #0.000 to 100.000%
        quality_num = 0
        if (random_num<=760):
            quality_num = random_num//76
            quality_num = 100 - quality_num
        elif(random_num<=1760):
            quality_num = (random_num-760)//100
            quality_num = 100 - quality_num - 10
        elif(random_num<=3020):
            quality_num = (random_num-1760)//126
            quality_num = 100 - quality_num - 20
        elif(random_num<=5540):
            quality_num = (random_num-3020)//252
            quality_num = 100 - quality_num - 30
        elif(random_num<=11840):
            quality_num = (random_num-5540)//630
            quality_num = 100 - quality_num - 40
        elif(random_num<=21910):
            quality_num = (random_num-11840)//1007
            quality_num = 100 - quality_num - 50
        elif(random_num<=35770):
            quality_num = (random_num-21910)//1386
            quality_num = 100 - quality_num - 60
        elif(random_num<=53400):
            quality_num = (random_num-35770)//1763
            quality_num = 100 - quality_num - 70
        elif(random_num<=74810):
            quality_num = (random_num-53400)//2141
            quality_num = 100 - quality_num - 80
        else:
            quality_num = (random_num-74810)//2290
            quality_num = 100 - quality_num - 90
        
        await ctx.send(f"{member.mention} got {quality_num} on their weapon!")

'''
def setup(bot):
    bot.add_cog(tapQuality(bot))
'''