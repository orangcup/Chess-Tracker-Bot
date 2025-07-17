import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv

import requests
import chess.pgn
import io
import json

from chessdotcom import Client, ChessDotComClient, get_player_stats, get_player_game_archives

load_dotenv()

intents = discord.Intents.default() # make a default intents object
intents.message_content = True # Enable message content intent
discord_bot = commands.Bot(command_prefix='!', intents=intents) # lets me use / commands and stuff like !commands 

headers = {
    'User-Agent' : 'Game Tracker Bot'
}
client = ChessDotComClient(user_agent = "My Python Application... ") # client that interacts with the api

#there should be a username system for the bot to track accounts accross servers
USERS_FILE = 'users.json'
def load_users():
    try:
        with open(USERS_FILE, 'r') as f: #load users
            content = f.read().strip()
            if not content:  # if the file is empty, return an empty dictionary
                return {}
            return json.loads(content)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Error decoding JSON from users file. Returning empty dictionary.")
        return {}
def save_data(data):
    with open(USERS_FILE, 'w') as f:
        json.dump(data, f, indent=4) 

@discord_bot.event
async def on_ready(): #when bot is loaded
    await discord_bot.tree.sync() #lets /commands work
    check_for_game.start() #start the loop to check for new games
    print(f'Logged in as {discord_bot.user}') #it should say so in console

@discord_bot.tree.command(name='ping', description='Replies with Pong!') # slash command
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'🏓Pong!\n```Latency: {discord_bot.latency * 1000:.0f} ms```')

class MyView(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    @discord.ui.button(label="Latest Game", style=discord.ButtonStyle.primary) 
    async def Latest_Game(self, interaction, button):
        data = load_users()
        channel_id = str(interaction.channel.id)

        if channel_id not in data:
            await interaction.response.send_message("No username set for this channel. Please set a username using !update_user <username>.",ephemeral=True)  # makes message visible only to the user clicking
            return
        username = data[channel_id]['username']
        await interaction.response.send_message(str_game_results(parse_game(get_latest_game(username)))) # Send a message when the button is clicked

@discord_bot.tree.command()
async def button(ctx):
    await ctx.response.send_message("Click here to check out your latest game!", view=MyView())

@discord_bot.command(name='update_user', description="Updates the username of the chess.com account you're tracking")
async def update_user(ctx, username: str):
            data = load_users() 
            channel_id = str(ctx.channel.id)
            data[channel_id] = {
                'username': username,
                "last_game_url": ""
            }
            save_data(data)
            await ctx.send(f"Username updated to {username} for this channel.")

@discord_bot.event
async def on_message(message):
    if message.author == discord_bot.user:
        return
    if message.content.startswith('!hello'):
        await message.channel.send('Hello! I am your Chess Tracker Bot!')
    if discord_bot.user in message.mentions: # if the bot is mentioned...
        pass #will update
    if message.content.startswith("!latest_game"):
        data = load_users()
        channel_id = str(message.channel.id)

        if channel_id not in data:
            await message.channel.send("No username set for this channel. Please set a username using !update_user <username>.")
            return
        username = data[channel_id]['username']

        await message.channel.send(str_game_results(parse_game(get_latest_game(username))))
    await discord_bot.process_commands(message)

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

def str_game_results(dict):
    str = dict["White"] + " " + dict["Result"] + " " + dict["Black"] + "\n" + dict["Termination"] + "\n" + dict["ECOUrl"]
    return str


#i want this bot to check the chess.com api every minute for new games
@tasks.loop(minutes=1)
async def check_for_game():
    print("hi")
    data = load_users()
    for channel_id, info in data.items():
        username = info['username']
        last_url = info['last_game_url']
        try:
            game_dict = parse_game(get_latest_game(username))
            new_game_url = game_dict['url']
        except Exception as e:
            print(f"Error fetching game for {username}: {e}")
            continue

        if new_game_url != last_url:
            channel = discord_bot.get_channel(int(channel_id))
            if channel:
                await channel.send("Click here to check out your latest game!", view=MyView())
                data[channel_id]['last_game_url'] = new_game_url
                save_data(data)



DISCORD_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not DISCORD_TOKEN:
    raise ValueError("No token provided. Please set the DISCORD_BOT_TOKEN environment variable")
discord_bot.run(DISCORD_TOKEN)