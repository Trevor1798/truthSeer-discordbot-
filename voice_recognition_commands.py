import discord
from discord.ext import commands
import os
import speech_recognition as sr

intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Function to encapsulate speech, call it in the command functions
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    # Perform speech recognition on the captured audio
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return ""


@bot.command()
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("You must be in a voice channel to use this command.")
        return

    channel = ctx.author.voice.channel
    await channel.connect()


@bot.command()
async def leave(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client is not None:
        await voice_client.disconnect()


@bot.command()
async def mute_everyone(ctx):
    speech_text = recognize_speech()

    if "Yooo Jarvis mute these" in speech_text:
        if ctx.author.voice and ctx.author.voice.channel:
            channel = ctx.author.voice.channel

            for member in channel.members:
                if member != ctx.author:
                    await member.edit(mute=True)

            await ctx.send("I've muted everyone, sir")
        else:
            await ctx.send("It didn't work, sir")

    else:
        await ctx.send("Sir, your command was invalid")


@bot.command()
async def unmute_everyone(ctx):
    speech_text = recognize_speech()

    if "Jarvis unmute" in speech_text:
        if ctx.author.voice and ctx.author.voice.channel:
            channel = ctx.author.voice.channel

            for member in channel.members:
                if member != ctx.author:
                    await member.edit(mute=False)

            await ctx.send("I've unmuted everyone, sir")
        else:
            await ctx.send("It didn't work, sir")

    else:
        await ctx.send("Sir, your command was invalid")
