"""Save / load game state to a JSON file.

Deliberately simple: one file, one dict, no migrations yet.
"""

import json
import os
from dataclasses import asdict

from src.chores import ChoreLog, Chore

SAVE_DIR = "saves"
SAVE_FILE = os.path.join(SAVE_DIR, "save.json")


def save_game(chore_log: ChoreLog, wood: int, player_x: float,
              player_y: float) -> None:
    os.makedirs(SAVE_DIR, exist_ok=True)
    data = {
        "version": 1,
        "wood": wood,
        "player": {"x": player_x, "y": player_y},
        "chores": {
            "pool": chore_log.pool,
            "total_completed": chore_log.total_completed,
            "chores": [asdict(c) for c in chore_log.chores],
        },
    }
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_game() -> dict | None:
    if not os.path.exists(SAVE_FILE):
        return None
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def apply_save(data: dict, chore_log: ChoreLog) -> tuple[int, float, float]:
    """Restore a ChoreLog in place. Returns (wood, x, y)."""
    chore_log.pool = data["chores"]["pool"]
    chore_log.total_completed = data["chores"]["total_completed"]

    saved = {c["id"]: c for c in data["chores"]["chores"]}
    for c in chore_log.chores:
        s = saved.get(c.id)
        if s:
            c.done = s["done"]

    return data["wood"], data["player"]["x"], data["player"]["y"]
