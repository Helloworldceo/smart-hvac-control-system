"""
Stage 1 reference – Error calculation and simple ON/OFF decision
(This is the tiny exercise from the beginning of the project.)
"""

target = 22.0
current = 18.0

error = target - current

if error > 0:
    heater = "ON"
else:
    heater = "OFF"

print(f"Target:  {target} °C")
print(f"Current: {current} °C")
print(f"Error:   {error} °C")
print(f"Heater command: {heater}")
