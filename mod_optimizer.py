import json
import re
from env import get_env
from initialise_data_structures import initialise_data_structures
from openpyxl import load_workbook

data_lookups = initialise_data_structures()
env_data = get_env()

allycode = env_data["allycode"]

with open('saved-mods.json', 'r', encoding='utf-8') as f:
    saved_mods = json.load(f)

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
        "weights": char_weights,
        "thresholds": char_thresholds
    })
    count += 1

