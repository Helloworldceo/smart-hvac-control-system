"""Plotting helpers."""

from __future__ import annotations
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from .simulation import SimulationResult
from .metrics import Metrics


def plot_single(result: SimulationResult, title: str, save_path: Path | None = None):
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

    axes[0].plot(result.time / 60, result.temperature, label="Room temp")
    axes[0].plot(result.time / 60, result.setpoint, "r--", label="Setpoint")
    axes[0].set_ylabel("Temperature (°C)")
    axes[0].legend(loc="upper right")
    axes[0].grid(True, alpha=0.3)
    axes[0].set_title(title)

    axes[1].plot(result.time / 60, result.control, color="orange")
    axes[1].set_ylabel("Heater command [0-1]")
    axes[1].set_ylim(-0.05, 1.05)
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(result.time / 60, result.outdoor, label="Outdoor", color="gray")
    if len(result.disturbance) > 0:
        axes[2].plot(result.time / 60, result.disturbance / 100, label="Disturbance/100", alpha=0.7)
    axes[2].set_ylabel("Outdoor (°C) / Dist")
    axes[2].set_xlabel("Time (minutes)")
    axes[2].legend(loc="upper right")
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150)
        print(f"Saved: {save_path}")
    plt.close(fig)


def plot_comparison(
    results: dict[str, SimulationResult],
    metrics_list: list[Metrics],
    save_path: Path | None = None,
):
    fig, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True)

    for name, res in results.items():
        axes[0].plot(res.time / 60, res.temperature, label=name)
    axes[0].plot(list(results.values())[0].time / 60, list(results.values())[0].setpoint, "k--", label="Setpoint")
    axes[0].set_ylabel("Temperature (°C)")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    axes[0].set_title("Controller Comparison – Room Temperature")

    for name, res in results.items():
        axes[1].plot(res.time / 60, res.control, label=name, alpha=0.8)
    axes[1].set_ylabel("Heater command")
    axes[1].set_xlabel("Time (minutes)")
    axes[1].set_ylim(-0.05, 1.05)
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150)
        print(f"Saved: {save_path}")
    plt.close(fig)

    # Metrics table
    print("\n=== Performance Metrics ===")
    print(f"{'Controller':<12} {'Rise (s)':>10} {'Overshoot %':>12} {'Settling (s)':>12} {'SSE (°C)':>10} {'Energy (kWh)':>12}")
    print("-" * 72)
    for m in metrics_list:
        print(
            f"{m.name:<12} {m.rise_time:10.1f} {m.overshoot:12.1f} "
            f"{m.settling_time:12.1f} {m.steady_state_error:10.3f} {m.energy_kwh:12.4f}"
        )
