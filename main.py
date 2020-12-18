#!/usr/bin/env python3

from api_swgoh_help import api_swgoh_help, settings
from texttable import Texttable
from env import get_env

env_data = get_env()
# Change the settings below
creds = settings(env_data.username, env_data.password)
client = api_swgoh_help(creds)

# should be any player's allycode in the guild
allycodes = [env_data.allycode]
guild_response = client.fetchGuilds(allycodes)

guild_allycodes = [i["allyCode"] for i in guild_response[0]["roster"]]

players = client.fetchPlayers(guild_allycodes)

GLdict = {
    "Supreme Leader Kylo Ren": [],
    "Rey": [],
    "Jedi Knight Luke Skywalker": [],
    "Sith Eternal Emperor": [],
    "Jedi Master Luke Skywalker": [],
    "Wat Tambor": [],
    "Darth Vader": []
}

for player in players:
    # print(player["name"])
    for character in player["roster"]:
        if character["nameKey"] in GLdict:
            # ult = [i for i in character["skills"] if i["nameKey"] in ["Depths of Rage", "Heir to the Jedi"]]
            GLdict[character["nameKey"]].append({
                "name": player["name"],
                "allyCode": player["allyCode"],
                "gear": character["gear"],
                "relic": character["relic"],
                # "ult": ult
            })

import pprint
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(GLdict)

table = Texttable()
table.set_cols_align(["l", "r", "r"])
table.set_cols_valign(["m", "m", "m"])
rows = [["Character", "Count", "At Gear 13+"]]

for name, GLs in GLdict.items():
    rows.append([name, len(GLs), sum([1 for i in GLs if i["gear"] >= 13])])
    # print(name, ":", len(GLs), " at gear 13+:", sum([1 for i in GLs if i["gear"] >= 13]))

table.add_rows(rows)
print(table.draw())


