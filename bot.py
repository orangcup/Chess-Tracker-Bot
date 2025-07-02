import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

import requests
import chess.pgn
import io

load_dotenv()

intents = discord.Intents.default() # make a default intents object
intents.message_content = True # Enable message content intent

bot = discord.Client(intents=intents) # make the bot client

@bot.event
async def on_ready(): #when bot is loaded
    print(f'Logged in as {bot.user}') #it should say so in console

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('!hello'):
        await message.channel.send('Hello! I am your Chess Tracker Bot!')
    if bot.user in message.mentions: # if the bot is mentioned...
        pass #will update
    if message.content.startswith("!update_username"):
        


TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not TOKEN:
    raise ValueError("No token provided. Please set the DISCORD_BOT_TOKEN environment variable")
bot.run(TOKEN)