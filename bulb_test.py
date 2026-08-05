from bulb import set_brightness, set_color, set_power

bright_response = set_brightness(500)
power_response = set_power(False)
color_response = set_color(0, 1000, 1000)

print(power_response, bright_response, color_response)