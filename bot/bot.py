import os
import random
import discord
import selenium
import bs4
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!',intents=intents)

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds,name=GUILD)

    print(
        f'{bot.user.name} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
    # print(guild.members)

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    lols = [
        "Arjun is a barking and irritating dog that bites everyone",
        "Aditi is still a very very boring cousin",
        "Chintu is a tenth grader unhappy with school but tops everything anyways",
        "Amogh is a douchebag and always says 'hurts man', 'STFU', etc",
        "Arya is my master",
        "At your service.",
    ]
    # Dictionary storing personalised message indices
    d = {
        "arjun":0,
        "chintu":2,
        "aditi":1,
        "amogh":3,
        "arya":4,
        "jarvis":5,
    }
    response = lols[d[message.content.lower()]]
    await message.channel.send(response)

URL = 'https://www.brainyquote.com/topics/inspirational-quotes'
page = requests.get(URL)
soup = BeautifulSoup(page.content,'html.parser')
results = soup.find(id='quotesList')
quotes = results.find_all('a',class_='b-qt')
quoteslist = []
for quote in quotes:
    quoteslist.append(quote.text)
    # print(quote.text)
# print(len(quoteslist))
bot = commands.Bot(command_prefix='!',intents=intents)

@bot.command(name='inspiration',help='Responds with an inspirational quote when asked')
async def inspiration(ctx):
    response = random.choice(quoteslist)
    await ctx.send(response)

URL1 = 'https://www.brainyquote.com/topics/motivational-quotes'
page = requests.get(URL1)
soup = BeautifulSoup(page.content,'html.parser')
results = soup.find(id='quotesList')
quotes = results.find_all('a',class_='b-qt')
quoteslist1 = []
for quote in quotes:
    quoteslist1.append(quote.text)
    # print(quote.text)
# print(len(quoteslist1))
bot = commands.Bot(command_prefix='!',intents=intents)

@bot.command(name='motivation',help='Responds with a motivational quote when asked')
async def motivation(ctx):
    response = random.choice(quoteslist1)
    await ctx.send(response)
    


@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log','a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise
# client.run(TOKEN)
bot.run(TOKEN)