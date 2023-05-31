import discord
from discord.ext import commands
import os
import asyncio
import requests
import yfinance as yf


target_channel_id = 1111186051520790550

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
 
@bot.command()
async def t(ctx, ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="15m")

        if len(data) > 0:
            daily_open = data["Open"].iloc[0]
            current_high = data["High"].max()

            if len(data) >= 2:
                previous_price = data["Close"].iloc[-2]
            else:
                previous_price = None

            if len(data) >= 1:
                current_price = data["Close"].iloc[-1]
            else:
                current_price = None

            description = f"Daily Opening Price: ${daily_open:.2f}\n" \
                          f"Current High of the Day: ${current_high:.2f}\n"

            if current_price is not None and previous_price is not None:
                if current_price > previous_price:
                    color = discord.Color.green()
                    description += f"Current Price (15 min): ${current_price:.2f} (Up from previous)"
                elif current_price < previous_price:
                    color = discord.Color.red()
                    description += f"Current Price (15 min): ${current_price:.2f} (Down from previous)"
                else:
                    color = discord.Color.orange()
                    description += f"Current Price (15 min): ${current_price:.2f} (No change)"
            else:
                color = discord.Color.orange()
                description += "No data available for current or previous price."

            embed = discord.Embed(title=f"{ticker.upper()} Stock Information", description=description, color=color)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"No data available for {ticker.upper()}")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")


@bot.command()
async def StockWatch(ctx):
 embed = discord.Embed(
    title = "Stock Watch",
    description = "Hello! I've built a small list of popular stocks from the market. These are commonly traded and some of my favorites. They include information about the daily opening price, current high of the day, current price, and previous price following the 15-minute chart. Try querying for any stock on the stock market and it should return information! To look for a stock type !t AAPL for example also if you query for just one ticker and its green that means the current candle (15min) is greater or higher than the previous candle, if its red vice versa.",
    color = discord.Color.gold()
 )

 embed.add_field(name="Symbols", value = "!WatchList\n!t SPY\n!t QQQ\n!t TSLA\n!t AMZN\n!t BA\n!t NVDA\n!t GME\n!t GOOGLE\n!t AAPL\n!t FB\n!t DIS\n!t NFLX\n!t AMD\n!t HD\n!t SBUX")
 embed.set_footer(text ="Please type the symbols exactly as shown to query for information. These are just examples try any ticker :)" )
 await ctx.send(embed = embed)

@bot.command()
async def WatchList(ctx):
    tickers = ["SPY", "QQQ", "TSLA", "AMZN", "BA", "NVDA", "GME", "GOOGL", "AAPL", "META", "DIS", "NFLX", "AMD", "HD", "SBUX"]
    embed = discord.Embed(title = "WatchList - Current Prices", color=0x00FF00)

    for tick in tickers:
        data = yf.Ticker(tick).history(period="15m")
        if not data.empty:
            
            current_price = data["Close"].iloc[-1]
            embed.add_field(name=tick, value=f"${current_price:.2f}", inline=True)
        else:
            embed.add_field(name=tick, value="No data available", inline=True)
    
    await ctx.send(embed=embed)

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
            await ctx.send(f"Shiiiiiit the current weather in {city}: {weather_description}. Temperature: {temperature}°F. Humidity: {humidity}. Wind speed: {wind_speed} m/s.")
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
        cat_image = data[0]["url"]
        await ctx.send(cat_image)
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




# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as")
    target_channel = bot.get_channel(target_channel_id)
    if target_channel:
        await target_channel.send("Bot connected to the target channel.")
    else:
        print(f"Failed to find the target channel with ID: {target_channel_id}")


@bot.command()
async def hello(ctx):
    await ctx.send("I know more than you")

@bot.command()
async def whatareyoudoing(ctx):
    await ctx.send("Me?")
    await asyncio.sleep(5)  # Wait for 5 seconds
    await ctx.send("Nothing...")
    await asyncio.sleep(10)  # Wait for another 10 seconds
    await ctx.send("Just hanging around")

@bot.command()
async def whatsup(ctx):
    await ctx.send("Me?")
    await asyncio.sleep(2)  # Wait for 5 seconds
    await ctx.send("Nothing...")
    await asyncio.sleep(2)  # Wait for another 10 seconds
    await ctx.send("Just hanging around")

@bot.command()
async def Jay(ctx):
    await ctx.send("Jay is a remarkable individual who embodies the qualities of a true sigma and an alpha male. With his strong presence and charismatic aura, he effortlessly commands respect and admiration from those around him. Jay possesses a unique blend of confidence, independence, and intelligence, making him a natural leader in any situation. His unwavering determination and self-assuredness enable him to navigate life's challenges with ease and grace. Jay's calm and collected demeanor coupled with his sharp wit and keen intellect make him an engaging conversationalist and a trusted friend. His unwavering commitment to personal growth and his ability to stay true to his values are truly inspiring. Jay's magnetic personality and unparalleled charisma make him a true alpha male, leaving a lasting impact on everyone fortunate enough to know him.")

@bot.command()
async def Frank(ctx):
    await ctx.send("Frank is an extraordinary individual who has solidified his place in the world of esports as a revered multi-title champion. His exceptional skills, unwavering dedication, and strategic brilliance have propelled him to the pinnacle of competitive gaming. With a string of victories under his belt, Frank has led his teammates to numerous triumphs, demonstrating his ability to inspire and guide his fellow players to greatness. As the best in-game leader (IGL) in the industry, Frank's strategic thinking, tactical expertise, and exceptional decision-making have set him apart from his peers. He has masterfully orchestrated his team's gameplay, ensuring flawless coordination and leading them to victory. Beyond his remarkable accomplishments, Frank's humility and sportsmanship have endeared him to fans and fellow gamers alike, making him a highly respected figure in the esports community. His legacy serves as a constant inspiration for aspiring gamers, showcasing the heights that can be reached through unwavering determination and a passion for excellence.")

@bot.command()
async def Vam(ctx):
    await ctx.send("Vam is an extraordinary individual who has demonstrated unparalleled expertise in two distinct domains: options trading and the popular rhythm game, osu! His exceptional skills and remarkable achievements have solidified his reputation as the best options trader and osu player of all time. In the world of finance, Vam's astute understanding of market dynamics, coupled with his keen analytical abilities, has consistently positioned him at the forefront of options trading. His ability to anticipate market trends, identify lucrative opportunities, and execute precise trades has yielded unparalleled success, establishing him as a true master of the craft. Simultaneously, Vam's unparalleled talent in osu! has captivated the gaming community. With lightning-fast reflexes, impeccable timing, and unmatched accuracy, he effortlessly conquers even the most challenging osu! maps, earning him the admiration of fellow players worldwide. Vam's dedication to honing his skills, relentless pursuit of excellence, and unwavering commitment to continuous improvement make him an inspiration to aspiring options traders and osu players alike. His remarkable achievements and undeniable impact have solidified his status as a legend in both arenas, leaving an indelible mark on the worlds of finance and gaming.")

@bot.command()
async def Chris(ctx):
    await ctx.send("""Chris is an extraordinary individual who possesses a unique blend of talents and passions. With an unmatched sense of humor and a natural gift for storytelling, he never fails to captivate those around him with his infectious laughter and entertaining anecdotes. Chris's comedic timing and wit make him the life of every gathering, effortlessly bringing joy and laughter to everyone in his presence.
But there's more to Chris than just humor. He is a true connoisseur of anime and OG games, with an encyclopedic knowledge of their intricate storylines, memorable characters, and iconic moments. His dedication to these realms of entertainment is unwavering, and he delights in sharing his vast expertise with others, igniting their interest and sparking engaging discussions. Chris's enthusiasm for anime and OG games is infectious, turning casual fans into avid enthusiasts.
Beyond his passion for entertainment, Chris is also a future goated programmer. With an insatiable curiosity and an innate knack for problem-solving, he dives into the world of coding with unparalleled zeal. His determination to master programming languages, algorithms, and cutting-edge technologies sets him on a path toward becoming an exceptional programmer. Chris's relentless pursuit of knowledge, coupled with his creativity and analytical thinking, ensures that he will leave an indelible mark on the programming landscape.
In summary, Chris is a remarkable individual who brings laughter, knowledge, and ambition to everything he does. Whether it's cracking jokes, sharing anime trivia, or diving into the world of programming, his infectious energy and passion are an inspiration to all. With his incredible sense of humor, wealth of anime and gaming knowledge, and his drive to excel in programming, Chris is destined to leave a lasting impact and become a goated programmer in the future.""")

@bot.command()
async def Trev(ctx):
    await ctx.send("Trev is a person who defies conventional descriptions. There's no single line that can truly capture the essence of who he is, except for the simple fact that he is 'him.' With a unique blend of qualities, experiences, and perspectives, Trev is an individual like no other, constantly defying expectations and bringing his own authentic self to everything he does.")

@bot.command()
async def Sam(ctx):
    await ctx.send("Sam is an exceptional individual who encompasses the qualities of the greatest artist, animal lover, and caring person all rolled into one. As an incredibly talented writer, Sam weaves words together with mastery, creating captivating stories and evoking emotions within readers. Through her artistry, she transports people to new worlds and sparks their imaginations. Sam's love for animals knows no bounds. She devotes her time and energy to advocating for animal rights, rescuing and providing a safe haven for furry companions, and promoting their well-being. Her compassion extends beyond animals, as she consistently demonstrates a caring and selfless nature towards others. Sam has a heart of gold, always offering support, empathy, and encouragement to those around her. Her wholesome and genuine character brightens the lives of everyone she encounters. Sam is undoubtedly the best person one could have the privilege of knowing and cherishing.")


#turbulence


@bot.command()
async def command_help(ctx):
    embed = discord.Embed(title="Available Commands", description="Here are the available commands:", color=discord.Color.purple())
    embed.add_field(name="!hello", value="Greet the bot", inline=False)
    embed.add_field(name="!whatsup", value="Check what the bot is up to", inline=False)
    embed.add_field(name="!StockWatch", value="Look at a bunch of different options for querying stocks", inline=False)
    embed.add_field(name="!weather ('city')", value="Check the weather of any city included in the free tier of this API", inline=False)
    embed.add_field(name="!joke ('category')", value="Pick a joke from a category (Programming, Misc, Dark, Pun, Spooky, Christmas)", inline=False)
    embed.add_field(name="!cat", value="Randomly generate a cat image", inline=False)
    embed.add_field(name="!Jay", value="Learn about Jay, a remarkable individual who embodies the qualities of a true sigma and an alpha male", inline=False)
    embed.add_field(name="!Frank", value="Discover more about Frank, a legendary multi-title esports champion who has retired", inline=False)
    embed.add_field(name="!Vam", value="Explore the accomplishments of Vam, the best options trader and osu player of all time", inline=False)
    embed.add_field(name="!Chris", value="Learn about Chris, a hilarious storyteller, anime and OG games expert, and future goated programmer", inline=False)
    embed.add_field(name="!Trev", value="Discover the indescribable essence of Trev, a person who defies conventional descriptions", inline=False)
    embed.add_field(name="!Sam", value="Learn about Sam, an exceptional individual who is simply the best", inline=False)
    embed.add_field(name="!help", value="Display this help message", inline=False)
    await ctx.send(embed=embed)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower().startswith("hi"):
        target_channel = bot.get_channel(target_channel_id)
        if target_channel:
            await target_channel.send("Hello!")

    await bot.process_commands(message)

bot.run(os.environ["BOT_TOKEN"])



#This code was easy to write but violated the DRY principle, recently I've added a way to query for any stock and not just a limited amount 
# @bot.command()
# async def SPY(ctx):
#     try:
#         spy = yf.Ticker("SPY")
#         data = spy.history(period="15m")
        
#         if len(data) > 0:
#             daily_open = data["Open"].iloc[0]
#             current_high = data["High"].max()
            
#             if len(data) >= 2:
#                 previous_price = data["Close"].iloc[-2]
#             else:
#                 previous_price = "N/A"
            
#             if len(data) >= 1:
#                 current_price = data["Close"].iloc[-1]
#             else:
#                 current_price = "N/A"

#             description = f"Daily Opening Price: ${daily_open:.2f}\n" \
#                           f"Current High of the Day: ${current_high:.2f}\n"

#             if current_price != "N/A":
#                 description += f"Current price (15 min): ${current_price:.2f}\n"

#             if previous_price != "N/A":
#                 description += f"Previous price (15 min): ${previous_price:.2f}"

#             embed = create_embed(description)
#             await ctx.send(embed=embed)
#         else:
#             await ctx.send("No data available for SPY")
#     except Exception as e:
#         await ctx.send(f"An error occurred: {str(e)}")




# @bot.command()
# async def QQQ(ctx):
#     try:
#         spy = yf.Ticker("QQQ")
#         data = spy.history(period="15m")
        
#         if len(data) > 0:
#             daily_open = data["Open"].iloc[0]
#             current_high = data["High"].max()
            
#             if len(data) >= 2:
#                 previous_price = data["Close"].iloc[-2]
#             else:
#                 previous_price = "N/A"
            
#             if len(data) >= 1:
#                 current_price = data["Close"].iloc[-1]
#             else:
#                 current_price = "N/A"

#             description = f"Daily Opening Price: ${daily_open:.2f}\n" \
#                           f"Current High of the Day: ${current_high:.2f}\n"

#             if current_price != "N/A":
#                 description += f"Current price (15 min): ${current_price:.2f}\n"

#             if previous_price != "N/A":
#                 description += f"Previous price (15 min): ${previous_price:.2f}"

#             embed = create_embed(description)
#             await ctx.send(embed=embed)
#         else:
#             await ctx.send("No data available for QQQ")
#     except Exception as e:
#         await ctx.send(f"An error occurred: {str(e)}")





# @bot.command()
# async def TSLA(ctx):
#     try:
#         spy = yf.Ticker("TSLA")
#         data = spy.history(period="15m")
        
#         if len(data) > 0:
#             daily_open = data["Open"].iloc[0]
#             current_high = data["High"].max()
            
#             if len(data) >= 2:
#                 previous_price = data["Close"].iloc[-2]
#             else:
#                 previous_price = "N/A"
            
#             if len(data) >= 1:
#                 current_price = data["Close"].iloc[-1]
#             else:
#                 current_price = "N/A"

#             description = f"Daily Opening Price: ${daily_open:.2f}\n" \
#                           f"Current High of the Day: ${current_high:.2f}\n"

#             if current_price != "N/A":
#                 description += f"Current price (15 min): ${current_price:.2f}\n"

#             if previous_price != "N/A":
#                 description += f"Previous price (15 min): ${previous_price:.2f}"

#             embed = create_embed(description)
#             await ctx.send(embed=embed)
#         else:
#             await ctx.send("No data available for TSLA")
#     except Exception as e:
#         await ctx.send(f"An error occurred: {str(e)}")




# @bot.command()
# async def AMZN(ctx):
#     try:
#         spy = yf.Ticker("AMZN")
#         data = spy.history(period="15m")
        
#         if len(data) > 0:
#             daily_open = data["Open"].iloc[0]
#             current_high = data["High"].max()
            
#             if len(data) >= 2:
#                 previous_price = data["Close"].iloc[-2]
#             else:
#                 previous_price = "N/A"
            
#             if len(data) >= 1:
#                 current_price = data["Close"].iloc[-1]
#             else:
#                 current_price = "N/A"

#             description = f"Daily Opening Price: ${daily_open:.2f}\n" \
#                           f"Current High of the Day: ${current_high:.2f}\n"

#             if current_price != "N/A":
#                 description += f"Current price (15 min): ${current_price:.2f}\n"

#             if previous_price != "N/A":
#                 description += f"Previous price (15 min): ${previous_price:.2f}"

#             embed = create_embed(description)
#             await ctx.send(embed=embed)
#         else:
#             await ctx.send("No data available for AMZN")
#     except Exception as e:
#         await ctx.send(f"An error occurred: {str(e)}")




# @bot.command()
# async def BA(ctx):
#     try:
#         spy = yf.Ticker("BA")
#         data = spy.history(period="15m")
        
#         if len(data) > 0:
#             daily_open = data["Open"].iloc[0]
#             current_high = data["High"].max()
            
#             if len(data) >= 2:
#                 previous_price = data["Close"].iloc[-2]
#             else:
#                 previous_price = "N/A"
            
#             if len(data) >= 1:
#                 current_price = data["Close"].iloc[-1]
#             else:
#                 current_price = "N/A"

#             description = f"Daily Opening Price: ${daily_open:.2f}\n" \
#                           f"Current High of the Day: ${current_high:.2f}\n"

#             if current_price != "N/A":
#                 description += f"Current price (15 min): ${current_price:.2f}\n"

#             if previous_price != "N/A":
#                 description += f"Previous price (15 min): ${previous_price:.2f}"

#             embed = create_embed(description)
#             await ctx.send(embed=embed)
#         else:
#             await ctx.send("No data available for BA")
#     except Exception as e:
#         await ctx.send(f"An error occurred: {str(e)}")




# @bot.command()
# async def NVDA(ctx):
#     try:
#         spy = yf.Ticker("NVDA")
#         data = spy.history(period="15m")
        
#         if len(data) > 0:
#             daily_open = data["Open"].iloc[0]
#             current_high = data["High"].max()
            
#             if len(data) >= 2:
#                 previous_price = data["Close"].iloc[-2]
#             else:
#                 previous_price = "N/A"
            
#             if len(data) >= 1:
#                 current_price = data["Close"].iloc[-1]
#             else:
#                 current_price = "N/A"

#             description = f"Daily Opening Price: ${daily_open:.2f}\n" \
#                           f"Current High of the Day: ${current_high:.2f}\n"

#             if current_price != "N/A":
#                 description += f"Current price (15 min): ${current_price:.2f}\n"

#             if previous_price != "N/A":
#                 description += f"Previous price (15 min): ${previous_price:.2f}"

#             embed = create_embed(description)
#             await ctx.send(embed=embed)
#         else:
#             await ctx.send("No data available for NVDA")
#     except Exception as e:
#         await ctx.send(f"An error occurred: {str(e)}")




# @bot.command()
# async def GME(ctx):
#     try:
#         spy = yf.Ticker("GME")
#         data = spy.history(period="15m")
        
#         if len(data) > 0:
#             daily_open = data["Open"].iloc[0]
#             current_high = data["High"].max()
            
#             if len(data) >= 2:
#                 previous_price = data["Close"].iloc[-2]
#             else:
#                 previous_price = "N/A"
            
#             if len(data) >= 1:
#                 current_price = data["Close"].iloc[-1]
#             else:
#                 current_price = "N/A"

#             description = f"Daily Opening Price: ${daily_open:.2f}\n" \
#                           f"Current High of the Day: ${current_high:.2f}\n"

#             if current_price != "N/A":
#                 description += f"Current price (15 min): ${current_price:.2f}\n"

#             if previous_price != "N/A":
#                 description += f"Previous price (15 min): ${previous_price:.2f}"

#             embed = create_embed(description)
#             await ctx.send(embed=embed)
#         else:
#             await ctx.send("No data available for GME")
#     except Exception as e:
#         await ctx.send(f"An error occurred: {str(e)}")




# @bot.command()
# async def GOOGL(ctx):
#     try:
#         spy = yf.Ticker("GOOGL")
#         data = spy.history(period="15m")
        
#         if len(data) > 0:
#             daily_open = data["Open"].iloc[0]
#             current_high = data["High"].max()
            
#             if len(data) >= 2:
#                 previous_price = data["Close"].iloc[-2]
#             else:
#                 previous_price = "N/A"
            
#             if len(data) >= 1:
#                 current_price = data["Close"].iloc[-1]
#             else:
#                 current_price = "N/A"

#             description = f"Daily Opening Price: ${daily_open:.2f}\n" \
#                           f"Current High of the Day: ${current_high:.2f}\n"

#             if current_price != "N/A":
#                 description += f"Current price (15 min): ${current_price:.2f}\n"

#             if previous_price != "N/A":
#                 description += f"Previous price (15 min): ${previous_price:.2f}"

#             embed = create_embed(description)
#             await ctx.send(embed=embed)
#         else:
#             await ctx.send("No data available for GOOGL")
#     except Exception as e:
#         await ctx.send(f"An error occurred: {str(e)}")




# @bot.command()
# async def AAPL(ctx):
#     try:
#         spy = yf.Ticker("AAPL")
#         data = spy.history(period="15m")
        
#         if len(data) > 0:
#             daily_open = data["Open"].iloc[0]
#             current_high = data["High"].max()

#             if len(data) >= 2:
#                 previous_price = data["Close"].iloc[-2]
#             else:
#                 previous_price = None

#             if len(data) >= 1:
#                 current_price = data["Close"].iloc[-1]
#             else:
#                 current_price = None

#             description = f"Daily Opening Price: ${daily_open:.2f}\n" \
#                           f"Current High of the Day: ${current_high:.2f}\n"

#             if current_price is not None and previous_price is not None:
#                 if current_price > previous_price:
#                     color = discord.Color.green()
#                     description += f"Current Price (15 min): ${current_price:.2f} (Up from previous)"
#                 elif current_price < previous_price:
#                     color = discord.Color.red()
#                     description += f"Current Price (15 min): ${current_price:.2f} (Down from previous)"
#                 else:
#                     color = discord.Color.orange()
#                     description += f"Current Price (15 min): ${current_price:.2f} (No change)"
#             else:
#                 color = discord.Color.orange()
#                 description += "No data available for current or previous price."

#             embed = discord.Embed(title="AAPL Stock Information", description=description, color=color)
#             await ctx.send(embed=embed)
#         else:
#             await ctx.send("No data available for AAPL")
#     except Exception as e:
#         await ctx.send(f"An error occurred: {str(e)}")




# @bot.command()
# async def META(ctx):
#     try:
#         spy = yf.Ticker("META")
#         data = spy.history(period="15m")
        
#         if len(data) > 0:
#             daily_open = data["Open"].iloc[0]
#             current_high = data["High"].max()

#             if len(data) >= 2:
#                 previous_price = data["Close"].iloc[-2]
#             else:
#                 previous_price = None

#             if len(data) >= 1:
#                 current_price = data["Close"].iloc[-1]
#             else:
#                 current_price = None

#             description = f"Daily Opening Price: ${daily_open:.2f}\n" \
#                           f"Current High of the Day: ${current_high:.2f}\n"

#             if current_price is not None and previous_price is not None:
#                 if current_price > previous_price:
#                     color = discord.Color.green()
#                     description += f"Current Price (15 min): ${current_price:.2f} (Up from previous)"
#                 elif current_price < previous_price:
#                     color = discord.Color.red()
#                     description += f"Current Price (15 min): ${current_price:.2f} (Down from previous)"
#                 else:
#                     color = discord.Color.orange()
#                     description += f"Current Price (15 min): ${current_price:.2f} (No change)"
#             else:
#                 color = discord.Color.orange()
#                 description += "No data available for current or previous price."

#             embed = discord.Embed(title="META Stock Information", description=description, color=color)
#             await ctx.send(embed=embed)
#         else:
#             await ctx.send("No data available for META")
#     except Exception as e:
#         await ctx.send(f"An error occurred: {str(e)}")




# @bot.command()
# async def DIS(ctx):
#     try:
#         spy = yf.Ticker("DIS")
#         data = spy.history(period="15m")
        
#         if len(data) > 0:
#             daily_open = data["Open"].iloc[0]
#             current_high = data["High"].max()

#             if len(data) >= 2:
#                 previous_price = data["Close"].iloc[-2]
#             else:
#                 previous_price = None

#             if len(data) >= 1:
#                 current_price = data["Close"].iloc[-1]
#             else:
#                 current_price = None

#             description = f"Daily Opening Price: ${daily_open:.2f}\n" \
#                           f"Current High of the Day: ${current_high:.2f}\n"

#             if current_price is not None and previous_price is not None:
#                 if current_price > previous_price:
#                     color = discord.Color.green()
#                     description += f"Current Price (15 min): ${current_price:.2f} (Up from previous)"
#                 elif current_price < previous_price:
#                     color = discord.Color.red()
#                     description += f"Current Price (15 min): ${current_price:.2f} (Down from previous)"
#                 else:
#                     color = discord.Color.orange()
#                     description += f"Current Price (15 min): ${current_price:.2f} (No change)"
#             else:
#                 color = discord.Color.orange()
#                 description += "No data available for current or previous price."

#             embed = discord.Embed(title="DIS Stock Information", description=description, color=color)
#             await ctx.send(embed=embed)
#         else:
#             await ctx.send("No data available for DIS")
#     except Exception as e:
#         await ctx.send(f"An error occurred: {str(e)}")




# @bot.command()
# async def NFLX(ctx):
#     try:
#         spy = yf.Ticker("NFLX")
#         data = spy.history(period="15m")
        
#         if len(data) > 0:
#             daily_open = data["Open"].iloc[0]
#             current_high = data["High"].max()

#             if len(data) >= 2:
#                 previous_price = data["Close"].iloc[-2]
#             else:
#                 previous_price = None

#             if len(data) >= 1:
#                 current_price = data["Close"].iloc[-1]
#             else:
#                 current_price = None

#             description = f"Daily Opening Price: ${daily_open:.2f}\n" \
#                           f"Current High of the Day: ${current_high:.2f}\n"

#             if current_price is not None and previous_price is not None:
#                 if current_price > previous_price:
#                     color = discord.Color.green()
#                     description += f"Current Price (15 min): ${current_price:.2f} (Up from previous)"
#                 elif current_price < previous_price:
#                     color = discord.Color.red()
#                     description += f"Current Price (15 min): ${current_price:.2f} (Down from previous)"
#                 else:
#                     color = discord.Color.orange()
#                     description += f"Current Price (15 min): ${current_price:.2f} (No change)"
#             else:
#                 color = discord.Color.orange()
#                 description += "No data available for current or previous price."

#             embed = discord.Embed(title="NFLX Stock Information", description=description, color=color)
#             await ctx.send(embed=embed)
#         else:
#             await ctx.send("No data available for NFLX")
#     except Exception as e:
#         await ctx.send(f"An error occurred: {str(e)}")



# @bot.command()
# async def AMD(ctx):
#     try:
#         spy = yf.Ticker("AMD")
#         data = spy.history(period="15m")
        
#         if len(data) > 0:
#             daily_open = data["Open"].iloc[0]
#             current_high = data["High"].max()

#             if len(data) >= 2:
#                 previous_price = data["Close"].iloc[-2]
#             else:
#                 previous_price = None

#             if len(data) >= 1:
#                 current_price = data["Close"].iloc[-1]
#             else:
#                 current_price = None

#             description = f"Daily Opening Price: ${daily_open:.2f}\n" \
#                           f"Current High of the Day: ${current_high:.2f}\n"

#             if current_price is not None and previous_price is not None:
#                 if current_price > previous_price:
#                     color = discord.Color.green()
#                     description += f"Current Price (15 min): ${current_price:.2f} (Up from previous)"
#                 elif current_price < previous_price:
#                     color = discord.Color.red()
#                     description += f"Current Price (15 min): ${current_price:.2f} (Down from previous)"
#                 else:
#                     color = discord.Color.orange()
#                     description += f"Current Price (15 min): ${current_price:.2f} (No change)"
#             else:
#                 color = discord.Color.orange()
#                 description += "No data available for current or previous price."

#             embed = discord.Embed(title="AMD Stock Information", description=description, color=color)
#             await ctx.send(embed=embed)
#         else:
#             await ctx.send("No data available for AMD")
#     except Exception as e:
#         await ctx.send(f"An error occurred: {str(e)}")


# @bot.command()
# async def HD(ctx):
#     try:
#         spy = yf.Ticker("HD")
#         data = spy.history(period="15m")
        
#         if len(data) > 0:
#             daily_open = data["Open"].iloc[0]
#             current_high = data["High"].max()

#             if len(data) >= 2:
#                 previous_price = data["Close"].iloc[-2]
#             else:
#                 previous_price = None

#             if len(data) >= 1:
#                 current_price = data["Close"].iloc[-1]
#             else:
#                 current_price = None

#             description = f"Daily Opening Price: ${daily_open:.2f}\n" \
#                           f"Current High of the Day: ${current_high:.2f}\n"

#             if current_price is not None and previous_price is not None:
#                 if current_price > previous_price:
#                     color = discord.Color.green()
#                     description += f"Current Price (15 min): ${current_price:.2f} (Up from previous)"
#                 elif current_price < previous_price:
#                     color = discord.Color.red()
#                     description += f"Current Price (15 min): ${current_price:.2f} (Down from previous)"
#                 else:
#                     color = discord.Color.orange()
#                     description += f"Current Price (15 min): ${current_price:.2f} (No change)"
#             else:
#                 color = discord.Color.orange()
#                 description += "No data available for current or previous price."

#             embed = discord.Embed(title="HD Stock Information", description=description, color=color)
#             await ctx.send(embed=embed)
#         else:
#             await ctx.send("No data available for HD")
#     except Exception as e:
#         await ctx.send(f"An error occurred: {str(e)}")

# @bot.command()
# async def SBUX(ctx):
#     try:
#         spy = yf.Ticker("SBUX")
#         data = spy.history(period="15m")
        
#         if len(data) > 0:
#             daily_open = data["Open"].iloc[0]
#             current_high = data["High"].max()

#             if len(data) >= 2:
#                 previous_price = data["Close"].iloc[-2]
#             else:
#                 previous_price = None

#             if len(data) >= 1:
#                 current_price = data["Close"].iloc[-1]
#             else:
#                 current_price = None

#             description = f"Daily Opening Price: ${daily_open:.2f}\n" \
#                           f"Current High of the Day: ${current_high:.2f}\n"

#             if current_price is not None and previous_price is not None:
#                 if current_price > previous_price:
#                     color = discord.Color.green()
#                     description += f"Current Price (15 min): ${current_price:.2f} (Up from previous)"
#                 elif current_price < previous_price:
#                     color = discord.Color.red()
#                     description += f"Current Price (15 min): ${current_price:.2f} (Down from previous)"
#                 else:
#                     color = discord.Color.orange()
#                     description += f"Current Price (15 min): ${current_price:.2f} (No change)"
#             else:
#                 color = discord.Color.orange()
#                 description += "No data available for current or previous price."

#             embed = discord.Embed(title="SBUX Stock Information", description=description, color=color)
#             await ctx.send(embed=embed)
#         else:
#             await ctx.send("No data available for SBUX")
#     except Exception as e:
#         await ctx.send(f"An error occurred: {str(e)}")