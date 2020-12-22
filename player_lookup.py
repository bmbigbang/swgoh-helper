from initialise_data_structures import *
from api_swgoh_help import api_swgoh_help, settings
from dictdiffer import diff

data_lookups = initialise_data_structures()
# gl ults
#[(i, j) for i,j in data_lookups["abilities"].items() if "ultimate" in i.lower()]
#[('ultimateability_supremeleaderkyloren', 'Depths of Rage'), ('ultimateability_glrey', 'Heir to the Jedi'), ('ultimateability_sithpalpatine', 'I Am All The Sith'), ('ultimateability_grandmasterluke', 'Heroic Stand')]
# [(i, j['thumbnailName'], j) for i,j in data_lookups["toons"].items() if j["nameKey"] == "Rey"]
# 'tex.charui_rey_tros'

env_data = get_env()
# Change the settings below
creds = settings(env_data["username"], env_data["password"])
client = api_swgoh_help(creds)

# should be any player's allycode
allycodes = [694845774]
players_response = client.fetchPlayers(allycodes)

# ability_response = client.fetchData({
#     "collection": "skillList",
#     "allycodes": allycodes,
#     "language": "eng_us",
#     "enums": True,
# })

payload = {
    "allycodes": allycodes,
    'collection': "unitsList",
    'language': "eng_us",
    'enums': True,
    'match': {
        "rarity": 7,
        "obtainable": True,
        "obtainableTime": 0
    }
}
units = client.fetchData(payload)
new_units = {}
for unit in units:
    new_units[unit['baseId']] = unit

print(diff(
    [j for i,j in data_lookups["toons"].items() if j["nameKey"] == "Rey"][0],
    [j for i,j in new_units.items() if j["nameKey"] == "Rey"][0]
))
a = diff(
    [j for i,j in data_lookups["toons"].items() if j["nameKey"] == "Rey"][0],
    [j for i,j in new_units.items() if j["nameKey"] == "Rey"][0]
)

####
# person lookup
allycodes = [591695128, 649421954]
players_response = client.fetchPlayers(allycodes)

a = diff(
    [i for i in players_response[0]["roster"] if i["nameKey"] == "Rey"][0],
    [i for i in players_response[1]["roster"] if i["nameKey"] == "Rey"][0],
)

payload = {
    'collection': "unitsList",
    'language': "eng_us",
    "enums": False,
    "match": {
        "_id": '6rFLGzvmRW-ios1qZUwPIg'
    }
}
t = client.fetchData(payload)

t = client.fetchUnits(allycodes)
a = diff(
    t["GLREY"][0],
    t["GLREY"][1],
)

t = client.fetchAPI(client.endpoints["roster"], { "allycodes": allycodes, "enum": False })
a = diff(
    t[0]["GLREY"],
    t[1]["GLREY"]
)
