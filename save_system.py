# save_system.py

import json
import os

SAVE_FILE = "savegame.json"

def save_game(state):
    with open(SAVE_FILE, 'w') as f:
        json.dump({"current_node": state}, f)

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            data = json.load(f)
            return data.get("current_node", "start")
    return "start"

def delete_save():
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
