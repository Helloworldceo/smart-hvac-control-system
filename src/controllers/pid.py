"""
Full PID controller implemented from scratch.

Features:
- Proportional, Integral, Derivative terms
- Anti-windup on the integral term
- Simple first-order filter on the derivative term (to reduce noise amplification)
"""

from .base import Controller
import numpy as np


class PIDController(Controller):
    def __init__(
        self,
        Kp: float = 2.0,
        Ki: float = 0.1,
        Kd: float = 5.0,
        u_min: float = 0.0,
        u_max: float = 1.0,
        derivative_filter_tau: float = 10.0,  # seconds
    ):
        self.Kp = float(Kp)
        self.Ki = float(Ki)
        self.Kd = float(Kd)
        self.u_min = float(u_min)
        self.u_max = float(u_max)
        self.tau = float(derivative_filter_tau)

        self.integral = 0.0
        self.prev_error = 0.0
        self.prev_derivative = 0.0

    def compute(self, measurement: float, setpoint: float, dt: float) -> float:
        error = setpoint - measurement

        # Integral
        self.integral += error * dt

        # Derivative with simple low-pass filter
        raw_derivative = (error - self.prev_error) / dt if dt > 0 else 0.0
        alpha = dt / (self.tau + dt) if (self.tau + dt) > 0 else 1.0
        derivative = alpha * raw_derivative + (1 - alpha) * self.prev_derivative

        u = self.Kp * error + self.Ki * self.integral + self.Kd * derivative

        # Anti-windup
        if u > self.u_max:
            u = self.u_max
            self.integral -= error * dt
        elif u < self.u_min:
            u = self.u_min
            self.integral -= error * dt

        self.prev_error = error
        self.prev_derivative = derivative

        return float(u)

    def reset(self):
        self.integral = 0.0
        self.prev_error = 0.0
        self.prev_derivative = 0.0
