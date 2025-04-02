import os
# import json
import asyncio
import discord
from pymongo import MongoClient
from dotenv import load_dotenv
from discord.ext import commands

# def get_server_prefix(message):
#     with open('prefixes.json', 'r') as c:
#         n_prefix = json.load(c)
#
#     return n_prefix[str(message.guild.id)]

load_dotenv()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix = '?', intents = intents)
token = os.getenv('CORE_TOKEN')

async def connect_():
    mongo_uri = os.getenv('MONGO_URI')
    shot = MongoClient(mongo_uri)
    db = shot["kiko"]
    w_coll = db["warns"] # ?

    try:
        await shot.admin.command('ping')
        print('db connect.')
    except Exception as e:
        print(f'Error: {e}')

@bot.event
async def on_ready():
    print('Logged!')
    try:
        synced_commands = await bot.tree.sync()
        print(f'Synced {len(synced_commands)} commands.')
    except Exception as e:
        print(f'Error: {e}')

async def load():
    for filename in os.listdir('./slash'):
        if filename.endswith('.py'):
            await bot.load_extension(f'slash.{filename[:-3]}')

async def main():
    async with bot:
        await load()
        await bot.start(token)

asyncio.run(main())