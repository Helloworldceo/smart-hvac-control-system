# Metrics & Suggested Experiments

## Metrics we compute

| Metric | Meaning |
|--------|--------|
| Rise time | Time to go from 10 % to 90 % of the step |
| Overshoot | How far the temperature exceeds the setpoint (% of step size) |
| Settling time | Time after which the temperature stays inside a ±2 % band |
| Steady-state error (SSE) | |setpoint − average temperature in last ~5 min| |
| IAE | Integral of Absolute Error – overall tracking quality |
| Energy (kWh) | Total electrical energy consumed by the heater |

## Suggested experiments

1. **Disable disturbances** (`enable_disturbances=False`) and compare ideal step responses of P / PI / PID.
2. **Sweep Kp** for pure P control and plot overshoot vs Kp.
3. **Compare energy** of ON/OFF vs well-tuned PID under the same disturbance profile.
4. **Change outdoor base temperature** and observe how much more energy is needed.
5. **Increase heater power** and see how rise time improves (and whether overshoot gets worse).
6. Open the Streamlit dashboard and interactively change gains while watching the response.

## Interpreting typical results

- ON/OFF: clear oscillation, never really “settles”, relatively high energy.
- P: faster, but visible steady-state offset.
- PI: removes the offset, may be a bit more oscillatory.
- PID: usually the best compromise of speed, low overshoot and zero steady-state error when tuned properly.
