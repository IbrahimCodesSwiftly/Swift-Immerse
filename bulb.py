from tuya_connector import TuyaOpenAPI

# ========= CONFIG =========
ACCESS_ID = "f8xcvjpuj3g3g7qwyrxy"
ACCESS_SECRET = "9b8f29f8a7914c479f2445535f0dd69f"
API_ENDPOINT = "https://openapi.tuyain.com"
DEVICE_ID = "d7a914028f279baac4i04a"
# ==========================

openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_SECRET)

if not openapi.connect()["success"]:
    raise Exception("Failed to connect to Tuya")

#send commands to the device
def send_commands(commands: list):
    return openapi.post(
        f"/v1.0/iot-03/devices/{DEVICE_ID}/commands",
        {
            "commands": commands
        }
    )

#set the power state of the device
def set_power(is_on: bool):
    return send_commands([
            {
                "code": "switch_led",
                "value": is_on
            }
        ])

#set the brightness of the device
def set_brightness(brightness: int):
    brightness = max(10, min(brightness, 1000)) #brightness must be between 10 and 1000
    return send_commands([
        {
            "code": "bright_value_v2",
            "value": brightness
        }
    ])

#set the colour of the device
def set_colour(h: int, s: int, v: int):
    h = max(0, min(h, 360)) #hue must be between 0 and 360, 0 is red, 120 is green, 240 is blue
    s = max(0, min(s, 1000)) #saturation must be between 0 and 1000, 0 is no colour, 1000 is full colour
    v = max(0, min(v, 1000)) #value must be between 0 and 1000, 0 is off, 1000 is full brightness
    return send_commands([
        {
            "code": "colour_data_v2",
            "value": {
                "h": h,
                "s": s,
                "v": v
            }
        }
    ])