import csv
import random

# open a database of players

def create_player_list():
    with open('People.csv','r') as players:
        player_reader = csv.reader(players)
        return list(player_reader)
    
# select a random player from that database

def select_player_from_list(player_list):
    number_of_players = len(player_list)
    player_index = random.randrange(number_of_players)
    return player_list[player_index]

def get_player_info(player):
    player = {"given_name": player[13],
              "surname": player[14],
              "birth_year": player[1],
              "birth_month": player[2],
              "birth_day": player[3],
              "bbrefID": player[-1],
              "url": f"https://www.baseball-reference.com/players/{player[-1][0]}/{player[-1]}.shtml"}
    return f"{player['given_name']} {player['surname']}\nBorn: {player['birth_month']} {player['birth_day']}, {player['birth_year']}\n{player['url']}"

# scrape baseball reference for that player's name, positions, date of birth, and photo

def create_url(player):
       
    return 

# TODO: post the player to twitter


player_list = create_player_list()

player = select_player_from_list(player_list)

print(get_player_info(player))
