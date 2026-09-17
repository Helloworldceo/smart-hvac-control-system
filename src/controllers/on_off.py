"""Classic ON/OFF (bang-bang) controller with optional hysteresis."""

from .base import Controller


class OnOffController(Controller):
    def __init__(self, hysteresis: float = 0.5):
        """
        Parameters
        ----------
        hysteresis : half-width of the dead band around the setpoint.
                     Heater turns ON when T < setpoint - hysteresis
                     Heater turns OFF when T > setpoint + hysteresis
        """
        self.hysteresis = float(hysteresis)
        self._state = False  # current heater state

    def compute(self, measurement: float, setpoint: float, dt: float = 1.0) -> float:
        if measurement < setpoint - self.hysteresis:
            self._state = True
        elif measurement > setpoint + self.hysteresis:
            self._state = False
        # else keep previous state (hysteresis)

        return 1.0 if self._state else 0.0

    def reset(self):
        self._state = False
