import tinytuya
import time
from src.bulb import set_color
from config.config import config

DEVICE_ID = config["tuya"]["DEVICE_ID"]
IP = config["tuya"]["IP"]
LOCAL_KEY = config["tuya"]["LOCAL_KEY"]

bulb = tinytuya.BulbDevice(
    DEVICE_ID,
    IP,
    LOCAL_KEY,
)

bulb.set_version(3.5)
bulb.set_socketPersistent(True)
bulb.set_socketTimeout(0.5)
bulb.detect_bulb(nowait=False)

start = time.perf_counter()

bulb.turn_on()

print(time.perf_counter() - start)

# for i in range(20):
#     start = time.perf_counter()

#     bulb.set_colour(255, 0, 0)

#     elapsed = time.perf_counter() - start

#     print(f"{i:02d}: {elapsed:.4f}s")

for _ in range(100):
    start = time.perf_counter()

    set_color(255, 0, 0)

    print(time.perf_counter() - start)
    time.sleep(0.1)

    start = time.perf_counter()

    set_color(0, 255, 0)
    
    print(time.perf_counter() - start)
    time.sleep(0.1)

    start = time.perf_counter()

    set_color(0, 0, 255)

    print(time.perf_counter() - start)
    time.sleep(0.1)

# bulb.set_colour(255, 0, 0)

# print("3...")
# time.sleep(1)

# print("2...")
# time.sleep(1)

# print("1...")
# time.sleep(1)

# start = time.perf_counter()
# print("Sending!")

# bulb.set_colour(0, 0, 0)

# print("Returned after:", time.perf_counter() - start)

# bulb.set_colour(116, 0, 0)

bulb.turn_off()

print(time.perf_counter() - start)