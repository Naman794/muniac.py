import discord
from discord.ext import commands, tasks
from discord import errors, guild, member, message, permissions, user
from urllib import response
from urllib3.util import url
import DiscordUtils
import json
from discord.ext.commands import has_permissions

from keep_alive import keep_alive




music = DiscordUtils.Music()


def get_prefix(bot, message):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
  return prefixes[str(message.guild.id)]

bot = commands.Bot(command_prefix=commands.when_mentioned_or('//'))

@bot.event
async def on_guild_join(guild):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)

  prefixes[str(guild.id)] = "m!"

  with open("prefixes.json", "w") as f:
    json.dump(prefixes,f)

@bot.command()
@commands.has_permissions(administrator = True)
async def changeprefix(ctx, prefix):
  with open("prefixes.json", "w") as f:
    prefixes = json.load(f)
  prefixes[str(ctx.guild.id)] = prefix

  with open("prefixes.json", "w") as f:
    json.dump(prefixes, f)

  await ctx.send(f"promise <pending>\nSuccessfully changed to {prefix}")

@bot.command()
async def join(ctx):
    await ctx.author.voice.channel.connect() 


@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command(aliases = ['p','Play'])
async def play(ctx, *, name):
    voice_state = ctx.author.voice

    if voice_state is None:
      return await ctx.send("You are not connected to any Voice Channel")

    player = music.get_player(guild_id=ctx.guild.id)
    if not player:
          await ctx.author.voice.channel.connect()
          player = music.create_player(ctx, ffmpeg_error_betterfix=True)
    if not ctx.voice_client.is_playing():
        
        await player.queue(name, search=True)
        song = await player.play()
        await ctx.send(f'🔍Searching for 🎵`{song.name}`')
        sngg = await ctx.send(f"**Now Playing** {song.name}")
        await sngg.add_reaction("🎧")
    else:
        song= await player.queue(name, search=True)
        await ctx.send(f"Queued {song.name}")

    if ctx.voice_client.is_playing() == False:
        
      await asyncio.sleep(1)
      await ctx.voice_client.disconnect()
      await ctx.send("**Disconnected Due to inactivity**")


@bot.command()
async def pause(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.pause()
    sng = await ctx.send(f"Paused {song.name}")
    await sng.add_reaction("✋")

@bot.command()
async def stop(ctx):
    player = music.get_player(guild_id =ctx.guild.id)
    await player.stop()
    stp = await ctx.send("Stopped")
    await stp.add_reaction("🖖")

@bot.command()
async def loop(ctx):
    player = music.get_player(guild_id =ctx.guild.id)
    song = await player.toggle_song_loop()
    if song.is_looping:
        await ctx.send(f"Enabled loop for {song.name}")
    else:
        await ctx.send(f"Disabled loop for {song.name}")


@bot.command()
async def skip(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    data = await player.skip(force=True)
    if len(data) == 2:
        await ctx.send(f"Skipped from {data[0].name} to {data[1].name}")
    else:
        await ctx.send(f"Skipped {data[0].name}")

@bot.command()
async def volume(ctx, vol):
    player = music.get_player(guild_id=ctx.guild.id)
    song, volume = await player.change_volume(float(vol) / 100) # volume should be a float between 0 to 1
    await ctx.send(f"Changed volume for {song.name} to {volume*100}%")

@bot.command()
async def np(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = player.now_playing()
    await ctx.send(song.name)

keep_alive()
bot.run(Tokens)
