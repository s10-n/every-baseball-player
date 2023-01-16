hank_aaron = {
    "nameFirst": "Hank",
    "nameLast": "Aaron",
    "bbrefID": "aaronha01"
    }

def create_url(player):
    player_id = player["bbrefID"]
    initial = player_id[0]    
    return f"""https://www.baseball-reference.com/players/{initial}/{player_id}.shtml"""
    
print(create_url(hank_aaron))
