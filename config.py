import json
from pathlib import Path

CONFIG_FILE = Path("config.json")

DEFAULTS = {"recursive": False, "overwrite": False, "last_input": "", "last_output": ""}


def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return DEFAULTS.copy()


def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4)
