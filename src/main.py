"""Run full controller comparison."""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.config import GAINS, SIM, PLANT
from src.controllers import OnOffController, ProportionalController, PIController, PIDController
from src.simulation import run_simulation
from src.metrics import compute_metrics
from src.plotting import plot_single, plot_comparison


def main():
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    controllers = {
        "ON/OFF": OnOffController(hysteresis=GAINS.onoff_hysteresis),
        "P": ProportionalController(Kp=GAINS.p_Kp),
        "PI": PIController(Kp=GAINS.pi_Kp, Ki=GAINS.pi_Ki),
        "PID": PIDController(Kp=GAINS.pid_Kp, Ki=GAINS.pid_Ki, Kd=GAINS.pid_Kd,
                             derivative_filter_tau=GAINS.pid_derivative_tau),
    }

    results = {}
    metrics_list = []

    print("Running simulations with disturbances...")
    for name, ctrl in controllers.items():
        print(f"  → {name}")
        res = run_simulation(controller=ctrl)
        results[name] = res
        m = compute_metrics(res, name=name)
        metrics_list.append(m)
        fname = name.lower().replace("/", "_") + ".png"
        plot_single(res, title=f"{name} Controller", save_path=results_dir / fname)

    plot_comparison(results, metrics_list, save_path=results_dir / "comparison.png")
    print("\nDone. See results/ for plots and metrics.csv")


if __name__ == "__main__":
    main()
