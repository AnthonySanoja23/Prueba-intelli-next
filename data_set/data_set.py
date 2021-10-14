import requests
import json


players = "https://www.easports.com/fifa/ultimate-team/api/fut/item?page=1/items"
keys_players = ["name","position"]

insert = lambda _dict, obj, pos: {k: v for k, v in (list(_dict.items())[:pos] + list(obj.items()) + list(_dict.items())[pos:])}

def get_players_api():
    response = requests.get(players)

    if response.status_code == 200 :
        Items_response = response.json()
        return clear_players_api(Items_response["items"])

def clear_players_api(players):
    all_players = []

    for idx,player in enumerate(players):
        player_clear = {key_player:player[key_player] for key_player in keys_players}
        player_clear["nationality"]=player["nation"]["name"]
        player_clear["team"]=player["club"]["name"]
        
        if not in_dictlist("name",player["name"],all_players):
            player_with_id = insert(player_clear,{'id':idx},0)
            all_players.append(player_with_id)

    return all_players

def in_dictlist(key, value, my_dictlist):
    for entry in my_dictlist:
        if entry[key] == value:
            return True
    return False



