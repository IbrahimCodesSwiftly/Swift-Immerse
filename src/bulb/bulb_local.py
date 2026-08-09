import tinytuya
from config.config import config
import time  #temp

DEFAULT_WHITE_TEMPERATURE = 1000

bulb = tinytuya.BulbDevice(
    config["tuya"]["DEVICE_ID"],
    config["tuya"]["IP"],
    config["tuya"]["LOCAL_KEY"],
)

bulb.set_version(3.5)
bulb.set_socketPersistent(False) #temp false
bulb.set_socketTimeout(0.5)
bulb.detect_bulb(nowait=False)

def set_power(is_on: bool):
    """Set the power state of the device."""
    response = bulb.turn_on() if is_on else bulb.turn_off()

    if response is None:
        return True

    return "Err" not in response


# def set_brightness(brightness: int):
#     '''Set the brightness of the device.'''
#     brightness = max(0, min(brightness, 1000))
#     return bulb.set_brightness(brightness)


def set_color(h: int, s: int, v: int):
    '''Set the color of the device.'''
    h = max(0, min(h, 360)) / 360 #hue must be between 0 and 360, 0 is red, 120 is green, 240 is blue
    s = max(0, min(s, 1000)) / 1000 #saturation must be between 0 and 1000, 0 is no color, 1000 is full color
    v = max(0, min(v, 1000)) / 1000 #value must be between 0 and 1000, 0 is off, 1000 is full brightness

    print(f"Sending HSV: h={h}, s={s}, v={v}") ###temp
    print(f"SET COLOR {h:.3f}, {s:.3f}, {v:.3f} @ {time.perf_counter():.3f}")  #temp
    bulb.set_hsv(h, s, v, nowait=True)


def set_white(brightness: int, temperature: int = DEFAULT_WHITE_TEMPERATURE):
    '''Set the white light of the device.'''
    brightness = max(10, min(brightness, 1000)) #brightness must be between 10 and 1000
    temperature = max(0, min(temperature, 1000)) #color temperature must be between 0 and 1000

    bulb.set_white(brightness, temperature)