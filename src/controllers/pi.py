"""Proportional-Integral controller with simple anti-windup."""

from .base import Controller
import numpy as np


class PIController(Controller):
    def __init__(
        self,
        Kp: float = 1.0,
        Ki: float = 0.05,
        u_min: float = 0.0,
        u_max: float = 1.0,
    ):
        self.Kp = float(Kp)
        self.Ki = float(Ki)
        self.u_min = float(u_min)
        self.u_max = float(u_max)
        self.integral = 0.0

    def compute(self, measurement: float, setpoint: float, dt: float) -> float:
        error = setpoint - measurement

        # Provisional integral
        self.integral += error * dt

        u = self.Kp * error + self.Ki * self.integral

        # Simple anti-windup: clamp integral if output saturates
        if u > self.u_max:
            u = self.u_max
            self.integral -= error * dt  # freeze integral
        elif u < self.u_min:
            u = self.u_min
            self.integral -= error * dt

        return float(u)

    def reset(self):
        self.integral = 0.0
