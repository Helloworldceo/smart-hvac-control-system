"""Performance metrics."""

from __future__ import annotations
import numpy as np
from dataclasses import dataclass
from .simulation import SimulationResult


@dataclass
class Metrics:
    name: str
    rise_time: float
    overshoot: float
    settling_time: float
    steady_state_error: float
    energy_kwh: float
    iae: float          # Integral Absolute Error
    max_error: float


def compute_metrics(result: SimulationResult, name: str = "") -> Metrics:
    t = result.time
    y = result.temperature
    sp = result.setpoint[0]
    dt = t[1] - t[0] if len(t) > 1 else 1.0

    y0 = y[0]
    y_final = np.mean(y[-int(300 / dt):]) if len(y) > 10 else y[-1]

    # Rise time 10% → 90%
    target_10 = y0 + 0.1 * (sp - y0)
    target_90 = y0 + 0.9 * (sp - y0)
    try:
        t10 = t[np.where(y >= target_10)[0][0]]
        t90 = t[np.where(y >= target_90)[0][0]]
        rise_time = float(t90 - t10)
    except IndexError:
        rise_time = float("nan")

    peak = np.max(y)
    overshoot = max(0.0, (peak - sp) / max(abs(sp - y0), 1e-6) * 100)

    band = 0.02 * abs(sp - y0)
    settled = np.abs(y - sp) <= band
    settling_time = float("nan")
    for i in range(len(y) - 1, -1, -1):
        if not settled[i]:
            if i + 1 < len(t):
                settling_time = float(t[i + 1])
            break
    else:
        settling_time = float(t[0])

    sse = abs(sp - y_final)
    iae = float(np.sum(np.abs(result.error)) * dt)
    max_error = float(np.max(np.abs(result.error)))
    energy_kwh = result.energy / 3.6e6

    return Metrics(
        name=name, rise_time=rise_time, overshoot=overshoot,
        settling_time=settling_time, steady_state_error=sse,
        energy_kwh=energy_kwh, iae=iae, max_error=max_error,
    )
