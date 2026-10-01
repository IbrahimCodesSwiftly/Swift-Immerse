from src.bulb.bulb_local import check_connection


print("Starting health check...")

result = check_connection()

print("Bulb reachable:", result)