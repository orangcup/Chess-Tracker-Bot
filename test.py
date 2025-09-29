'''from chessdotcom import get_leaderboards, get_player_stats, get_player_game_archives, Client
import pprint
import requests

Client.request_config['headers']['User-Agent'] = 'test program (contact: iansun768@gmail.com)'

printer = pprint.PrettyPrinter()

def print_leaderboards():
	data = get_leaderboards().json
	categories = data.keys()

	for category in categories:
		print('Category:', category)
		for idx, entry in enumerate(data[category]):
			print(f'Rank: {idx + 1} | Username: {entry["username"]} | Rating: {entry["score"]}')


def get_player_rating(username):
	data = get_player_stats(username).json
	categories = ['chess_blitz', 'chess_rapid', 'chess_bullet']
	for category in categories:
		print('Category:', category)
		print(f'Current: {data[category]["last"]["rating"]}')
		print(f'Best: {data[category]["best"]["rating"]}')
		print(f'Best: {data[category]["record"]}')

def get_most_recent_game(username):
	data = get_player_game_archives(username).json
	url = data['archives'][-1]
	games = requests.get(url).json()
	game = games['games'][-1]
	printer.pprint(game)

get_most_recent_game('timruscica')

'''
import requests
from chessdotcom import ChessDotComClient, get_player_profile, get_player_game_archives

headers = {
    'User-Agent' : 'Game Tracker Bot'
}
client = ChessDotComClient(user_agent = "My Python Application... (username: ian175; contact: iansun768@gmail.com)")

#response = client.get_player_profile("ian175")
response = client.get_player_game_archives("ian175")

'''
response.player.name # 'Fabiano Caruana'
response.player.title # 'GM'
response.player.last_online_datetime # datetime.datetime(2024, 10, 25, 20, 8, 28)
response.player.joined_datetime # datetime.datetime(2013, 3, 17, 15, 14, 32)
# See readthedocs for full documentation of responses
'''

# or access the source

#latest month archive
archive_url = response.json['archives'][-1]
print(response.json['archives'][-1])

games = requests.get(archive_url, headers=headers).json()
game_data = games['games'][-1]
#print(game_data)

pgn_str = game_data['pgn'] #created in the format of a string
pgn_list = pgn_str.split('\n')
# 0 event
# 1 site
# 2 date
# 3 round
# 4 white
# 5 black
# 6 result
# 7 ending position
# 8 timezone
# 9 ECO
# 10 ECO Url
# 11 UTC Date
# 12 UTC Time
# 13 white elo
# 14 black elo
# 15 time control
# 16 termination
# 17 start time
# 18 end date
# 19 end time
# 20 link
# 21 moves

#print(pgn_list)

pgn_list = [pgn for pgn in pgn_list if pgn.strip() != ""]
game_dict = {}
for i in range(0,21):
    entry = pgn_list[i].replace('[',"").replace(']',"").replace('"',"")
    key, value = entry.split(" ",1)
    game_dict[key] = value

game_dict['time_comtrol'] = game_data['time_control']
game_dict['rated'] = game_data['rated']
game_dict['initial_setup'] = game_data['initial_setup']
game_dict['rules'] = game_data['rules']
game_dict['white'] = game_data['white']
game_dict['black'] = game_data['black']

print(game_dict)