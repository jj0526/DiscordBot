import nextcord
from nextcord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

# Import the roll_dice cog
from roll_dice import roll_dice

# Import the music_cog
from music_cog import music_cog
from help_cog import help_cog

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="?", intents=intents)


#bot.load_extension("music_cog")
#bot.load_extension("roll_dice")
#bot.load_extension("help_cog")



@bot.event
async def on_ready():
    #await bot.load_extension("music_cog")
    #await bot.load_extension("roll_dice")
    #await bot.load_extension("help_cog")
    bot.add_cog(music_cog(bot))
    bot.add_cog(roll_dice(bot))
    bot.add_cog(help_cog(bot))
    print(f"{bot.user.name} has connected to Discord!")



bot.remove_command('help')
# Remove the default help command so that we can write our own


# Register the roll_dice cog with the bot
#bot.add_cog(roll_dice(bot))

# Create an instance of the music_cog
#bot.load_extension("music_cog")
#bot.load_extension("roll_dice")
#bot.load_extension("help_cog")


# Register the music_cog instance with the bot
#bot.add_cog(music_cog_instance)

# Start the bot with our token
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
bot.run(TOKEN)
