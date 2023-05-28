import discord
from discord.ext import commands
import os
import asyncio
import requests




target_channel_id = 1111186051520790550

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

WEATHER_KEY = os.environ.get("API_WEATHER_KEY")
BASE_URL = os.environ.get("WEATHER_API_URL")


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
    help_message = "Here are the available commands:\n"
    help_message += "!hello - Greet the bot\n"
    help_message += "!whatareyoudoing - Check what the bot is doing\n"
    help_message += "!whatsup - Check what the bot is up to\n"
    help_message += "!Jay - Learn about Jay, a remarkable individual who embodies the qualities of a true sigma and an alpha male\n"
    help_message += "!Frank - Discover more about Frank, a legendary two-time esports champion who has retired\n"
    help_message += "!Vam - Explore the accomplishments of Vam, the best options trader and osu player of all time\n"
    help_message += "!Chris - Learn about Chris, a hilarious storyteller, anime and OG games expert, and future goated programmer\n"
    help_message += "!Trev - Discover the indescribable essence of Trev, a person who defies conventional descriptions\n"
    help_message += "!Sam - Learn about Sam, an exceptional individual who is simply the best\n" 
    help_message += "!help - Display this help message"


    await ctx.send(help_message)

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
