"""Performance metrics for control experiments."""

from __future__ import annotations
import numpy as np
from dataclasses import dataclass
from .simulation import SimulationResult


@dataclass
class Metrics:
    rise_time: float          # seconds (10% → 90%)
    overshoot: float          # percent
    settling_time: float      # seconds (±2% band)
    steady_state_error: float # °C (last 5 minutes average)
    energy_kwh: float
    name: str = ""


def compute_metrics(result: SimulationResult, name: str = "") -> Metrics:
    t = result.time
    y = result.temperature
    sp = result.setpoint[0]

    # Normalize for step response metrics
    y0 = y[0]
    y_final = np.mean(y[-int(300 / (t[1] - t[0])) :])  # last ~5 min

    # Rise time 10% → 90%
    target_10 = y0 + 0.1 * (sp - y0)
    target_90 = y0 + 0.9 * (sp - y0)

    try:
        t10 = t[np.where(y >= target_10)[0][0]]
        t90 = t[np.where(y >= target_90)[0][0]]
        rise_time = t90 - t10
    except IndexError:
        rise_time = np.nan

    # Overshoot
    peak = np.max(y)
    overshoot = max(0.0, (peak - sp) / (sp - y0) * 100) if (sp - y0) != 0 else 0.0

    # Settling time (±2%)
    band = 0.02 * abs(sp - y0)
    settled = np.abs(y - sp) <= band
    # Find last time it entered the band and stayed
    settling_time = np.nan
    for i in range(len(y) - 1, -1, -1):
        if not settled[i]:
            if i + 1 < len(t):
                settling_time = t[i + 1]
            break
    else:
        settling_time = t[0]

    # Steady-state error
    sse = abs(sp - y_final)

    energy_kwh = result.energy / 3.6e6  # J → kWh

    return Metrics(
        rise_time=float(rise_time),
        overshoot=float(overshoot),
        settling_time=float(settling_time),
        steady_state_error=float(sse),
        energy_kwh=float(energy_kwh),
        name=name,
    )
