from abc import ABC, abstractmethod

class Controller(ABC):
    @abstractmethod
    def compute(self, measurement: float, setpoint: float, dt: float) -> float:
        pass

    def reset(self):
        pass
