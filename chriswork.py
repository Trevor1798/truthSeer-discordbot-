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
# from dotenv import load_dotenv


#load_dotenv()




target_channel_id = 1111186051520790550

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
