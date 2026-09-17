"""Simulation engine with realistic disturbances."""

from __future__ import annotations
import numpy as np
from dataclasses import dataclass, field
from .plant import Room
from .controllers.base import Controller
from .config import PLANT, SIM


@dataclass
class SimulationResult:
    time: np.ndarray
    temperature: np.ndarray
    setpoint: np.ndarray
    control: np.ndarray
    outdoor: np.ndarray
    energy: float
    disturbance: np.ndarray = field(default_factory=lambda: np.array([]))
    error: np.ndarray = field(default_factory=lambda: np.array([]))


def run_simulation(
    controller: Controller,
    duration: float = SIM.duration,
    dt: float = PLANT.dt,
    setpoint: float = SIM.setpoint,
    T_init: float = PLANT.T_init,
    T_out_base: float = PLANT.T_out_base,
    enable_disturbances: bool = SIM.enable_disturbances,
    seed: int | None = SIM.seed,
) -> SimulationResult:
    rng = np.random.default_rng(seed)
    room = Room()
    room.T = T_init
    room.T_out = T_out_base
    controller.reset()

    n_steps = int(duration / dt)
    time = np.zeros(n_steps)
    temperature = np.zeros(n_steps)
    sp = np.full(n_steps, setpoint)
    control = np.zeros(n_steps)
    outdoor = np.zeros(n_steps)
    disturbance = np.zeros(n_steps)
    error = np.zeros(n_steps)

    for i in range(n_steps):
        t = i * dt
        time[i] = t

        if enable_disturbances:
            T_out = T_out_base + 3.0 * np.sin(2 * np.pi * t / 3600) + rng.normal(0, 0.3)
            door = -800.0 if (800 < t < 860) or (2000 < t < 2050) else 0.0
            occ = 150.0 if 1200 < t < 2800 else 0.0
            dist = door + occ + rng.normal(0, 20)
        else:
            T_out = T_out_base
            dist = 0.0

        room.T_out = T_out
        outdoor[i] = T_out
        disturbance[i] = dist

        u = controller.compute(room.T, setpoint, dt)
        control[i] = u
        error[i] = setpoint - room.T
        temperature[i] = room.step(u, disturbance_power=dist)

    return SimulationResult(
        time=time, temperature=temperature, setpoint=sp, control=control,
        outdoor=outdoor, energy=room.energy_consumed, disturbance=disturbance, error=error,
    )
