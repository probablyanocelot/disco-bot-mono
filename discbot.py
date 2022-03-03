import os
import sys
import discord
import pafy
import asyncio
import ctypes
import ctypes.util
from asgiref.sync import async_to_sync
from discord.ext import commands
from config import FFMPEG_OPTIONS, TOKEN
from ctnrs import song_dict, counter
from search_yt import yt_query, YT_API_KEY, get_vid_name
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


# BOT
intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='--')
# discord.opus.load_opus('libopus-0.0.17.dll')  # 'libopus-0.0.17.dll'
'''
If you are getting this Python error (excerpt) with discord.py:
 
raise OpusNotLoaded()
discord.opus.OpusNotLoaded
 
Solve it by adding this in your script:
'''

# print("ctypes - Find opus:")
# a = ctypes.util.find_library('opus')
# print(a)

# print("Discord - Load Opus:")
# b = discord.opus.load_opus(a)
# print(b)

# print("Discord - Is loaded:")
# c = discord.opus.is_loaded()
# print(c)


# if not discord.opus.is_loaded():
#     #     # the 'opus' library here is opus.dll on windows
#     #     # or libopus.so on linux in the current directory
#     #     # you should replace this with the location the
#     #     # opus library is located in and with the proper filename.
#     #     # note that on windows this DLL is automatically provided for you
# discord.opus.load_opus()


def restart_bot():
    '''Restarts the bot.'''
    os.execv(sys.executable, ['python'] + sys.argv)


async def author_in_voice(ctx):
    """
    Validates if the author of the command is in a voice channel.
        if True: channel.connect()
    """
    if ctx.message.author.voice:
        channel = discord.utils.get(
            ctx.guild.voice_channels, name=ctx.message.author.voice.channel.name)
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    else:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    if not ctx.message.guild.voice_client:
        if voice is not None:  # test if voice is None
            if not voice.is_connected():
                await channel.connect()
            else:
                pass
        else:
            await channel.connect()


@bot.command(name='res', help="Restart the bot")
async def restart(ctx):
    await ctx.send("Bot Restarted.")  # actually not yet
    restart_bot()


@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()


@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command(name='play', help='To play song, [command_prefix]play [song name]')
async def play(ctx, *terms):

    try:
        await author_in_voice(ctx)
    except:
        return

    print(*terms)

    voice_client = ctx.message.guild.voice_client

    async with ctx.typing():

        # Get & Load YouTube Song
        url = await yt_query(YT_API_KEY, *terms)
        song = pafy.new(url).getbestaudio()

        # add song to end of dict
        song_dict[len(song_dict)] = {'title': song.title, 'url': song.url}

        try:
            # voice_client.is_playing()
            if voice_client.is_playing():
                await ctx.send('**Queued:** {}'.format(song.title))
                return
        except AttributeError:
            return

        song = song_dict[counter['count']]
        # print(song)

        source = discord.FFmpegPCMAudio(
            song['url'], **FFMPEG_OPTIONS)

        msg = await ctx.send('**Now playing:** {}'.format(song['title']))
        voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(
            play_next(ctx, msg=msg), bot.loop))
        # asyncio.run_coroutine_threadsafe(play_next(ctx, msg=msg), bot.loop)
        # play_next(ctx, msg=msg)


@bot.command(name='next', help='Next song!')
async def play_next(ctx, msg=None):
    await asyncio.sleep(2)
    voice_client = ctx.message.guild.voice_client
    # voice_channel.stop()
    counter['count'] += 1

    try:
        song = song_dict[counter['count']]
    except KeyError:
        await ctx.send('End of List! Use --play to add more songs.')
        song_dict.clear()
        await msg.delete()
        counter['count'] = 0
        return
    if msg:
        await msg.delete()
    voice_client.pause()
    source = discord.FFmpegPCMAudio(
        song['url'], **FFMPEG_OPTIONS)  # executable="./ffmpeg.exe",
    msg = await ctx.send('**Now playing:** {}'.format(song['title']))
    voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(
        play_next(ctx, msg=msg), bot.loop))
    # play_next(ctx, msg=msg)
    # asyncio.run_coroutine_threadsafe(play_next(ctx, msg=msg), bot.loop)
    # await asyncio.sleep(2)


@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")


@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        song_dict.clear()
        voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


bot.run(TOKEN)
