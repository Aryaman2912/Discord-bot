import os
import sys
import random
import discord
import selenium
import bs4
import requests
import imdb
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from discord.ext import commands
from discord.ext.commands import has_permissions,CheckFailure,BadArgument
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
# client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!',intents=intents,help_command=None)


# Print members to stdout when connected
@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds,name=GUILD)

    print(
        f'{bot.user.name} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

# Send a dm to a new joiner
@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )
    await bot.process_commands(member)


# Respond to specific messages on the server
@bot.listen('on_message')
async def on_message(message):
    if message.author == bot.user:
        return
    response = "At your service."
    if message.content.lower() == 'jarvis':
        await message.channel.send(response)

# Give quote on requested topic
@bot.command(name='quote',help='give a quote on a requested topic')
async def quote(ctx,topic=''):
    URL = 'https://www.brainyquote.com/topics/'+topic+'-quotes'
    page = requests.get(URL)
    if page.status_code == 404:
        await ctx.send("Enter a valid topic you nitwit. Stupid people smh")
    else:
        soup = BeautifulSoup(page.content,'html.parser')
        results = soup.find(id='quotesList')
        quotes = results.find_all('a',class_='b-qt')
        if quotes == None:
            await ctx.send("Nothing available")
        else:
            quotes_list = []
            for quote in quotes:
                quotes_list.append(quote.text)
            response = random.choice(quotes_list)
            await ctx.send(response)

# Create new channel
@bot.command(name='create-channel',help='creates a new text channel')
@commands.has_role('admin')
async def create_channel(ctx,channel_name = 'new'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels,name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)

# Give info about a movie
@bot.command(name='movie')
async def movie(ctx,*args):
    movies = " ".join(args[:])
    if movies == None:
        response = 'Enter a movie douchebag\n'
        await ctx.send(response)
    else:
        ia = imdb.IMDb()
        # movies = movies[1:-1]
        print(movies)
        search = ia.search_movie(movies)
        id = search[0].movieID
        information = ia.get_movie(id)
        print(id)
        name = information
        rating = information.data['rating']
        genre = ','.join([genre for genre in information.data['genres']])
        # plot = information.data['plot outline']
        language = information.data['languages'][0]
        response = f'Name:{name}\nRating:{rating}\nGenres:{genre}\nLanguage:{language}\n' 
        await ctx.send(f'```{response}```')
             
# Kick members
@bot.command(pass_context=True,name='kick',help='kick a member')
@commands.has_permissions(kick_members=True)
async def kick(ctx,username: discord.Member):
    if username.guild_permissions.administrator:
        await ctx.send("Target is an admin")
    else:
        await ctx.guild.kick(username)
        await ctx.send(f"Kicked {username}")
@kick.error
async def kick_error(ctx,error):
    if isinstance(error,commands.errors.BadArgument):
        await ctx.send("Invalid username")
    elif isinstance(error,commands.errors.MissingPermissions):
        await ctx.send("You do not have the correct permissions for this command")

# Fetch topics for quotes
URL = 'https://www.brainyquote.com/topics/'
page = requests.get(URL)
soup = BeautifulSoup(page.content,'html.parser')
x = soup.find_all('span',class_='topicContentName')
topics = []
for item in x:
    topics.append(item.text)

# Custom help command
@bot.command(name='help')
async def help(ctx,command=None):
    if command == None:
        response = '```List of available commands:\n\tquote\n\tkick\n\tcreate-channel\n\tmovie```'
        await ctx.send(response)
    if command == 'quote':
        response = '\n'.join([item for item in topics])
        response = '!quote <topic>\n'+'List of available topics are: \n' + response
        await ctx.send(f'```{response}```')
    if command == 'kick':
        response = '!kick <username>'
        await ctx.send(f'```{response}```')
    if command == 'create-channel':
        response = "!create-channel <name>\nDefault name is 'new'"
        await ctx.send(f'```{response}```')
    if command == 'movie':
        response = "!movie <name>\nEnter the name in quotes\nProvides rating,genres and language"
        await ctx.send(f'```{response}```')


# Error handling
@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log','a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise
bot.run(TOKEN)