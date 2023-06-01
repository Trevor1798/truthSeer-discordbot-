import discord 
from discord.ext import commands 
import os
import speech_recognition as sr
from gtts import gTTS
import playsound


intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)


# Function to encapsulate speech recognition, call it in the command functions
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return ""


# Example usage
# text = recognize_speech()
# print("You said:", text)


@bot.command()
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("You must be in a voice channel to use this command.")
        return
    
    channel = ctx.author.voice.channel
    await channel.connect()
    recognize_speech()


@bot.command()
async def leave(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client is not None:
        await voice_client.disconnect()


async def mute_everyone(ctx):
    speech_text = recognize_speech()

    if "Yooo Jarvis mute these" in speech_text:
        if ctx.author.voice and ctx.author.voice.channel:
            channel = ctx.author.voice.channel

            for member in channel.members:
                if member != ctx.author:
                    await member.edit(mute=True)

            tts = gTTS("I've muted everyone, sir")
            tts.save("muted.mp3")
            playsound.playsound("muted.mp3", True)
            os.remove("muted.mp3")
        else:
            tts = gTTS("It didn't work, sir")
            tts.save("error.mp3")
            playsound.playsound("error.mp3", True)
            os.remove("error.mp3")
    else:
        tts = gTTS("Sir, your command was invalid")
        tts.save("invalid.mp3")
        playsound.playsound("invalid.mp3", True)
        os.remove("invalid.mp3")


async def unmute_everyone(ctx):
    speech_text = recognize_speech()

    if "Jarvis unmute" in speech_text:
        if ctx.author.voice and ctx.author.voice.channel:
            channel = ctx.author.voice.channel

            for member in channel.members:
                if member != ctx.author:
                    await member.edit(mute=False)

            tts = gTTS("I've unmuted everyone, sir")
            tts.save("unmuted.mp3")
            playsound.playsound("unmuted.mp3", True)
            os.remove("unmuted.mp3")
        else:
            tts = gTTS("It didn't work, sir")
            tts.save("error.mp3")
            playsound.playsound("error.mp3", True)
            os.remove("error.mp3")
    else:
        tts = gTTS("Sir, your command was invalid")
        tts.save("invalid.mp3")
        playsound.playsound("invalid.mp3", True)
        os.remove("invalid.mp3")
