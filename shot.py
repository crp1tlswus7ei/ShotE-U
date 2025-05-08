import os
import asyncio
import discord
from pymongo import MongoClient
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix = '' ,intents = intents)
token = os.getenv('CORE_TOKEN')

async def connect_():
   mongo_uri = os.getenv('MONGO_URI')
   shot = MongoClient(mongo_uri)

   try:
      await shot.admin.command('ping')
      print('db connect.')
   except Exception as e:
      print(f'Error: {e}')

async def load():
   for filename in os.listdir('./slash'):
      if filename.endswith('.py'):
         await bot.load_extension(f'slash.{filename[:-3]}')

@bot.event
async def on_ready():
   print('Status: Online')
   try:
      synced_commands = await bot.tree.sync()
      print(f'Synced {len(synced_commands)} commands.')
   except Exception as e:
      print(f'Error: {e}')

async def main():
   async with bot:
      await load()
      await bot.start(token)

asyncio.run(main())