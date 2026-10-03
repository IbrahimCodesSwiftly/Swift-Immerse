from config.config import config

mode = config["mode"].lower()

if mode == "full_screen":
    print("Using Full Screen Mode")
    from .full_screen import *

elif mode == "ambient_edge":
    print("Using Ambient Edge Mode")
    from .ambient_edge import *

else:
    raise ValueError(
        f"Unknown mode: {mode}. Please set 'mode' in config.json to either 'full_screen' or 'ambient_edge'."
    )