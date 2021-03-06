import json
import os
from api_swgoh_help import api_swgoh_help, settings
from env import get_env
from initialise_data_structures import initialise_data_structures
from texttable import Texttable
from data_lookups import mod_set_stats, mod_slots, unit_stats, primary_stat_names_map

saved_data = initialise_data_structures()


def add_stat(stats, stat_name, value, upgrade_tier):
    if stat_name in stats:
        stats[stat_name].append([value, upgrade_tier])
    else:
        stats[stat_name] = [[value, upgrade_tier]]


def get_mods(allycode=0, force_reload=False, unit_exclusions=None, unit_inclusions=None):

    env_data = get_env()
    if allycode == 0:
        allycode = env_data["allycode"]

    saved_mods = {}
    if not force_reload and os.path.isfile('saved-mods.json'):
        with open('saved-mods.json', 'r', encoding='utf-8') as f:
            saved_mods = json.load(f)
        if allycode in saved_mods:
            return saved_mods[allycode]

    # Change the settings below
    creds = settings(env_data["username"], env_data["password"])
    client = api_swgoh_help(creds)

    players_response = client.fetchRoster([allycode], enums=False)

    units_without_mods = {}
    units_upgradable_mods = {}
    stats = {}
    mods = {}
    chars = {}
    char_name_map = {}
    for unit_id, unit_array in players_response[0].items():
        unit = unit_array[0]
        if unit_exclusions and saved_data["toons"][unit_id]["nameKey"] in unit_exclusions:
            continue
        if unit_inclusions and saved_data["toons"][unit_id]["nameKey"] in unit_exclusions not in unit_inclusions:
            continue
        if unit["level"] < 50:
            continue
        chars[unit_id] = {
            "char_name": saved_data["toons"][unit_id]["nameKey"],
            "starLevel": unit["starLevel"],
            "level": unit["level"],
            "mods": []
        }
        char_name_map[saved_data["toons"][unit_id]["nameKey"]] = unit_id

        for x in range(len(unit["mods"])):
            mod = unit["mods"][x]
            mod_slot = mod_slots[x]
            if "id" not in mod:
                if unit["type"] == 1:
                    unit_without_mod = units_without_mods.get(unit_id, [])
                    unit_without_mod.append(mod_slot)
                    units_without_mods[unit_id] = unit_without_mod
                continue
            chars[unit_id]["mods"].append(mod["id"])

            mod_stats = {}
            mods[mod["id"]] = {
                "set": mod_set_stats[mod["set"]],
                "slot": mod_slot,
                "stats": mod_stats,
                "primary": primary_stat_names_map[mod["stat"][0][0]],
                "char_name": saved_data["toons"][unit_id]["nameKey"]
            }
            for i in range(5):
                if i > len(mod["stat"]) - 1:
                    print(unit_id, "appears to not have the correct amount of mod slots")
                    break
                else:
                    if mod["stat"][i][0] == 0:
                        upgradable_mods = units_upgradable_mods.get(unit_id, [])
                        upgradable_mods.append(mod_slot)
                        units_upgradable_mods[unit_id] = upgradable_mods
                        name = unit_stats[0]
                        mod_stats[name] = 0
                    else:
                        name = unit_stats[mod["stat"][i][0]]
                        mod_stats[name] = mod["stat"][i][1]
                        add_stat(stats, name, mod["stat"][i][1], mod["stat"][i][2])

    table = Texttable()
    table.set_cols_align(["l", "l", "l"])
    table.set_cols_valign(["m", "m", "m"])
    rows = [["Character", "Missing Mods", "Upgradable Mods"]]

    table_units = set(units_without_mods.keys())
    table_units.update(set(units_upgradable_mods.keys()))
    for unit_id in table_units:
        rows.append([
            saved_data["toons"][unit_id]["nameKey"],
            ", ".join(units_without_mods.get(unit_id, [])),
            ", ".join(units_upgradable_mods.get(unit_id, []))
        ])

    table.add_rows(rows)
    print(table.draw())

    # save data
    saved_mods[allycode] = {"mods": mods, "stats": stats, "chars": chars, "char_name_map": char_name_map}
    with open('saved-mods.json', 'w', encoding='utf-8') as f:
        json.dump(saved_mods, f, ensure_ascii=False, indent=4)
    return saved_mods[allycode]

# run with force reload to update cache of stored data
all_units = [j["nameKey"] for j in saved_data["toons"].values()]
exclusions = []
get_mods(force_reload=True, unit_exclusions=exclusions, unit_inclusions=all_units)
