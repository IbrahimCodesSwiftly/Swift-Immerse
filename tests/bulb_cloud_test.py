import time

from src.bulb.bulb_cloud import set_color, set_power

start = time.perf_counter()
set_power(True)
print(time.perf_counter() - start)

for _ in range(100):
    start = time.perf_counter()

    set_color(0, 1000, 1000)  # Red (HSV)

    print(time.perf_counter() - start)

    start = time.perf_counter()

    set_color(120, 1000, 1000)  # Green

    print(time.perf_counter() - start)

    start = time.perf_counter()

    set_color(240, 1000, 1000)  # Blue

    print(time.perf_counter() - start)

start = time.perf_counter()
set_power(False)
print(time.perf_counter() - start)
# print("3...")
# time.sleep(1)

# print("2...")
# time.sleep(1)

# print("1...")
# time.sleep(1)

# start = time.perf_counter()
# print("Sending!")

# set_color(120, 1000, 1000)

# print("Returned after:", time.perf_counter() - start)
    

# bright_response = set_brightness(500)
# power_response = set_power(False)
# color_response = set_color(0, 1000, 1000)

# print(power_response, bright_response, color_response)