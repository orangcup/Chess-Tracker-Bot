import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

import requests
import chess.pgn
import io

from chessdotcom import Client, ChessDotComClient, get_player_stats, get_player_game_archives

load_dotenv()

intents = discord.Intents.default() # make a default intents object
intents.message_content = True # Enable message content intent
discord_bot = commands.Bot(command_prefix='!', intents=intents) # lets me use / commands and stuff like !commands 

headers = {
    'User-Agent' : 'Game Tracker Bot'
}
client = ChessDotComClient(user_agent = "My Python Application... (username: ian175; contact: iansun768@gmail.com)") # client that interacts with the api

username = "ian175"

@discord_bot.event
async def on_ready(): #when bot is loaded
    await discord_bot.tree.sync() #lets /commands work
    print(f'Logged in as {discord_bot.user}') #it should say so in console

@discord_bot.tree.command(name='ping', description='Replies with Pong!') # slash command
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'🏓Pong!\n```Latency: {discord_bot.latency * 1000:.0f} ms```')
@discord_bot.event
async def on_message(message):
    if message.author == discord_bot.user:
        return
    if message.content.startswith('!hello'):
        await message.channel.send('Hello! I am your Chess Tracker Bot!')
    if discord_bot.user in message.mentions: # if the bot is mentioned...
        pass #will update
    if message.content.startswith("!update_username"):
        #update the username for the bot to track
        
        pass # i should have a variable here that changes/stores username
    if message.content.startswith("!latest_game"):
        await message.channel.send(parse_game(get_latest_game("ian175")))
        

def get_latest_game(username):
    response = client.get_player_game_archives(username)
    archive_url = response.json['archives'][-1] #latest month archive
    games = requests.get(archive_url, headers=headers).json() #gaems from latest month
    game_data = games['games'][-1] #latest game 
    return game_data

def parse_game(game_data): #taking the data and converting it to something readable
    pgn_str = game_data['pgn']
    pgn_list = pgn_str.split('\n')
    pgn_list = [pgn for pgn in pgn_list if pgn.strip() != ""]
    game_dict = {}
    for i in range(0,21):
        entry = pgn_list[i].replace('[',"").replace(']',"").replace('"',"")
        key, value = entry.split(" ",1)
        game_dict[key] = value
    
    game_dict['url'] = game_data['url']
    game_dict['time_comtrol'] = game_data['time_control']
    game_dict['rated'] = game_data['rated']
    game_dict['initial_setup'] = game_data['initial_setup']
    game_dict['rules'] = game_data['rules']
    game_dict['white'] = game_data['white']
    game_dict['black'] = game_data['black']
    
    return game_dict
    


DISCORD_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not DISCORD_TOKEN:
    raise ValueError("No token provided. Please set the DISCORD_BOT_TOKEN environment variable")
discord_bot.run(DISCORD_TOKEN)