# Smart HVAC / Room Temperature Control System

Complete implementation of a room temperature control system built from first principles.

This project covers the full progression:

1. Fundamentals of control systems
2. ON/OFF controller
3. First-order mathematical model of a room
4. Proportional (P) control
5. PI and PID control (implemented from scratch)
6. Disturbances and robustness testing
7. Performance metrics and comparison
8. Visualization and clean packaging

## Features

- Physics-based room thermal model (first-order lag)
- Controllers implemented from scratch: ON/OFF, P, PI, PID
- Realistic disturbances (outdoor temperature variation, door openings, occupancy)
- Performance metrics: rise time, overshoot, settling time, steady-state error, energy consumption
- Side-by-side comparison of all controllers
- Clean modular architecture
- Ready for extension to MPC or RL later

## Quick Start

```bash
git clone https://github.com/Helloworldceo/smart-hvac-control-system.git
cd smart-hvac-control-system
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run the full comparison
python -m src.main
```

Plots and metrics will be saved in `results/`.

## Project Structure

```
src/
├── plant.py              # Room thermal model
├── controllers/
│   ├── base.py
│   ├── on_off.py
│   ├── proportional.py
│   ├── pi.py
│   └── pid.py
├── simulation.py         # Simulation engine + disturbances
├── metrics.py            # Rise time, overshoot, settling, SSE, energy
├── plotting.py           # Visualization helpers
└── main.py               # Run all experiments

docs/
├── mathematical_model.md
├── controllers.md
└── results_interpretation.md

experiments/
results/
```

## Mathematical Model (Room)

We use a simple but realistic first-order model:

```
C * dT/dt = (T_out - T)/R + P_heater + P_disturbance
```

Where:
- `T` = room temperature (°C)
- `T_out` = outdoor temperature (°C)
- `R` = thermal resistance (°C/W)
- `C` = thermal capacitance (J/°C)
- `P_heater` = heater power (W)
- `P_disturbance` = additional heat gains/losses

This is discretized with a fixed time step for simulation.

## Controllers

### ON/OFF
Classic bang-bang with hysteresis option.

### Proportional (P)
```
u(t) = Kp * e(t)
```

### PI
```
u(t) = Kp * e(t) + Ki * ∫e(τ)dτ
```

### PID (from scratch)
```
u(t) = Kp * e(t) + Ki * ∫e(τ)dτ + Kd * de/dt
```

Anti-windup and derivative filtering are included in the PID implementation.

## Performance Metrics

For every controller we compute:

- Rise time (10% → 90%)
- Overshoot (%)
- Settling time (±2% band)
- Steady-state error
- Total energy consumed by the heater

## Example Results

After running `python -m src.main` you will see comparison plots and a metrics table in the terminal and in `results/`.

## Requirements

- Python ≥ 3.10
- numpy
- matplotlib
- pandas (optional, for nice tables)

## License

MIT
