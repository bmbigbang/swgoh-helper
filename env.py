import json
import os


def get_env():
    if not os.path.isfile('env.json'):
        print("please create env.json, including your username, password and allycode to use")
    else:
        with open('env.json', 'r', encoding='utf-8') as f:
            env_data = json.load(f)
        for attr in ["username", "password", "allycode"]:
            if attr not in env_data:
                raise "could not find {0} in env.json".format(attr)

        return env_data