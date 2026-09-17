# Mathematical Model of the Room

## Continuous-time model

We treat the room as a single thermal mass:

```
C · dT/dt = (T_out − T)/R + P_heater + P_disturbance
```

### Meaning of each symbol

| Symbol | Meaning | Unit |
|--------|---------|------|
| T | Room temperature | °C |
| T_out | Outdoor temperature | °C |
| R | Thermal resistance of the building envelope | °C/W |
| C | Thermal capacitance (how much energy is needed to raise temperature by 1 °C) | J/°C |
| P_heater | Heat injected by the heater | W |
| P_disturbance | Other heat flows (door, occupancy, solar…) | W |

### Physical intuition

- `(T_out − T)/R` is heat loss/gain through walls and windows (Newton’s law of cooling).
- Larger C → slower temperature change for the same net power (bigger room or more furniture).
- The time constant of the system is τ = R · C. After roughly 3–4 time constants the free response has mostly settled.

## Discrete-time implementation (forward Euler)

```
T[k+1] = T[k] + dt · [(T_out − T[k])/R + P_heater + P_disturbance] / C
```

This is simple, transparent, and accurate enough for the 1-second step we use.

## Parameters used in the project

- R ≈ 0.05 °C/W
- C ≈ 5×10⁵ J/°C
- Heater max power = 3000 W

These values give a realistic residential-scale response on the order of tens of minutes.

> **Note**: This is still a highly simplified model. Real buildings have multiple zones, radiation, humidity, and non-linear effects. For learning classical control the first-order model is sufficient and clear.
