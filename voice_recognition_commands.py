import discord 
from discord.ext import commands 
import os
import speech_recognition as sr
from gtts import gTTS
import playsound
import pulsectl


# Set the audio backend to PulseAudio
sr.AudioFile.DEFAULT_READER = "pulseaudio"

pulse = pulsectl.Pulse('my-client')

def set_default_source():
    source_info = pulse.source_list()[0]
    default_source = pulse.get_source_by_index(source_info.index)
    pulse.default_set_source(default_source)

set_default_source()



intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)


# Function to encapsulate speech recognition, call it in the command functions
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone(device_index=pulsectl.Pulse('my-client').source_list()[0].index) as source:
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
    try:
        channel = ctx.author.voice.channel
        await channel.connect()
        set_default_source() 
        recognize_speech()
    except Exception as e:
        print("An error occurred while joining the voice channel:", e)
        await ctx.send("An error occurred while joining the voice channel.")


@bot.command()
async def leave(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client is not None:
        try:
            await voice_client.disconnect()
        except Exception as e:
            print("An error occurred while leaving the voice channel:", e)
            await ctx.send("An error occurred while leaving the voice channel.")


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
