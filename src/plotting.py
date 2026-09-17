"""Plotting and reporting helpers."""

from __future__ import annotations
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from .simulation import SimulationResult
from .metrics import Metrics


def plot_single(result: SimulationResult, title: str, save_path: Path | None = None):
    fig, axes = plt.subplots(4, 1, figsize=(11, 10), sharex=True)

    axes[0].plot(result.time / 60, result.temperature, label="Room temp", lw=1.8)
    axes[0].plot(result.time / 60, result.setpoint, "r--", label="Setpoint", lw=1.5)
    axes[0].set_ylabel("Temperature (°C)")
    axes[0].legend(loc="upper right")
    axes[0].grid(True, alpha=0.3)
    axes[0].set_title(title)

    axes[1].plot(result.time / 60, result.control, color="darkorange", lw=1.2)
    axes[1].set_ylabel("Heater [0–1]")
    axes[1].set_ylim(-0.05, 1.05)
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(result.time / 60, result.error, color="purple", lw=1.2)
    axes[2].axhline(0, color="gray", ls="--", lw=0.8)
    axes[2].set_ylabel("Error (°C)")
    axes[2].grid(True, alpha=0.3)

    axes[3].plot(result.time / 60, result.outdoor, label="Outdoor", color="steelblue")
    if len(result.disturbance):
        axes[3].plot(result.time / 60, result.disturbance / 100, label="Disturbance/100", alpha=0.7)
    axes[3].set_ylabel("Outdoor / Dist")
    axes[3].set_xlabel("Time (minutes)")
    axes[3].legend(loc="upper right")
    axes[3].grid(True, alpha=0.3)

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=160, bbox_inches="tight")
        print(f"Saved: {save_path}")
    plt.close(fig)


def plot_comparison(results: dict[str, SimulationResult], metrics_list: list[Metrics], save_path: Path | None = None):
    fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True)

    for name, res in results.items():
        axes[0].plot(res.time / 60, res.temperature, label=name, lw=1.6)
    axes[0].plot(list(results.values())[0].time / 60, list(results.values())[0].setpoint, "k--", label="Setpoint", lw=1.4)
    axes[0].set_ylabel("Temperature (°C)")
    axes[0].legend(ncol=3)
    axes[0].grid(True, alpha=0.3)
    axes[0].set_title("Controller Comparison")

    for name, res in results.items():
        axes[1].plot(res.time / 60, res.control, label=name, alpha=0.85, lw=1.2)
    axes[1].set_ylabel("Heater command")
    axes[1].set_xlabel("Time (minutes)")
    axes[1].set_ylim(-0.05, 1.05)
    axes[1].legend(ncol=3)
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=160, bbox_inches="tight")
        print(f"Saved: {save_path}")
    plt.close(fig)

    # Console + CSV
    print("\n=== Performance Metrics ===")
    rows = []
    header = f"{'Controller':<10} {'Rise(s)':>9} {'Overshoot%':>11} {'Settling(s)':>12} {'SSE(°C)':>9} {'IAE':>9} {'Energy(kWh)':>12}"
    print(header)
    print("-" * len(header))
    for m in metrics_list:
        print(f"{m.name:<10} {m.rise_time:9.1f} {m.overshoot:11.1f} {m.settling_time:12.1f} "
              f"{m.steady_state_error:9.3f} {m.iae:9.1f} {m.energy_kwh:12.4f}")
        rows.append({
            "Controller": m.name, "Rise_time_s": m.rise_time, "Overshoot_pct": m.overshoot,
            "Settling_time_s": m.settling_time, "SSE_C": m.steady_state_error,
            "IAE": m.iae, "Energy_kWh": m.energy_kwh, "Max_error_C": m.max_error,
        })
    if save_path:
        csv_path = save_path.parent / "metrics.csv"
        pd.DataFrame(rows).to_csv(csv_path, index=False)
        print(f"Saved: {csv_path}")
