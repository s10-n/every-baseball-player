import csv
import random
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re
import tweepy
import constants

# Functions

# create_player_list()
# opens the CSV of players and returns a list object containing each player
 
def create_player_list():
    with open('People.csv','r') as players:
        player_reader = csv.reader(players)
        print("Player list created successfully")
        return list(player_reader)

# select_player_from_list()
# takes in a list object of players, selects a random player form the list,
# and returns that player's information

def select_player_from_list(player_list): 
    number_of_players = len(player_list)
    player_index = random.randrange(number_of_players)
    print(f"Player #{player_index} selected")
    return player_list[player_index]

# get_baseball_reference_data()
# takes in a baseball-reference.com URL and returns a BS4 object of the page

def get_baseball_reference_data(url):
    r = requests.get(url)
    print(r)
    soup = BeautifulSoup(r.content, "html.parser")
    return soup

# get_image()
# takes in a BS4 object, scrapes the page for the player's main image,
# then downloads the image. Returns the image URL

def get_image(soup):
    if soup.find("div", class_="media-item"):
        img_container = soup.find("div", class_="media-item")
        img_element = img_container.select_one("img")
        img_url = img_element.get("src")
        download_image(img_url)
        print(f"Player image: {img_url}")
    else:
        img_url = ""
        print("No image")
    return img_url

# download_image()
# takes in an image url and downloads it to the working directory

def download_image(img_url):
    image_file = requests.get(img_url)
    open('image.jpg', 'wb').write(image_file.content)

# get_position()
# takes in a BS4 object, scrapes the page for the player's position(s),
# and returns the position(s) as a string

def get_position(soup):
    infobox = soup.find("div", id="meta")
    position =""
    paragraphs = infobox.find_all("p")
    for i in range(len(paragraphs)):
        element = paragraphs[i].get_text()
        if "Position" in element:
            position = element
    position = re.sub(":\s*",": ",position)
    position = re.sub("\s{2,}|\n","",position)
    return position

# get_player_info()
# takes in a single item from the player list and returns a dictionary
# that includes all of the important information from the tweet

def get_player_info(player):
    player = {"given_name": player[13],
              "surname": player[14],
              "birth_year": player[1],
              "birth_month": datetime.strptime(player[2],"%m").strftime("%B"),
              "birth_day": player[3],
              "bbrefID": player[-1],
              "url": f"https://www.baseball-reference.com/players/{player[-1][0]}/{player[-1]}.shtml"}
    print(f"Player data: {player}")
    player_soup = get_baseball_reference_data(player["url"])
    player["img_url"] = get_image(player_soup)
    player["position"] = get_position(player_soup)
    return player

# TODO: post the player to twitter

def print_player_info(player):
    return f"\n{player['given_name']} {player['surname']}\nBorn {player['birth_month']} {player['birth_day']}, {player['birth_year']}\n{player['position']}"


player_list = create_player_list()

player_index = select_player_from_list(player_list)

player = get_player_info(player_index)

tweet = print_player_info(player)

print(tweet)


auth = tweepy.OAuth1UserHandler(
  constants.api_key, constants.api_secret,
   constants.access_token, constants.access_secret
)
api = tweepy.API(auth)

media = api.chunked_upload("image.jpg")
print(api.update_status(status=tweet, media_ids=[media.media_id_string]))

