from tuya_connector import TuyaOpenAPI

# ========= CONFIG =========
ACCESS_ID = "f8xcvjpuj3g3g7qwyrxy"
ACCESS_SECRET = "9b8f29f8a7914c479f2445535f0dd69f"
API_ENDPOINT = "https://openapi.tuyain.com"
DEVICE_ID = "d7a914028f279baac4i04a"
# ==========================

openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_SECRET)

openapi.connect()

def turn_on():
    commands = {
        "commands": [
            {
                "code": "switch_led",
                "value": True
            }
        ]
    }

    return openapi.post(
        f"/v1.0/iot-03/devices/{DEVICE_ID}/commands",
        commands
    )