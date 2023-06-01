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

redis_url = os.environ.get("REDISCLOUD_URL")
r = redis.Redis.from_url(redis_url)

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


WEATHER_KEY = os.environ.get("API_WEATHER_KEY")
BASE_URL = os.environ.get("WEATHER_API_URL")

def create_embed(description):
    embed = discord.Embed(description = description, color = discord.Color.orange())
    return embed

#Weather API function
@bot.command()
async def weather(ctx, city):
    params = {
        'q': city,
        'appid': WEATHER_KEY,
        'units': 'imperial'
    }
    response = requests.get(BASE_URL, params=params)
    weather_data = response.json()

    print(weather_data)
    if 'main' in weather_data:
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]
        weather_description = weather_data["weather"][0]["description"]
    
        if response.status_code == 200:
            embed = discord.Embed(title=f"Weather in {city}", color=discord.Colour.teal())
            embed.add_field(name="Description", value=weather_description)
            embed.add_field(name="Temperature", value=f"{temperature}°F")
            embed.add_field(name="Humidity", value=humidity)
            embed.add_field(name="Wind Speed", value=f"{wind_speed} m/s")
            await ctx.send(embed=embed)
        else:
            await ctx.send("Failed to fetch weather information")
    else:
        await ctx.send("City not included in this API bozo, this the free tier")



#Cat API function
@bot.command()
async def cat(ctx):
    api_key = os.environ.get("CAT_API_KEY")
    headers = {
        "x-api-key": api_key
    }
    url = "https://api.thecatapi.com/v1/images/search"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        image_url = data[0]["url"]
        await ctx.send(image_url)
    else:
        await ctx.send("Failed to fetch the cat image")
@bot.command()
async def kitty10x(ctx):
    api_key = os.environ.get("CAT_API_KEY")
    headers = {
        "x-api-key": api_key
    }
    url = "https://api.thecatapi.com/v1/images/search?limit=10"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for cat_data in data:
            cat_image = cat_data["url"]
            embed = discord.Embed()
            embed.set_image(url=cat_image)
            await ctx.send(embed=embed)
    else:
        await ctx.send("Maybe 10 is to many right neow")

#Joke API function    
@bot.command()
async def joke(ctx, category="Any"):
    url = f"https://v2.jokeapi.dev/joke/{category}"
    response = requests.get(url)
    joke_data = response.json()

    if response.status_code == 200:
        if joke_data["type"] == "single":
            joke = joke_data["joke"]
        else:
            joke = f"{joke_data['setup']} {joke_data['delivery']}"
        await ctx.send(joke)
    else:
        await ctx.send("Failed to fetch that one, maybe you dont deserve to hear it")



@bot.command()
async def hello(ctx):
    await ctx.send("I know more than you")


@bot.command()
async def whatsup(ctx):
    await ctx.send("Me?")
    await asyncio.sleep(2)  # Wait for 5 seconds
    await ctx.send("Nothing...")
    await asyncio.sleep(2)  # Wait for another 10 seconds
    await ctx.send("Just hanging around")


@bot.command()
async def sauce(ctx, *tags):
    wf = WaifuAioClient()
    async with aiohttp.ClientSession() as session:
        for _ in range(5):
            if tags:
                image = await wf.search(included_tags=tags)
            else:
                image = await wf.search()

            async with session.get(image.url) as response:
                if response.status == 200:
                    data = await response.read()
                    file = discord.File(BytesIO(data), filename="image.jpg")
                    await ctx.send(file=file)
                else:
                    await ctx.send("Failed to retrieve the image.")

    await session.close()

        
