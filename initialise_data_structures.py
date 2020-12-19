import json
import os
from api_swgoh_help import api_swgoh_help, settings
from env import get_env


def initialise_data_structures(force_reload=False):
    saved_data = { "toons": {}, "skills": {}, "abilities": {}, "gear": {}, "modSets": {} }
    if not force_reload and os.path.isfile('saved-data.json'):
        with open('saved-data.json', 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        if len(saved_data["toons"]):
            return saved_data

    env_data = get_env()
    # Change the settings below
    creds = settings(env_data["username"], env_data["password"])
    client = api_swgoh_help(creds)

    # Build local list of obtainable characters
    payload = {}
    payload['collection'] = "unitsList"
    payload['language'] = "eng_us"
    payload['enums'] = True
    payload['match'] = {
        "rarity": 7,
        "obtainable": True,
        "obtainableTime": 0
    }
    # payload['project'] = {
    #     "baseId": 1,
    #     "nameKey": 1,
    #     "descKey": 1,
    #     "forceAlignment": 1,
    #     "categoryIdList": 1,
    #     "combatType": 1
    # }
    units = client.fetchData(payload)

    for unit in units:
        saved_data["toons"][unit['baseId']] = unit

    # Build local skills list
    payload = {}
    payload['collection'] = "skillList"
    payload['language'] = "eng_us"
    payload['enums'] = True
    # payload['project'] = {
    #     "id": 1,
    #     "abilityReference": 1,
    #     "isZeta": 1
    # }
    items = client.fetchData(payload)

    for skill in items:
        saved_data["skills"][skill['id']] = skill

    # Build local abilities list
    # skills[id]['abilityReference'] -> abilities[id]
    payload = {}
    payload['collection'] = "abilityList"
    payload['language'] = "eng_us"
    payload['enums'] = True
    # payload['project'] = {
    #     "id": 1,
    #     "type": 1,
    #     "nameKey": 1
    # }
    items = client.fetchData(payload)

    for ability in items:
        saved_data["abilities"][ability['id']] = ability

    # Build local gear list
    payload = {}
    payload['collection'] = "equipmentList"
    payload['language'] = "eng_us"
    payload['enums'] = True
    # payload['project'] = {
    #     "id": 1,
    #     "nameKey": 1
    # }
    items = client.fetchData(payload)
    for gear in items:
        saved_data["gear"][gear['id']] = gear

    payload = {
        'collection': "statModSetList",
        'language': "eng_us",
        'enums': True,
    }
    mod_stat_list = client.fetchData(payload)
    saved_data["modSets"] = {i["id"]: i for i in mod_stat_list}

    with open('saved-data.json', 'w', encoding='utf-8') as f:
        json.dump(saved_data, f, ensure_ascii=False, indent=4)
    return saved_data


# run with force reload to update cache of stored data
# initialise_data_structures(force_reload=True)