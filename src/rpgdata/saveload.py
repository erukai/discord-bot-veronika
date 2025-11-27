import json
import os

def save_stats(stats_dict, filename="user_stats.json", folder="rpgdata"):
    path = os.path.join("src", folder, filename)
    with open(path, "w") as f:
        json.dump(stats_dict, f, indent=4)

def load_stats(filename="user_stats.json", folder="rpgdata"):
    path = os.path.join("src", folder, filename)
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}