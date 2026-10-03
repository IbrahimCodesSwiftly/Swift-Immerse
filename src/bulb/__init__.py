from config.config import config

bulb_mode = config["bulb_mode"].lower()

if bulb_mode == "cloud":
    print("Using Cloud Backend")
    from .bulb_cloud import *

elif bulb_mode == "local":
    print("Using Local Backend")
    from .bulb_local import *

else:
    raise ValueError(
        f"Unknown mode: {bulb_mode}. Please set 'bulb_mode' in config.json to either 'cloud' or 'local'."
        )