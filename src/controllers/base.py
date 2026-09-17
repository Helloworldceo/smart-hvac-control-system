"""Base controller interface."""

from abc import ABC, abstractmethod


class Controller(ABC):
    """All controllers expose the same interface."""

    @abstractmethod
    def compute(self, measurement: float, setpoint: float, dt: float) -> float:
        """
        Compute control signal u ∈ [0, 1].

        Parameters
        ----------
        measurement : current room temperature
        setpoint    : desired temperature
        dt          : time step (needed for integral/derivative)

        Returns
        -------
        u : float in [0, 1]
        """
        pass

    def reset(self):
        """Reset internal state (integral, previous error, etc.)."""
        pass
