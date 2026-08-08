from tuya_connector import TuyaOpenAPI
from config.config import config

# ========= CONFIG =========
ACCESS_ID = config["tuya"]["ACCESS_ID"]
ACCESS_SECRET = config["tuya"]["ACCESS_SECRET"]
API_ENDPOINT = config["tuya"]["ENDPOINT"]
DEVICE_ID = config["tuya"]["DEVICE_ID"]
# ==========================

DEFAULT_WHITE_TEMPERATURE = 1000
openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_SECRET)

if not openapi.connect()["success"]:
    raise Exception("Failed to connect to Tuya")

def send_commands(commands: list):
    '''Send commands to the device.'''
    return openapi.post(
        f"/v1.0/iot-03/devices/{DEVICE_ID}/commands",
        {
            "commands": commands
        }
    )

def set_power(is_on: bool):
    '''Set the power state of the device.'''
    response = send_commands([
            {
                "code": "switch_led",
                "value": is_on
            }
        ])
    return response.get("success", False)

def set_color(h: int, s: int, v: int):
    '''Set the color of the device.'''
    h = max(0, min(h, 360)) #hue must be between 0 and 360, 0 is red, 120 is green, 240 is blue
    s = max(0, min(s, 1000)) #saturation must be between 0 and 1000, 0 is no color, 1000 is full color
    v = max(0, min(v, 1000)) #value must be between 0 and 1000, 0 is off, 1000 is full brightness
    send_commands([
        {
        "code": "work_mode",
        "value": "colour"
        },
        {
            "code": "colour_data_v2",
            "value": {
                "h": h,
                "s": s,
                "v": v
            }
        }
    ])

def set_white(brightness: int, temperature: int = DEFAULT_WHITE_TEMPERATURE):
    '''Set the white light of the device.'''
    brightness = max(10, min(brightness, 1000)) #brightness must be between 10 and 1000
    temperature = max(0, min(temperature, 1000)) #color temperature must be between 0 and 1000
    send_commands([
        {
            "code": "work_mode",
            "value": "white"
        },
        {
            "code": "bright_value_v2",
            "value": brightness
        },
        {
            "code": "temp_value_v2",
            "value": temperature
        }
    ])