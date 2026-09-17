"""
Room thermal model (first-order).

Physics:
    C * dT/dt = (T_out - T) / R + P_heater + P_disturbance

Discretized with forward Euler for simplicity and clarity.
"""

from __future__ import annotations
import numpy as np


class Room:
    """Simple single-zone room model."""

    def __init__(
        self,
        T_init: float = 18.0,
        T_out: float = 5.0,
        R: float = 0.05,          # °C/W  (thermal resistance)
        C: float = 5e5,           # J/°C  (thermal capacitance)
        heater_max_power: float = 3000.0,  # W
        dt: float = 1.0,          # simulation step in seconds
    ):
        self.T = float(T_init)
        self.T_out = float(T_out)
        self.R = float(R)
        self.C = float(C)
        self.heater_max_power = float(heater_max_power)
        self.dt = float(dt)

        # Internal state for energy accounting
        self.energy_consumed = 0.0  # Joules

    def step(self, u: float, disturbance_power: float = 0.0) -> float:
        """
        Advance the room by one time step.

        Parameters
        ----------
        u : float
            Control signal in [0, 1]. 1 = full heater power.
        disturbance_power : float
            Additional heat flow in Watts (can be negative).

        Returns
        -------
        float
            New room temperature (°C)
        """
        u = float(np.clip(u, 0.0, 1.0))
        P_heater = u * self.heater_max_power

        # Heat balance
        dT = ((self.T_out - self.T) / self.R + P_heater + disturbance_power) / self.C
        self.T += dT * self.dt

        # Energy accounting (only heater energy)
        self.energy_consumed += P_heater * self.dt

        return self.T

    def reset(self, T_init: float | None = None):
        if T_init is not None:
            self.T = float(T_init)
        self.energy_consumed = 0.0
