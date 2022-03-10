import os
import sys
import discord
import pafy
import asyncio
import getreddit
import json
from asgiref.sync import async_to_sync
from discord.ext import commands
from config import FFMPEG_OPTIONS, TOKEN
from ctnrs import counter  # song_dict
from search_yt import yt_query, YT_API_KEY, get_vid_name
# FFMPEG_OPTIONS = {
#     'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


# BOT
intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='--')
song_dict = dict()


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


@bot.command(name='rlist', help='[cmd][sub]')
async def rlist(ctx, subreddit):
    data = getreddit.post_data(subreddit, '100')
    filtered_data = json.loads(getreddit.filter_data(data, criteria='youtu'))
    # if len(song_dict) > 0:
    for song in filtered_data:
        # print(song)
        song_dict[len(song_dict)] = {
            'title': filtered_data[song]['title'], 'url': filtered_data[song]['url']}
    # else:

    # song_dict.update(json.loads(getreddit.filter_data(
    #     getreddit.post_data(*subreddit, '100')), criteria='youtu'))
    print(song_dict)
    await play(ctx, main=False)


# DO DRYS, MAKE MODULAR!!!
@ bot.command(name='play', help='To play song, [command_prefix]play [song name]')
async def play(ctx, *terms, main=True):
    await asyncio.sleep(1)

    try:
        await author_in_voice(ctx)
    except:
        return

    voice_client = ctx.message.guild.voice_client

    async with ctx.typing():

        # Get & Load YouTube Song
        if main:
            print(*terms)
            url = await yt_query(YT_API_KEY, *terms)
        else:
            url = song_dict[counter['count']]['url']

        song = pafy.new(url).getbestaudio()
        song_dict[len(song_dict)] = {'title': song.title, 'url': url}

        try:
            # voice_client.is_playing()
            if voice_client.is_playing():
                await ctx.send('**Queued:** {}'.format(song.title))
                return
        except AttributeError:
            return

        try:
            song_dict[len(song_dict)] = {
                'title': song.title, 'url': song.url}
        except AttributeError:
            await ctx.send('No song found.')
            return

        song = song_dict[counter['count']]
        # print(song)
        print(song_dict)

        source = discord.FFmpegPCMAudio(
            song['url'], **FFMPEG_OPTIONS)
        msg = await ctx.send('**Now playing:** {}'.format(song['title']))
        voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(
            play_next(ctx, msg=msg, bot_action=True), bot.loop))

        # asyncio.run_coroutine_threadsafe(play_next(ctx, msg=msg), bot.loop)
        # play_next(ctx, msg=msg)


@ bot.command(name='next', help='Next song!')
async def play_next(ctx, msg=None, bot_action=None):
    await asyncio.sleep(2)
    voice_client = ctx.message.guild.voice_client
    # voice_channel.stop()
    try:
        song_dict[counter['count'] + 1]
        counter['count'] += 1
        song = song_dict[counter['count']]

        if len(song['url']) < 100:
            song_pafy = pafy.new(song['url']).getbestaudio()
            song['url'] = song_pafy.url
            song['title'] = song_pafy.title

    except KeyError:
        if bot_action is None:
            await ctx.send('End of List! Use --play to add more songs..')
            return
        else:
            await asyncio.sleep(2)
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
        play_next(ctx, msg=msg, bot_action=True), bot.loop))
    # play_next(ctx, msg=msg)
    # asyncio.run_coroutine_threadsafe(play_next(ctx, msg=msg), bot.loop)
    # await asyncio.sleep(2)


@ bot.command(name='back', help='Previous song!')
async def play_prev(ctx, msg=None):
    await asyncio.sleep(2)
    voice_client = ctx.message.guild.voice_client
    # voice_channel.stop()
    if counter['count'] != 0:
        counter['count'] -= 1
    else:
        await ctx.send('This is the first song in the list!')
        return
    try:
        song = song_dict[counter['count']]
    except:
        print('Error, maybe do ExceptKeyError?')
    if msg:
        await msg.delete()
    voice_client.pause()
    source = discord.FFmpegPCMAudio(
        song['url'], **FFMPEG_OPTIONS)  # executable="./ffmpeg.exe",
    msg = await ctx.send('**Now playing:** {}'.format(song['title']))
    voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(
        play_next(ctx, msg=msg), bot.loop))
    # asyncio.run_coroutine_threadsafe(play_next(ctx, msg=msg), bot.loop)
    # await asyncio.sleep(2)


@ bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


@ bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")


@ bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        song_dict.clear()
        voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


bot.run(TOKEN)
