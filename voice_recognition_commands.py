# import discord
# from discord.ext import commands
# import os
# import speech_recognition as sr
# import asyncio

# intents = discord.Intents.default()
# intents.voice_states = True

# bot = commands.Bot(command_prefix="!", intents=intents)

# # Function to encapsulate speech recognition
# async def recognize_speech():
#     loop = asyncio.get_event_loop()
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         audio = await loop.run_in_executor(None, r.listen, source)

#     try:
#         text = await loop.run_in_executor(None, r.recognize_google, audio)
#         return text
#     except sr.UnknownValueError:
#         print("Speech recognition could not understand audio")
#     except sr.RequestError as e:
#         print("Could not request results from Google Speech Recognition service; {0}".format(e))
#     return ""

# @bot.event
# async def on_ready():
#     print(f"Bot is ready. Logged in as {bot.user}")

# @bot.event
# async def on_voice_state_update(member, before, after):
#     if member == bot.user:
#         return

#     if before.channel is None and after.channel is not None:
#         # User has joined a voice channel
#         if member == bot.user:
#             # Bot has joined the voice channel
#             speech_text = await recognize_speech()

#             if "Yooo Jarvis mute these" in speech_text:
#                 channel = after.channel

#                 for member in channel.members:
#                     if member != bot.user:
#                         await member.edit(mute=True)

#                 print("Muted everyone")
#             elif "Jarvis unmute" in speech_text:
#                 channel = after.channel

#                 for member in channel.members:
#                     if member != bot.user:
#                         await member.edit(mute=False)

#                 print("Unmuted everyone")
#             else:
#                 print("Invalid command")
# @bot.command()
# async def join(ctx):
#     if ctx.author.voice is None:
#         await ctx.send("You must be in a voice channel to use this command.")
#         return

#     channel = ctx.author.voice.channel
#     await channel.connect()

#     # Call speech recognition function when the bot joins a voice channel
#     speech_text = await recognize_speech()

#     if "Yooo Jarvis mute these" in speech_text:
#         for member in channel.members:
#             if member != bot.user:
#                 await member.edit(mute=True)

#         print("Muted everyone")
#     elif "Jarvis unmute" in speech_text:
#         for member in channel.members:
#             if member != bot.user:
#                 await member.edit(mute=False)

#         print("Unmuted everyone")
#     else:
#         print("Invalid command")


# @bot.command()
# async def leave(ctx):
#     voice_client = ctx.guild.voice_client
#     if voice_client is not None:
#         await voice_client.disconnect()
