import json
import re
from env import get_env
from initialise_data_structures import initialise_data_structures
from openpyxl import load_workbook
from data_lookups import mod_slots
import numpy as np

data_lookups = initialise_data_structures()
env_data = get_env()

allycode = env_data["allycode"]

with open('saved-mods.json', 'r', encoding='utf-8') as f:
    saved_mods = json.load(f)

with open('./swgoh-stat-calc/unit_stat_data.json', 'r', encoding='utf-8') as f:
    unit_stats = json.load(f)

workbook = load_workbook('mod-weights.xlsx')
char_mod_stat_weights = workbook["Char Mod Stat Weights"]

column_stat_map = {
    1: "Speed",
    2: "Offence",
    3: "Crit Chance",
    4: "Crit Damage",
    5: "Health",
    6: "Defence",
    7: "Protection",
    8: "Crit Avoidance",
    9: "Tenacity",
    10: "Potency",
    11: "Accuracy"
}

col_to_mod_stat_map = {
    1: ["Speed", "SpeedPercentAdditive"],
    2: ["Offence", "OffensePercentAdditive"],
    3: ["CriticalChancePercentAdditive"],
    4: ["CriticalDamage"],
    5: ["Health", "MaxHealthPercentAdditive"],
    6: ["Defense", "DefensePercentAdditive"],
    7: ["MaxShield", "MaxShieldPercentAdditive"],
    8: ["CriticalNegateChancePercentAdditive"],
    9: ["Resistance"],
    10: ["Accuracy"],
    11: ["EvasionNegatePercentAdditive"]
}

# primary stats have an unfair advantage in this calc, by letting them normalise from 0
max_mod_values_per_stat = {
    "Speed": 32,
    "SpeedPercentAdditive": 0.1,
    "Offence": 253,
    "OffensePercentAdditive": 0.085,
    "CriticalChancePercentAdditive": 0.2,
    "CriticalDamage": 0.42,
    "Health": 2696,
    "MaxHealthPercentAdditive": 0.16,
    "Defense": 73,
    "DefensePercentAdditive": 0.2,
    "MaxShield": 4607,
    "MaxShieldPercentAdditive": 0.24,
    "CriticalNegateChancePercentAdditive": 0.35,
    "Resistance": 0.35,
    "Accuracy": 0.3,
    "EvasionNegatePercentAdditive": 0.3,
}

char_name_map = {j["char_name"]: i for i, j in saved_mods[allycode]["chars"].items()}


def construct_weights():
    weights = []
    threshold_pattern = re.compile(r"(?P<init>\d+)(\s*,\s*)(?P<threshold>\d+\.?\d*)(\s*,\s*)(?P<final>\d+)")

    count = 2
    for row in char_mod_stat_weights.iter_rows(min_row=2, max_col=12, max_row=1000):

        char_name = row[0].value
        if not char_name:
            print("Empty char name on row {}".format(count))
            break

        char_weights = []
        char_thresholds = []

        for col_idx, stat_name in column_stat_map.items():
            cell = row[col_idx].value
            if not cell:
                char_weights.append(0)
                char_thresholds.append({0: 0})
            elif type(cell) is int:
                char_weights.append(cell)
                char_thresholds.append({0: 0})
            elif cell.startswith("("):
                threshold = threshold_pattern.search(cell)
                if not threshold:
                    print("Could not validate threshold pattern on row {} - {}".format(count, stat_name))
                    char_weights.append(0)
                    char_thresholds.append({0: 0})
                else:
                    char_weights.append(int(threshold.groupdict()["init"]))
                    char_thresholds.append({
                        float(threshold.groupdict()["threshold"]): int(threshold.groupdict()["final"])
                    })

        weights.append({
            "char_name": char_name,
            "weights": np.array(char_weights),
            "thresholds": char_thresholds
        })
        count += 1
    return weights


def find(pred, iterable):
    for element in iterable:
        if pred(element):
            return element
    return None


def scaled_stat_modifiers(stat_name, char_stats):
    percent_modifier = max_mod_values_per_stat.get(stat_name + "PercentAdditive", 1)
    if stat_name == "Offense":
        return 1 / (char_stats["final"]["6"] * percent_modifier)
    elif stat_name == "Health":
        return 1 / (char_stats["final"]["1"] * percent_modifier)
    elif stat_name == "Defense":
        return 2 / ((char_stats["base"]["8"] + char_stats["base"]["9"]) * percent_modifier)
    elif stat_name == "MaxShield":
        return 1 / (char_stats["final"]["28"] * percent_modifier)
    elif stat_name == "SpeedPercentAdditive":
        return 1 / (max_mod_values_per_stat[stat_name] / char_stats["final"]["5"])
    elif stat_name == "Speed":
        return 1 / max_mod_values_per_stat[stat_name]
    else:
        return 0.01 / max_mod_values_per_stat[stat_name]


def restructure_mods(char_name):
    mods_container = {slot: [] for slot in mod_slots.values()}
    mod_map = {}
    char_stats = unit_stats[char_name_map[char_name]]
    for mod_id, mod in saved_mods[allycode]["mods"].items():
        mod_vector = [0.001 for _i in col_to_mod_stat_map.keys()]
        for col_idx, stat_names in col_to_mod_stat_map.items():
            for stat_name in stat_names:
                value = mod["stats"].get(stat_name, 0)
                if value:
                    scaled_value = scaled_stat_modifiers(stat_name, char_stats)
                    mod_vector[col_idx - 1] += scaled_value * value
        nd_array = np.array(mod_vector)
        mods_container[mod["slot"]].append(nd_array)
        mod_map[str(nd_array.data)] = mod_id
    return mods_container, mod_map


def evaluate_mods():
    weights = construct_weights()
    for weight_object in weights:
        mods_container, mod_map = restructure_mods(weight_object["char_name"])
