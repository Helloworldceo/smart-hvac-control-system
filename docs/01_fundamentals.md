# Stage 1 – Fundamentals of Control Systems

## What is a control system?

A control system is any arrangement that deliberately influences the behavior of a process so that it behaves the way we want.

### Core vocabulary (room temperature example)

| Term | Meaning in this project |
|------|-------------------------|
| **Plant** | The room (the physical system we want to control) |
| **Output / Controlled variable** | Room air temperature |
| **Setpoint / Reference** | Desired temperature (e.g. 22 °C) |
| **Error** | Setpoint − Measured temperature |
| **Controller** | Algorithm that decides the heater command |
| **Actuator** | The heater |
| **Sensor** | Thermometer |
| **Control signal (u)** | Command sent to the heater, usually in [0, 1] |
| **Disturbance** | Anything that affects temperature that we did not command (outdoor weather, open door, people, solar gain…) |
| **State** | Minimum information needed to predict future behavior (here mainly current temperature) |

### Open-loop vs Closed-loop

- **Open-loop**: controller never looks at the actual temperature. Example: “turn heater on for 40 minutes every morning”. Sensitive to disturbances.
- **Closed-loop (feedback)**: controller continuously (or repeatedly) uses the measured temperature to correct itself. This is what almost all real HVAC systems use.

Feedback is the central idea of classical control.

### Why we care about error

The controller’s job is to drive the error toward zero and keep it there despite disturbances and model uncertainty.
