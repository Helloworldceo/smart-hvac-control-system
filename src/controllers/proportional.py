from .base import Controller
import numpy as np

class ProportionalController(Controller):
    def __init__(self, Kp: float = 1.0, u_min: float = 0.0, u_max: float = 1.0):
        self.Kp = float(Kp)
        self.u_min = float(u_min)
        self.u_max = float(u_max)

    def compute(self, measurement: float, setpoint: float, dt: float = 1.0) -> float:
        error = setpoint - measurement
        return float(np.clip(self.Kp * error, self.u_min, self.u_max))
