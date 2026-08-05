from pathlib import Path
import json

DEFAULTS_PATH = Path("config/defaults.json")
CONFIG_PATH = Path("config/config.json")

with open(DEFAULTS_PATH, "r") as f:
    defaults = json.load(f)

config = {}

if CONFIG_PATH.exists():
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)

# Merge defaults with user config
for category, settings in defaults.items():
    if category in config:
        for key, value in settings.items():
            if key not in config[category]:
                config[category][key] = value
    else:
        config[category] = settings.copy()