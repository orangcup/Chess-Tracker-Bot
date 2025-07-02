import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()


intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')


TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not TOKEN:
    raise ValueError("No token provided. Please set the DISCORD_BOT_TOKEN environment variable.")
bot.run(TOKEN)