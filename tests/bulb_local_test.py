import tinytuya
import time
from src.bulb.bulb_local import set_color, set_power, set_white
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


# colors = [
#     (0, 1000, 1000),
#     (120, 1000, 1000),
#     (240, 1000, 1000)
# ]

set_power(True)

def timed(name, function, *args):
    start = time.perf_counter()

    response = function(*args)

    elapsed = time.perf_counter() - start

    print(f"{name}: {elapsed:.3f}s | Response: {response}")


timed("WHITE", set_white, 500)

time.sleep(2)

timed("RED", set_color, 0, 1000, 1000)

time.sleep(2)

timed("GREEN", set_color, 120, 1000, 1000)

time.sleep(2)

timed("BLUE", set_color, 240, 1000, 1000)

# print("1. WHITE")
# response = set_white(500)
# print("White response:", response)

# time.sleep(3)

# print("2. RED")
# response = set_color(0, 1000, 1000)
# print("Red response:", response)

# time.sleep(3)

# print("3. GREEN")
# response = set_color(120, 1000, 1000)
# print("Green response:", response)

# time.sleep(3)

# print("4. BLUE")
# response = set_color(240, 1000, 1000)
# print("Blue response:", response)

# print("WHITE")
# set_white(500)

# time.sleep(5)

# print("RED")
# set_color(0, 1000, 1000)

# time.sleep(5)

# print("WHITE")
# set_white(500)

# time.sleep(5)

# print("BLUE")
# set_color(240, 1000, 1000)

# time.sleep(2)

# print("Done.")

# print("WHITE")
# set_white(500)

# time.sleep(2)

# print("BLACK")
# set_color(0, 0, 0)

# time.sleep(2)

# print("WHITE")
# set_white(500)

# time.sleep(2)

# print("BLACK")
# set_color(0, 0, 0)

# time.sleep(2)

# print("COLOR")
# set_color(0, 1000, 1000)

# time.sleep(2)

# print("BLACK")
# set_color(0, 0, 0)

# for i in range(100):
#     color = colors[i % 3]

#     print(f"{i + 1}/100 -> {color}")
#     set_color(*color)

#     time.sleep(1 / 30)

# for i in range(100):
#     print(f"Cycle {i + 1}/100")

#     set_white(500)
#     set_color(0, 1000, 1000)

# print("Finished")  #Test 2

# for i in range(100):
#     print(f"Color {i + 1}/100")

#     set_color(0, 1000, 1000)
#     set_color(120, 1000, 1000)
#     set_color(240, 1000, 1000)

# print("Finished colors")  #Test 1

# for i in range(50):
#     print(f"Sending white command {i + 1}/100")
#     start = time.perf_counter()


#     set_white(500)

#     elapsed = time.perf_counter() - start
#     print(f"{i:02d}: {elapsed:.4f}s")
    

#     print("White commands finished. Sending RED...")
#     start = time.perf_counter()


#     set_color(0, 1000, 1000)

#     elapsed = time.perf_counter() - start
#     print(f"{i:02d}: {elapsed:.4f}s")

#     print("Sending GREEN...")
#     time.sleep(1)

#     start = time.perf_counter()

#     set_color(120, 1000, 1000)

#     elapsed = time.perf_counter() - start
#     print(f"{i:02d}: {elapsed:.4f}s")

#     print("Sending BLUE...")
#     time.sleep(1)

#     start = time.perf_counter()

#     set_color(240, 1000, 1000)

#     elapsed = time.perf_counter() - start
#     print(f"{i:02d}: {elapsed:.4f}s")

#     print("Done.")


# set_color(0, 1000, 1000)

# time.sleep(1)

# set_white(500)

# time.sleep(1)

# set_color(120, 1000, 1000)

# time.sleep(1)

# set_color(240, 1000, 1000)

# response = set_power(True)
# print(response)

# response = set_power(False)
# print(response)

# start = time.perf_counter()

# bulb.turn_on()

# print(time.perf_counter() - start)

# # for i in range(20):
# #     start = time.perf_counter()

# #     bulb.set_colour(255, 0, 0)

# #     elapsed = time.perf_counter() - start

# #     print(f"{i:02d}: {elapsed:.4f}s")

# for _ in range(50):
#     start = time.perf_counter()

#     set_color(255, 0, 0)

#     print(time.perf_counter() - start)
#     time.sleep(0.03)

#     start = time.perf_counter()

#     set_color(0, 255, 0)
    
#     print(time.perf_counter() - start)
#     time.sleep(0.03)

#     start = time.perf_counter()

#     set_color(0, 0, 255)

#     print(time.perf_counter() - start)
#     time.sleep(0.03)

# # bulb.set_colour(255, 0, 0)

# # print("3...")
# # time.sleep(1)

# # print("2...")
# # time.sleep(1)

# # print("1...")
# # time.sleep(1)

# # start = time.perf_counter()
# # print("Sending!")

# # bulb.set_colour(0, 0, 0)

# # print("Returned after:", time.perf_counter() - start)

# # bulb.set_colour(116, 0, 0)

# bulb.turn_off()

# print(time.perf_counter() - start)