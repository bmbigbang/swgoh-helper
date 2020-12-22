import json
import os
from api_swgoh_help import api_swgoh_help, settings
from env import get_env

mod_set_stats = {
    1: {
        "name": "Health",
        "setCount": 2,
        "stat": ["UNITSTATMAXHEALTHPERCENTADDITIVE", 10]
    },
    2: {
        "name": "Offence",
        "setCount": 4,
        "stat": ["UNITSTATOFFENSEPERCENTADDITIVE", 15]
    },
    3: {
        "name": "Defense",
        "setCount": 2,
        "stat": ["UNITSTATDEFENSEPERCENTADDITIVE", 25]
    },
    4: {
        "name": "Speed",
        "setCount": 4,
        "stat": ["UNITSTATSPEEDPERCENTADDITIVE", 10]
    },
    5: {
        "name": "Crit Chance",
        "setCount": 2,
        "stat": ["UNITSTATCRITICALCHANCEPERCENTADDITIVE", 8]
    },
    6: {
        "name": "Crit Damage",
        "setCount": 4,
        "stat": ["UNITSTATCRITICALDAMAGE", 30]
    },
    7: {
        "name": "Potency",
        "setCount": 2,
        "stat": ["UNITSTATACCURACY", 15]
    },
    8: {
        "name": "Tenacity",
        "setCount": 2,
        "stat": ["UNITSTATRESISTANCE", 20]
    },
}

mod_slots = {
    0: "Square",
    1: "Arrow",
    2: "Diamond",
    3: "Triangle",
    4: "Circle",
    5: "Cross"
}

def get_mods(allycode=0, force_reload=False):
    env_data = get_env()
    if allycode == 0:
        allycode = env_data["allycode"]

    saved_mods = {}
    if not force_reload and os.path.isfile('saved-mods.json'):
        with open('saved-data.json', 'r', encoding='utf-8') as f:
            saved_mods = json.load(f)
        if allycode in saved_mods:
            return saved_mods[allycode]


    # Change the settings below
    creds = settings(env_data["username"], env_data["password"])
    client = api_swgoh_help(creds)

    players_response = client.fetchRoster([allycode])

    stats = {}
    mods = {}

    def add_stat(stat_name, value, upgrade_tier):
        if stat_name in stats:
            stats[stat_name].append([value, upgrade_tier])
        else:
            stats[stat_name] = [[value, upgrade_tier]]

    for unit_id, unit_array in players_response[0].items():
        unit = unit_array[0]
        for x in range(len(unit["mods"])):
            mod = unit["mods"][x]
            if "id" not in mod:
                continue
            mod_stats = {}
            mods[mod["id"]] = {
                "set": mod_set_stats[mod["set"]],
                "slot": mod_slots[x],
                "stats": mod_stats
            }
            for i in range(5):
                if i > len(mod["stat"]) - 1:
                    print(unit_id)
                    name = "NOSTAT{0}".format(i)
                    mod_stats[name] = 0
                    add_stat(name, 0, 0)
                else:
                    if mod["stat"][i][0] == 0:
                        name = "NOSTAT{0}".format(i)
                        mod_stats[name] = 0
                        add_stat(name, 0, 0)
                    else:
                        mod_stats[mod["stat"][i][0]] = mod["stat"][i][1]
                        add_stat(*mod["stat"][i])


    # save data
    saved_mods[allycode] = { "mods": mods, "stats": stats }
    with open('saved-mods.json', 'w', encoding='utf-8') as f:
        json.dump(saved_mods, f, ensure_ascii=False, indent=4)
    return saved_mods[allycode]

# run with force reload to update cache of stored data
# get_mods(force_reload=True)