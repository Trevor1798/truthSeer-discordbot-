import discord
from discord.ext import commands
import os
import asyncio

bot_token = os.environ.get("BOT_TOKEN")
bot = commands.Bot(command_prefix="!")

# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f"Bot is ready logged in as {bot.user.name}")

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
    await asyncio.sleep(5)  # Wait for 5 seconds
    await ctx.send("Nothing...")
    await asyncio.sleep(10)  # Wait for another 10 seconds
    await ctx.send("Just hanging around")

@bot.command()
async def Jay(ctx):
    await ctx.send("Jay is a remarkable individual who embodies the qualities of a true sigma and an alpha male. With his strong presence and charismatic aura, he effortlessly commands respect and admiration from those around him. Jay possesses a unique blend of confidence, independence, and intelligence, making him a natural leader in any situation. His unwavering determination and self-assuredness enable him to navigate life's challenges with ease and grace. Jay's calm and collected demeanor coupled with his sharp wit and keen intellect make him an engaging conversationalist and a trusted friend. His unwavering commitment to personal growth and his ability to stay true to his values are truly inspiring. Jay's magnetic personality and unparalleled charisma make him a true alpha male, leaving a lasting impact on everyone fortunate enough to know him.")

@bot.command()
async def Frank(ctx):
    await ctx.send("Frank is an exceptional individual who has left an indelible mark on the world of esports as a legendary two-time champion. With his extraordinary skills, dedication, and strategic prowess, he has etched his name in the annals of competitive gaming history. Frank's unparalleled talent and relentless drive propelled him to the pinnacle of success, where he claimed victory in not just one, but two significant esports championships. His mastery of the game, combined with his strategic thinking and quick reflexes, allowed him to outshine his opponents and lead his team to triumph. As a retired champion, Frank's legacy lives on, serving as an inspiration for aspiring gamers and a testament to the heights that can be reached through unwavering determination and passion. Beyond his competitive achievements, Frank's humble nature and sportsmanship have endeared him to fans and fellow gamers alike. He remains a respected figure in the esports community, and his impact will be remembered for years to come.")

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
async def help(ctx):
    help_message = "Here are the available commands:\n"
    help_message += "!hello - Greet the bot\n"
    help_message += "!whatareyoudoing - Check what the bot is doing\n"
    help_message += "!whatsup - Check what the bot is up to\n"
    help_message += "!Jay - Learn about Jay, a remarkable individual who embodies the qualities of a true sigma and an alpha male\n"
    help_message += "!Frank - Discover more about Frank, a legendary two-time esports champion who has retired\n"
    help_message += "!Vam - Explore the accomplishments of Vam, the best options trader and osu player of all time\n"
    help_message += "!Chris - Learn about Chris, a hilarious storyteller, anime and OG games expert, and future goated programmer\n"
    help_message += "!Trev - Discover the indescribable essence of Trev, a person who defies conventional descriptions\n"
    help_message += "!help - Display this help message"

    await ctx.send(help_message)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower().startswith("hi"):
        await message.channel.send("Hello!")

    await bot.process_commands(message)

bot.run(bot_token)
