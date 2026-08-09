import time

from src.bulb import set_power
from src.bulb.worker import start, stop, set_state


set_power(True)

start()

print("RED")
set_state("color", (0, 1000, 1000))
time.sleep(2)

print("WHITE")
set_state("white", 500)
time.sleep(2)

print("BLACK")
set_state("color", (0, 0, 0))
time.sleep(2)

print("BLUE")
set_state("color", (240, 1000, 1000))
time.sleep(2)

print("Stopping worker...")
stop()

print("Done.")

# import time

# from src.bulb import set_power
# from src.bulb.worker import start, stop, set_state


# set_power(True)

# start()

# print("RED")
# set_state("color", (0, 1000, 1000))
# time.sleep(1)

# print("WHITE")
# set_state("white", 500)
# time.sleep(1)

# print("BLACK")
# set_state("color", (0, 0, 0))
# time.sleep(1)

# print("BLUE")
# set_state("color", (240, 1000, 1000))
# time.sleep(1)

# print("Stopping worker...")
# stop()

# print("Done.")

# # import time
# # from src.bulb.bulb_local import set_power, set_color, set_white

# # set_power(True)

# # print("RED")
# # set_color(0, 1000, 1000)
# # time.sleep(0.2)

# # print("WHITE")
# # set_white(500)
# # time.sleep(0.2)

# # print("RED")
# # set_color(0, 1000, 1000)
# # time.sleep(0.2)

# # print("BLACK")
# # set_color(0, 0, 0)
# # time.sleep(0.2)

# # print("WHITE")
# # set_white(500)
# # time.sleep(0.2)

# # print("RED AGAIN")
# # set_color(0, 1000, 1000)
# # time.sleep(0.2)

# # print("BLUE")
# # set_color(240, 1000, 1000)
# # time.sleep(0.2)

# # # print("RED AGAIN - RETRY")
# # # set_color(0, 1000, 1000)
# # # time.sleep(1)

# # print("Done.")

# # import time

# # from src.bulb import set_power
# # from src.bulb.worker import start, stop, set_state


# # set_power(True)

# # start()

# # print("RED")
# # set_state("color", (0, 1000, 1000))
# # time.sleep(1)

# # print("WHITE")
# # set_state("white", 500)
# # time.sleep(1)

# # print("BLACK")
# # set_state("color", (0, 0, 0))
# # time.sleep(1)

# # print("BLUE")
# # set_state("color", (240, 1000, 1000))
# # time.sleep(1)

# # print("Stopping worker...")
# # stop()

# # print("Done.")


# # set_power(True)

# # colors = [
# #     (0, 1000, 1000),      # Red
# #     (120, 1000, 1000),    # Green
# #     (240, 1000, 1000),    # Blue
# # ]

# # for i in range(100):
# #     color = colors[i % 3]

# #     print(f"{i + 1:03} -> {color}")
# #     set_color(*color)

# #     time.sleep(0.1)  # 10 commands/sec

# # print("Finished sending.")