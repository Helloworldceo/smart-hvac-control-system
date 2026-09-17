"""Central configuration for the HVAC control project."""

from dataclasses import dataclass


@dataclass
class PlantConfig:
    T_init: float = 16.0
    T_out_base: float = 5.0
    R: float = 0.05          # °C/W
    C: float = 5.0e5         # J/°C
    heater_max_power: float = 3000.0  # W
    dt: float = 1.0          # s


@dataclass
class SimConfig:
    duration: float = 3600.0  # s (1 hour)
    setpoint: float = 22.0
    enable_disturbances: bool = True
    seed: int = 42


@dataclass
class ControllerGains:
    onoff_hysteresis: float = 0.4
    p_Kp: float = 0.8
    pi_Kp: float = 0.6
    pi_Ki: float = 0.02
    pid_Kp: float = 1.2
    pid_Ki: float = 0.04
    pid_Kd: float = 8.0
    pid_derivative_tau: float = 10.0


PLANT = PlantConfig()
SIM = SimConfig()
GAINS = ControllerGains()
