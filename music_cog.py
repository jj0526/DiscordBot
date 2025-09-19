import discord
from discord.ext import commands
from discord import Embed
from azapi import AZlyrics
import yt_dlp
import asyncio

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = {}
        self.is_paused = {}
        self.currently_playing = {}
        self.is_bot_connected = {}

        self.music_queue = {}
        self.YDL_OPTIONS = {'format': 'm4a/bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'm4a',}]}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None
    def search_yt(self, item):
        with yt_dlp.YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                if "youtube.com" in item:
                    info = ydl.extract_info(item, download=False)
                else:
                    info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception: 
                return False

        return {'source': info['formats'][3]['url'], 'title': info['title']}
    
    async def play_next(self, ctx):
        guild_id = ctx.guild.id

        if len(self.music_queue[guild_id]) > 0:
            self.is_playing[guild_id] = True
            song_data = self.music_queue[guild_id].pop(0)
            self.currently_playing[guild_id].pop(0)
            m_url = song_data[0]['source']

            def after_play(error):
                self.bot.loop.create_task(self.play_next(ctx))

            self.vc_dict[guild_id].play(
                discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS),
                after=after_play
            )
        else:
            self.is_playing[guild_id] = False
            self.currently_playing[guild_id] = []
            self.bot.loop.create_task(self.disconnect_after_timeout(ctx))
    
    async def play_music(self, ctx):
        guild_id = ctx.guild.id

        if len(self.music_queue[guild_id]) == 0:
            self.is_playing[guild_id] = False
            self.currently_playing[guild_id] = []
            self.bot.loop.create_task(self.disconnect_after_timeout(ctx))
            return

        self.is_playing[guild_id] = True
        song_data = self.music_queue[guild_id][0]
        m_url = song_data[0]['source']
        voice_channel = song_data[1]

        if not hasattr(self, 'vc_dict'):
            self.vc_dict = {}

        if guild_id not in self.vc_dict or not self.vc_dict[guild_id].is_connected():
            self.vc_dict[guild_id] = await voice_channel.connect()
            if not self.vc_dict[guild_id]:
                await ctx.send("Could not connect to the voice channel")
                return
        else:
            await self.vc_dict[guild_id].move_to(voice_channel)

        def after_play(error):
            self.bot.loop.create_task(self.play_next(ctx))

        self.vc_dict[guild_id].play(
            discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS),
            after=after_play
        )
    
async def disconnect_after_timeout(self, ctx, timeout=600):  # 600초 = 10분
    await asyncio.sleep(timeout)
    if not self.is_playing[ctx.guild.id] and not self.is_paused[ctx.guild.id]:
        if self.vc and self.vc.is_connected():
            await ctx.send("10분 동안 노래가 없어 자동으로 퇴장합니다.")
            await self.vc.disconnect()
            self.music_queue[ctx.guild.id] = []
            self.currently_playing[ctx.guild.id] = []
    
    
    @commands.command(name="play", aliases=['p', 'play', 'playing'], help="Play the selected song from youtube")
    async def play(self, ctx, *args):
        if ctx.guild.id in self.music_queue:
            pass
        else:
            self.music_queue[ctx.guild.id] = []
            self.is_playing[ctx.guild.id] = False
            self.is_paused[ctx.guild.id] = False
            self.currently_playing[ctx.guild.id] = []
        query = " ".join(args)

        voice_channel = ctx.message.author.voice.channel if ctx.message.author.voice else None
        if voice_channel is None:
            await ctx.send("Connect to a voice channel!")
        elif self.is_paused[ctx.guild.id]:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song. Incorrect format, try a different keyword")
            else:
                await ctx.send("Song added to the queue")
                em = Embed(title=None, description=f":musical_note: **{song['title']}** added to the queue")
                em.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar)
                await ctx.send(embed=em)
                self.currently_playing[ctx.guild.id].append([query, song['title']])
                self.music_queue[ctx.guild.id].append([song, voice_channel])
                if self.is_playing[ctx.guild.id] == False:
                    await self.play_music(ctx)
    
    
    
    @commands.command(name="pause", help="Pauses the current song being played")
    async def pause(self, ctx, *args):
        if self.is_playing[ctx.guild.id]:
            self.is_playing[ctx.guild.id] = False
            self.is_paused[ctx.guild.id] = True
            self.vc.pause()
        elif self.is_paused[ctx.guild.id]:
            self.vc.resume()
            
    @commands.command(name="resume", aliases=["r"], help="Resumes playing the current song")
    async def resume(self, ctx, *args):
        if self.is_paused[ctx.guild.id]:
            self.is_playing[ctx.guild.id] = True
            self.is_paused[ctx.guild.id] = False
            self.vc.resume()

    @commands.command(name="skip", aliases=["s"], help="Skips the current song being played")
    async def skip(self, ctx):
        if self.vc and self.vc.is_playing():
            #self.currently_playing[ctx.guild.id] = []
            #self.currently_playing[ctx.guild.id].pop(0)
            self.vc.stop()
            await ctx.send("Skipping current song")
        else:
            await ctx.send("No song is currently playing.")

        # Try to play the next song in the queue if it exists
        await self.play_music(ctx)
    
    @commands.command(name="queue", aliases=["q"], help="Displays all the songs currently in the queue")
    async def queue(self, ctx):
        if ctx.guild.id not in self.music_queue or not self.music_queue[ctx.guild.id]:
            if not self.currently_playing.get(ctx.guild.id):
                await ctx.send("No music in the queue.")
                return
            else:
                currently_playing = self.currently_playing[ctx.guild.id][0][1]
                em = Embed(title=f"**Music Queue | {ctx.guild.name}**", description=f"**Now Playing:** {currently_playing}")
                if ctx.guild.icon:
                    em.set_thumbnail(url=ctx.guild.icon.url)
                em.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
                await ctx.send(embed=em)
        else:
            retval = ""
            for i, song in enumerate(self.music_queue[ctx.guild.id], start=1):
                retval += f"**{i}.** {song[0]['title']}\n"

            currently_playing = self.currently_playing[ctx.guild.id][0][1] if self.currently_playing.get(ctx.guild.id) else "None"
            em = Embed(title=f"**Music Queue | {ctx.guild.name}**", description=f"**Now Playing:** {currently_playing}\n{retval}")
            if ctx.guild.icon:
                em.set_thumbnail(url=ctx.guild.icon.url)
            em.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
            await ctx.send(embed=em)
    

    
    async def clearSongs(self, ctx):
        if self.vc != None and self.is_playing[ctx.guild.id]:
            self.vc.stop()
            self.is_playing[ctx.guild.id] = False
            self.is_paused[ctx.guild.id] = False #added
        self.music_queue[ctx.guild.id] = [] #pop all
        self.currently_playing[ctx.guild.id] = []
        await ctx.send("Music queue cleared")
    
    @commands.command(name="clear", aliases=["c", "bin"], help="Stops the current song and clears the queue")
    async def clear(self, ctx):
        await self.clearSongs(ctx)
        
    
    @commands.command(name="leave", aliases=["disconnect", "l", "d", "dc"], help="Kick the bot from the voice channel")
    async def leave(self, ctx):
        self.is_playing[ctx.guild.id] = False
        self.is_paused[ctx.guild.id] = False
        await self.clearSongs(ctx)
        await self.vc.disconnect()
    
    @commands.command(name="lyric", help="Displays the lyrics of the currently playing song")
    async def lyric(self, ctx):
        """Displays lyrics of currently played song, use /lyrics [song title and/or artist name] if the bot can't find the lyrics

        Parameters
        ----------
        interaction: Interaction
            The interaction object
        """
        api = AZlyrics("google")
        if self.currently_playing[ctx.guild.id] == []:
            await ctx.send("No music is playing right now")
        else:
            for elem in self.currently_playing[ctx.guild.id][0]:
                api.title = elem
                Lyrics = api.getLyrics()
                if type(Lyrics) == str:
                    em = Embed(title=f"{api.title} by {api.artist}", description=Lyrics)
                    em.set_footer(text = ctx.author.name, icon_url = ctx.author.display_avatar)
                    em.set_thumbnail(url=ctx.guild.icon)
                    await ctx.send(embed=em)
                    break
            if type(Lyrics) == int:
                await ctx.send("Could not find lyrics, try /lyrics song")

    @discord.slash_command(name='lyrics', description='find lyrics')
    async def lyrics(self, interaction: discord.Interaction, song_query:str):
        """Displays lyrics

        Parameters
        ----------
        interaction: Interaction
            The interaction object
        song_query: str
            song title with or without the song artist
        """
        await interaction.response.defer()
        api = AZlyrics("google")
        api.title = song_query
        Lyrics = api.getLyrics()
        em = Embed(title=f"{api.title} by {api.artist}", description=Lyrics)
        em.set_footer(text = interaction.user.name, icon_url = interaction.user.display_avatar)
        await interaction.edit_original_message(embed=em)

async def setup(bot):
    await bot.add_cog(music_cog(bot))

