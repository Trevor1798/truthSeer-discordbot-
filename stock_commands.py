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

watchlists = {}
watchlists["Pineapple"] = ["SPY", "QQQ", "TSLA", "AMZN", "BA", "NVDA", "GME", "GOOGL", "AAPL", "META", "DIS", "NFLX", "AMD", "HD", "SBUX"]


def create_embed(description):
    embed = discord.Embed(description = description, color = discord.Color.orange())
    return embed
 

@bot.command()
async def t(ctx, ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")

        if len(data) > 0:
            daily_open = data["Open"].iloc[0]
            current_high = data["High"].max()
            current_low = data["Low"].min()

            if len(data) >= 1:
                current_price = data["Close"].iloc[-1]
            else:
                current_price = None

            description = f"Daily Opening Price: ${daily_open:.2f}\n" \
                          f"Current High of the Day: ${current_high:.2f}\n" \
                          f"Current Low of the Day: ${current_low:.2f}\n"

            if current_price is not None:
                description += f"Current Price (15 min): ${current_price:.2f}"

                # Create a dark-themed candlestick chart
                mc = mpf.make_marketcolors(up='green', down='red')
                s = mpf.make_mpf_style(marketcolors=mc, facecolor='black', edgecolor='grey')

                fig, ax = plt.subplots(figsize=(12, 9))
                mpf.plot(data, type='candle', ax=ax, volume=False, style=s)

                plt.title(f"{ticker.upper()} Candlestick Chart", color='grey')
                plt.xlabel("Date", color='orange')
                plt.ylabel("Time", color='orange')
                plt.xticks(color='grey')
                plt.yticks(color='grey')
                ax.xaxis.label.set_color('orange')
                ax.yaxis.label.set_color('orange')
                ax.spines['bottom'].set_color('grey')
                ax.spines['top'].set_color('grey')
                ax.spines['left'].set_color('grey')
                ax.spines['right'].set_color('grey')

                # Plot the candles with color based on close and opening prices
                # for i in range(len(data)):
                #     if data['Close'].iloc[i] >= data['Open'].iloc[i]:
                #         color = mc['edge']['up']  # Green for bullish candles
                #     else:
                #         color = mc['edge']['down']  # Red for bearish candles
                #     mpf.plot(data.iloc[i:i+1], type='candle', ax=ax, volume=False, color=color, style=s)

                # Save the chart as an image
                image_stream = BytesIO()
                plt.savefig(image_stream, format='png', facecolor='black')
                image_stream.seek(0)

                # Create a file attachment from the image
                file = discord.File(image_stream, filename="chart.png")

                # Create the embed with the chart image
                embed = create_embed(description)
                embed.set_image(url="attachment://chart.png")

                # Send the embed with the chart image
                await ctx.send(file=file, embed=embed)
            else:
                description += "No data available for current or previous price."

            # embed = create_embed(description)
            # await ctx.send(embed=embed)
        else:
            await ctx.send(f"No data available for {ticker.upper()}")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

@bot.command()
async def StockWatch(ctx):
    embed = discord.Embed(
        title = "Stock Watch",
        description = "Hello! I've built a small list of popular stocks from the market. These are commonly traded and some of my favorites. They include information about the daily opening price, current high of the day, current price, and previous price following the 15-minute chart. Try querying for any stock on the stock market and it should return information! To look for a stock type !t AAPL for example also if you query for just one ticker and its green that means the current candle (15min) is greater or higher than the previous candle, if its red vice versa. You can also add your own stocks to the current WatchList just type !AddStock AAPL, AAPL is already in there but if theres a ticker you would like to add that isn't in there this command will handle that!",
        color = discord.Color.gold()
    )

    embed.add_field(name="Symbols", value = "!WatchList (watchlist name)\n !AddStock (watchlist_name) (ticker) - This will add a stock to a specific watchlist and if there is none it will create one!\n !ListWatch - This will List of our WatchLists \n!t SPY\n!t QQQ\n!t TSLA\n!t AMZN\n!t BA\n!t NVDA\n!t GME\n!t GOOGLE\n!t AAPL\n!t FB\n!t DIS\n!t NFLX\n!t AMD\n!t HD\n!t SBUX")
    embed.set_footer(text ="Please type the symbols exactly as shown to query for information. These are just examples try any ticker :)" )
    await ctx.send(embed = embed)


# Command to add stocks to the watchlist
@bot.command()
async def AddStock(ctx, watchlist_name, ticker):
    global watchlists
    # Check if the ticker symbol is valid
    stock = yf.Ticker(ticker)
    try:
        data = stock.history(period="15m")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")
        return
    
    if len(data) > 0:
        # Check if the watchlist already exists, create a new one if it doesn't
        if watchlist_name not in watchlists:
            watchlists[watchlist_name] = []
        
        # Add the stock to the chosen watchlist
        if ticker not in watchlists[watchlist_name]:
            watchlists[watchlist_name].append(ticker)
            await ctx.send(f"Stock {ticker} added to watchlist {watchlist_name}.")
        else:
            await ctx.send(f"Stock {ticker} is already in watchlist {watchlist_name}.")
        r.set(watchlist_name, ','.join(watchlists[watchlist_name]))
    else:
        await ctx.send(f"No data available for {ticker.upper()}")

@bot.command()
async def WatchList(ctx, watchlist_name):
    global watchlists

    if watchlist_name not in watchlists:
        await ctx.send(f"Watchlist '{watchlist_name}' does not exist.")
        return

    if r.exists(watchlist_name):
        # Retrieve the watchlist data from Redis
        watchlist_data = r.get(watchlist_name).decode().split(',')
        watchlist = watchlist_data if watchlist_data else []
    else:
        # Retrieve the watchlist from the in-memory watchlists dictionary
        watchlist = watchlists[watchlist_name]


    if len(watchlist) > 0:
        embed = discord.Embed(title=f"Watchlist - {watchlist_name} - Current Price", color=0xB8860B)
        for ticker in watchlist:
            data = yf.Ticker(ticker).history(period="15m")
            if not data.empty:
                current_price = data["Close"].iloc[-1]
                embed.add_field(name=ticker, value=f"${current_price:.2f}", inline=True)
            else:
                embed.add_field(name=ticker, value="No data available", inline=True)

        r.set(watchlist_name, ','.join(watchlist))
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"The watchlist '{watchlist_name}' is empty.")


@bot.command()
async def ListWatch(ctx):
    global watchlists
    
    # Create an embedded message with a gold color
    embed = discord.Embed(title="Watchlists", color=discord.Color.gold())
    

    keys = r.keys()  

    for key in keys:
        watchlist_name = key.decode()  # Convert the key to string
        watchlist_data = r.get(key).decode().split(',')  # Get the watchlist data from Redis and split it into a list
    # Iterate over the watchlists and add them to the embedded message
        # Create a string representation of the stocks in the watchlist
        stocks_str = "\n".join(watchlist_data) if watchlist_data else "No stocks in this watchlist."
        # Add the watchlist name and stocks to the embedded message
        embed.add_field(name=watchlist_name, value=stocks_str, inline=False)
    for watchlist_name, stocks in watchlists.items():
        if watchlist_name not in r.keys():
            # Create a string representation of the stocks in the watchlist
            stocks_str = "\n".join(stocks) if stocks else "No stocks in this watchlist."    


    # Send the embedded message
    await ctx.send(embed=embed)
