from bulb import set_brightness, set_colour, set_power

bright_response = set_brightness(500)
power_response = set_power(False)
colour_response = set_colour(0, 1000, 1000)

print(power_response, bright_response, colour_response)