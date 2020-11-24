import os
import random
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds,name=GUILD)

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
    # print(guild.members)

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    lols = [
        "Arjun is a pet dog that bites all strangers",
        "Aditi is a very very boring cousin",
        "Chintu is a field marshal and a war hero",
        "Amogh is a douchebag and always says 'hurts man'",
        "Arya is my master",
    ]
    if message.content.lower() == 'arjun':
        response = lols[0]
        await message.channel.send(response)
    if message.content.lower() == 'chintu':
        response = lols[2]
        await message.channel.send(response)
    if message.content.lower() =='aditi':
        response = lols[1]
        await message.channel.send(response)
    if message.content.lower() == 'amogh':
        response = lols[3]
        await message.channel.send(response)
    if message.content.lower() == 'arya':
        response = lols[4]
        await message.channel.send(response)
client.run(TOKEN)