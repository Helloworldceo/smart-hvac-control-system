from .base import Controller

class OnOffController(Controller):
    def __init__(self, hysteresis: float = 0.5):
        self.hysteresis = float(hysteresis)
        self._state = False

    def compute(self, measurement: float, setpoint: float, dt: float = 1.0) -> float:
        if measurement < setpoint - self.hysteresis:
            self._state = True
        elif measurement > setpoint + self.hysteresis:
            self._state = False
        return 1.0 if self._state else 0.0

    def reset(self):
        self._state = False
