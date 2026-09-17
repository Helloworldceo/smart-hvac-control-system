"""
Stage 1 — Tiny exercise: Error calculation and simple ON/OFF decision

Your task:
1. Calculate the error
2. Write the if-condition that decides whether the heater should be ON or OFF
3. Run it with current = 18.0 and then with current = 23.5
4. Observe and explain what happens
"""

target = 22.0          # setpoint (°C)
current = 18.0         # measured temperature (°C) – pretend this comes from a sensor

# 1. Calculate the error
error = None           # <-- replace None with the correct expression

# 2. Simple on/off decision
#    If the room is too cold (error > 0), turn heater ON
#    Otherwise turn heater OFF
if None:               # <-- replace None with the correct condition
    heater = "ON"
else:
    heater = "OFF"

print(f"Target:  {target} °C")
print(f"Current: {current} °C")
print(f"Error:   {error} °C")
print(f"Heater command: {heater}")
