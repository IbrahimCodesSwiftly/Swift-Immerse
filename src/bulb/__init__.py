from config.config import config

mode = config["mode"].lower()

if mode == "cloud":
    print("Using Cloud Backend")
    from .bulb_cloud import *

elif mode == "local":
    print("Using Local Backend")
    from .bulb_local import *

else:
    raise ValueError(f"Unknown mode: {mode}. Please set 'mode' in config.json to either 'cloud' or 'local'.")