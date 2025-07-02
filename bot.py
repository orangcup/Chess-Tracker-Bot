import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default() # Create a default intents object
intents.message_content = True # Enable message content intent

bot = discord.Client(intents=intents) # Create a client instance with the specified intents

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('!hello'):
        await message.channel.send('Hello! I am your Chess Tracker Bot!')


TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not TOKEN:
    raise ValueError("No token provided. Please set the DISCORD_BOT_TOKEN environment variable")
bot.run(TOKEN)