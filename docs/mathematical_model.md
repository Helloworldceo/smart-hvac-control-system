# Mathematical Model of the Room

## Continuous-time model

We model the room as a single thermal mass:

```
C · dT/dt = (T_out − T)/R + P_heater + P_disturbance
```

### Variables

| Symbol          | Meaning                        | Typical unit |
|-----------------|--------------------------------|--------------|
| T               | Room air temperature           | °C           |
| T_out           | Outdoor temperature            | °C           |
| R               | Thermal resistance of envelope | °C/W         |
| C               | Thermal capacitance of room    | J/°C         |
| P_heater        | Heat input from heater         | W            |
| P_disturbance   | Other heat flows (door, people, solar…) | W     |

### Physical intuition

- `(T_out − T)/R` is heat flowing through the walls/windows (Newton’s law of cooling).
- `C` determines how fast the temperature changes for a given net heat flow (larger room or heavier furniture → larger C → slower dynamics).
- The time constant of the system is `τ = R · C`.

## Discrete-time implementation

We use forward Euler:

```
T[k+1] = T[k] + dt · [(T_out − T[k])/R + P_heater + P_disturbance] / C
```

This is simple, transparent, and accurate enough for the time steps we use (1 s).

## Parameters used in the project

- R ≈ 0.05 °C/W
- C ≈ 5×10⁵ J/°C
- Heater max power = 3000 W
- These values give a realistic residential-scale response (tens of minutes).
