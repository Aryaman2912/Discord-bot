import os
import sys
import random
import discord
import selenium
import bs4
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from discord.ext import commands
from discord.ext.commands import has_permissions,CheckFailure,BadArgument
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
# client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!',intents=intents)


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

# Fetch inspiration quotes 
URL = 'https://www.brainyquote.com/topics/inspirational-quotes'
page = requests.get(URL)
soup = BeautifulSoup(page.content,'html.parser')
results = soup.find(id='quotesList')
quotes = results.find_all('a',class_='b-qt')
inspiration_list = []
for quote in quotes:
    inspiration_list.append(quote.text)

# Fetch motivational quotes
URL1 = 'https://www.brainyquote.com/topics/motivational-quotes'
page = requests.get(URL1)
soup = BeautifulSoup(page.content,'html.parser')
results = soup.find(id='quotesList')
quotes = results.find_all('a',class_='b-qt')
motivation_list = []
for quote in quotes:
    motivation_list.append(quote.text)

# Fetch attitude quotes 
URL = 'https://www.brainyquote.com/topics/attitude-quotes'
page = requests.get(URL)
soup = BeautifulSoup(page.content,'html.parser')
results = soup.find(id='quotesList')
quotes = results.find_all('a',class_='b-qt')
attitude_list = []
for quote in quotes:
    attitude_list.append(quote.text)

# Respond to '!inspiration' command
@bot.command(name='inspiration',help='Responds with an inspirational quote')
async def inspiration(ctx):
    response = random.choice(inspiration_list)
    await ctx.send(response)

# Respond to '!motivation' command
@bot.command(name='motivation',help='Responds with a motivational quote')
async def motivation(ctx):
    response = random.choice(motivation_list)
    await ctx.send(response)
    
# Respond to '!attitude' command
@bot.command(name='attitude',help='Responds with a quote about attitude')
async def attitude(ctx):
    response = random.choice(attitude_list)
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
    try:
        if isinstance(error,commands.errors.BadArgument):
            print("Here1")
            await ctx.send("Invalid username")
        elif isinstance(error,commands.errors.MissingPermissions):
            print("Here2")
            await ctx.send("You do not have the correct permissions for this command")
    except:
        print("Here4")
        print(sys.exc_info())
        await ctx.send(sys.exc_info())

# Error handling
@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log','a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise
bot.run(TOKEN)