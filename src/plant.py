"""Room thermal model (first-order)."""

from __future__ import annotations
import numpy as np
from .config import PLANT


class Room:
    def __init__(self, cfg=PLANT):
        self.T = float(cfg.T_init)
        self.T_out = float(cfg.T_out_base)
        self.R = float(cfg.R)
        self.C = float(cfg.C)
        self.heater_max_power = float(cfg.heater_max_power)
        self.dt = float(cfg.dt)
        self.energy_consumed = 0.0  # Joules

    def step(self, u: float, disturbance_power: float = 0.0) -> float:
        u = float(np.clip(u, 0.0, 1.0))
        P_heater = u * self.heater_max_power
        dT = ((self.T_out - self.T) / self.R + P_heater + disturbance_power) / self.C
        self.T += dT * self.dt
        self.energy_consumed += P_heater * self.dt
        return self.T

    def reset(self, T_init: float | None = None):
        if T_init is not None:
            self.T = float(T_init)
        self.energy_consumed = 0.0
