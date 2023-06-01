import discord
from discord.ext import commands
import os
import asyncio
import requests
import yfinance as yf
import redis
import matplotlib.pyplot as plt
from waifuim import WaifuAioClient
import mplfinance as mpf
import pandas
from io import BytesIO
import aiohttp
from stock_commands import *
from friend_commands import *
from api_commands import *



redis_url = os.environ.get("REDISCLOUD_URL")
r = redis.Redis.from_url(redis_url)


target_channel_id = 1111186051520790550


intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)



# bot.add_command(t)
# bot.add_command(StockWatch)
# bot.add_command(AddStock)
# bot.add_command(WatchList)
# bot.add_command(ListWatch)
# bot.add_command(weather)
# bot.add_command(cat)
# bot.add_command(kitty10x)
# bot.add_command(joke)
# bot.add_command(hello)
# bot.add_command(whatsup)
# bot.add_command(sauce)
# bot.add_command(Jay)
# bot.add_command(Frank)
# bot.add_command(Vam)
# bot.add_command(Chris)
# bot.add_command(Trev)
# bot.add_command(Sam)
# bot.add_command(command_help)


# Add error handling and command_not_found event
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found.")
    else:
        print("Error:", error)


@bot.event
async def on_ready():
    print("Bot is ready. Logged in as", bot.user)
 
    target_channel = bot.get_channel(target_channel_id)
    if target_channel:
        await target_channel.send("Bot connected to the target channel.")
    else:
        print(f"Failed to find the target channel with ID: {target_channel_id}")


async def start():
    extensions = [
        'stock_commands',
        'friend_commands',
        'api_commands'
    ]
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"Failed to load extension {extension}: {e}")
            
        await start()




bot.run(os.environ["BOT_TOKEN"])