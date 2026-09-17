# Smart HVAC / Room Temperature Control System

Professional implementation of a room temperature control system built from first principles.

Covers the full progression: Fundamentals → ON/OFF → Mathematical Model → P → PI → PID → Disturbances → Metrics & Visualization.

## Features

- Physics-based first-order room thermal model
- Controllers from scratch: ON/OFF (hysteresis), P, PI (anti-windup), PID (anti-windup + derivative filter)
- Realistic disturbances (outdoor variation, door openings, occupancy)
- Rich performance metrics + CSV export
- High-quality comparison plots
- Configurable via `config.py`
- Optional Streamlit live dashboard
- Clean modular architecture

## Quick Start

```bash
git clone https://github.com/Helloworldceo/smart-hvac-control-system.git
cd smart-hvac-control-system
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Full comparison (plots + metrics + CSV)
python -m src.main

# Optional interactive dashboard
streamlit run src/dashboard.py
```

Results appear in `results/` (PNG plots + `metrics.csv`).

## Project Structure

```
src/
├── config.py              # All tunable parameters
├── plant.py               # Room thermal model
├── controllers/           # ON/OFF, P, PI, PID
├── simulation.py          # Engine + disturbances
├── metrics.py             # Rise/settling/overshoot/SSE/energy
├── plotting.py            # Visualization
├── dashboard.py           # Streamlit UI (optional)
└── main.py
docs/
results/
```

## Mathematical Model

```
C * dT/dt = (T_out - T)/R + P_heater + P_disturbance
```

Discretized with forward Euler. Time constant τ = R·C.

## Controllers

| Controller | Equation | Notes |
|------------|----------|-------|
| ON/OFF | bang-bang + hysteresis | Oscillates, simple |
| P | u = Kp·e | Steady-state error remains |
| PI | + Ki·∫e | Eliminates SSE, anti-windup |
| PID | + Kd·de/dt | Damping + filtered derivative |

## License

MIT
