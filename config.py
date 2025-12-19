import json
import os
from pathlib import Path

APP_NAME = "Nvidia Clips Compressor"

CONFIG_DIR = Path(os.getenv("APPDATA")) / APP_NAME
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULTS = {
    "recursive": False,
    "overwrite": False,
    "last_input": "",
    "last_output": "",
}


def load_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return DEFAULTS.copy()
    return DEFAULTS.copy()


def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4)
