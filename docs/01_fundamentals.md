# Stage 1 — Fundamentals of Control Systems

## What is a control system?

A control system is any arrangement that deliberately influences the behavior of something so that it behaves the way we want.

### Key terms (using the room-temperature example)

- **Plant**: the room itself
- **Output / Controlled variable**: room temperature
- **Setpoint / Reference**: desired temperature (e.g. 22 °C)
- **Error**: Setpoint − Measured temperature
- **Controller**: decides what the heater should do
- **Actuator**: the heater
- **Sensor**: thermometer
- **Input / Control signal**: command sent to the heater
- **Disturbance**: anything that affects temperature that we did not command (outdoor weather, open door, people, sunlight…)
- **State**: current condition of the plant needed to predict future behavior (mainly current temperature in the simple model)

### Open-loop vs Closed-loop

- **Open-loop**: controller acts without looking at the actual temperature
- **Closed-loop (feedback)**: controller continuously uses the measured temperature to correct itself

We will almost always use closed-loop control.

## Tiny exercise

See `src/stage1_fundamentals/exercise_01_error_and_on_off.py`
