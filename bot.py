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

username = ""

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
        #update the username for the bot to track
        
        pass # i should have a variable here that changes/stores username
    if message.content.startswith("!latest_game"):
        await message.channel.send(fetch_latest_game("ian175"))
        

def fetch_latest_game(username):
    archive_url = "https://api.chess.com/pub/player/"+username+"/games/archives" #grabs the api of (username)
    data = requests.get(archive_url).json() #save the data from the api into a variable
    #saving as a json means that its saved as a dictionary
    #since the data is split into months so we take the latest month
    latest_month = data["archives"][-1]

    latest_month_data = requests.get(latest_month).json() #samethign with data but with the month this time
    games = latest_month_data["games"]
    if not games: #if i havent played games that month...
        return None #return nothing

    latest_game = games[-1] #take the last game played

    parse_game(latest_game) #parse the game

def parse_game(stuff): #taking the data and converting it to something readable
    game_stream = io.StringIO(stuff.get("pgn","")) #we got a string but chess.pgn library wants it as a sort of file
    game = chess.pgn.read_game(game_stream)
    if game is None:
        return None  # if game doesnt exist... return nothing

    white_player = game.headers.get("White")
    black_player = game.headers.get("Black")
    opening = game.headers.get("ECOUrl")
    result = game.headers.get("Result")

    if str(black_player).lower() == username:
        colour = "black"
        player = black_player
        opponent = white_player
    else:
        colour = "white"
        player = white_player
        opponent = black_player

    return {
        "colour": colour,
        "player": player,
        "opponent": opponent,
        "opening": opening,
        "result": result
    }


TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not TOKEN:
    raise ValueError("No token provided. Please set the DISCORD_BOT_TOKEN environment variable")
bot.run(TOKEN)