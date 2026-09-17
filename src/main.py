"""
Main entry point – runs the full comparison of all controllers.
"""

from pathlib import Path
import sys

# Ensure src is importable when running as module
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.controllers import (
    OnOffController,
    ProportionalController,
    PIController,
    PIDController,
)
from src.simulation import run_simulation
from src.metrics import compute_metrics
from src.plotting import plot_single, plot_comparison


def main():
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    duration = 3600.0  # 1 hour
    dt = 1.0
    setpoint = 22.0
    T_init = 16.0

    controllers = {
        "ON/OFF": OnOffController(hysteresis=0.4),
        "P": ProportionalController(Kp=0.8),
        "PI": PIController(Kp=0.6, Ki=0.02),
        "PID": PIDController(Kp=1.2, Ki=0.04, Kd=8.0),
    }

    results = {}
    metrics_list = []

    print("Running simulations...")
    for name, ctrl in controllers.items():
        print(f"  → {name}")
        res = run_simulation(
            controller=ctrl,
            duration=duration,
            dt=dt,
            setpoint=setpoint,
            T_init=T_init,
            enable_disturbances=True,
            seed=42,
        )
        results[name] = res
        m = compute_metrics(res, name=name)
        metrics_list.append(m)

        # Individual plot
        plot_single(res, title=f"{name} Controller", save_path=results_dir / f"{name.lower().replace('/', '_')}.png")

    # Comparison plot + metrics table
    plot_comparison(results, metrics_list, save_path=results_dir / "comparison.png")

    print("\nDone. Check the results/ folder for plots.")


if __name__ == "__main__":
    main()
