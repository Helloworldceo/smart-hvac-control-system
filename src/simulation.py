"""Simulation engine with optional disturbances."""

from __future__ import annotations
import numpy as np
from dataclasses import dataclass, field
from typing import Callable

from .plant import Room
from .controllers.base import Controller


@dataclass
class SimulationResult:
    time: np.ndarray
    temperature: np.ndarray
    setpoint: np.ndarray
    control: np.ndarray
    outdoor: np.ndarray
    energy: float
    disturbance: np.ndarray = field(default_factory=lambda: np.array([]))


def run_simulation(
    controller: Controller,
    duration: float = 3600.0,          # seconds
    dt: float = 1.0,
    setpoint: float = 22.0,
    T_init: float = 16.0,
    T_out_base: float = 5.0,
    enable_disturbances: bool = True,
    seed: int | None = 42,
) -> SimulationResult:
    """
    Run a closed-loop simulation.

    Disturbances (when enabled):
    - Slow outdoor temperature variation (sinusoidal + noise)
    - Occasional door-opening events (negative heat pulses)
    - Random occupancy heat gains
    """
    rng = np.random.default_rng(seed)

    room = Room(T_init=T_init, T_out=T_out_base, dt=dt)
    controller.reset()

    n_steps = int(duration / dt)
    time = np.zeros(n_steps)
    temperature = np.zeros(n_steps)
    sp = np.full(n_steps, setpoint)
    control = np.zeros(n_steps)
    outdoor = np.zeros(n_steps)
    disturbance = np.zeros(n_steps)

    for i in range(n_steps):
        t = i * dt
        time[i] = t

        # Outdoor temperature variation
        if enable_disturbances:
            # Daily-ish sinusoid + noise (scaled for 1-hour demo)
            T_out = T_out_base + 3.0 * np.sin(2 * np.pi * t / 3600) + rng.normal(0, 0.3)
            # Door openings: short negative pulses
            door = -800.0 if (800 < t < 860) or (2000 < t < 2050) else 0.0
            # Occupancy heat gain
            occ = 150.0 if 1200 < t < 2800 else 0.0
            dist = door + occ + rng.normal(0, 20)
        else:
            T_out = T_out_base
            dist = 0.0

        room.T_out = T_out
        outdoor[i] = T_out
        disturbance[i] = dist

        # Controller
        u = controller.compute(room.T, setpoint, dt)
        control[i] = u

        # Plant step
        temperature[i] = room.step(u, disturbance_power=dist)

    return SimulationResult(
        time=time,
        temperature=temperature,
        setpoint=sp,
        control=control,
        outdoor=outdoor,
        energy=room.energy_consumed,
        disturbance=disturbance,
    )
