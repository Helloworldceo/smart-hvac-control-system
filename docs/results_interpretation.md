# Interpreting the Results

After running `python -m src.main` you obtain:

1. Individual plots for each controller (`results/on_off.png`, `p.png`, …)
2. A comparison plot (`results/comparison.png`)
3. A metrics table printed to the terminal

## What to look for

- **ON/OFF**: Clear oscillation, relatively high energy use, never settles quietly.
- **P**: Faster than ON/OFF, but usually a visible steady-state offset.
- **PI**: Eliminates steady-state error, may be a bit more oscillatory than pure P.
- **PID**: Best combination of speed, low overshoot, and zero steady-state error when tuned well.

## Metrics definitions

- **Rise time**: time to go from 10% to 90% of the initial step.
- **Overshoot**: how far the temperature exceeds the setpoint (percentage of the step size).
- **Settling time**: time after which the temperature stays inside a ±2% band around the setpoint.
- **Steady-state error**: absolute difference between setpoint and average temperature in the last 5 minutes.
- **Energy**: total electrical energy consumed by the heater (kWh).

These metrics let you objectively compare controllers under the same disturbance scenario.
