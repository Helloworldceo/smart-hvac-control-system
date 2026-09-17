"""Optional Streamlit dashboard for interactive exploration."""

import streamlit as st
import numpy as np
from src.controllers import OnOffController, ProportionalController, PIController, PIDController
from src.simulation import run_simulation
from src.metrics import compute_metrics
import matplotlib.pyplot as plt

st.set_page_config(page_title="Smart HVAC Control", layout="wide")
st.title("Smart HVAC – Interactive Controller Lab")

controller_type = st.sidebar.selectbox("Controller", ["ON/OFF", "P", "PI", "PID"])
setpoint = st.sidebar.slider("Setpoint (°C)", 18.0, 26.0, 22.0, 0.5)
duration_min = st.sidebar.slider("Duration (min)", 15, 120, 60)
enable_dist = st.sidebar.checkbox("Enable disturbances", True)

if controller_type == "ON/OFF":
    hyst = st.sidebar.slider("Hysteresis", 0.1, 1.5, 0.4, 0.1)
    ctrl = OnOffController(hysteresis=hyst)
elif controller_type == "P":
    Kp = st.sidebar.slider("Kp", 0.1, 5.0, 0.8, 0.1)
    ctrl = ProportionalController(Kp=Kp)
elif controller_type == "PI":
    Kp = st.sidebar.slider("Kp", 0.1, 5.0, 0.6, 0.1)
    Ki = st.sidebar.slider("Ki", 0.001, 0.2, 0.02, 0.001)
    ctrl = PIController(Kp=Kp, Ki=Ki)
else:
    Kp = st.sidebar.slider("Kp", 0.1, 5.0, 1.2, 0.1)
    Ki = st.sidebar.slider("Ki", 0.001, 0.2, 0.04, 0.001)
    Kd = st.sidebar.slider("Kd", 0.0, 30.0, 8.0, 0.5)
    ctrl = PIDController(Kp=Kp, Ki=Ki, Kd=Kd)

if st.sidebar.button("Run Simulation", type="primary"):
    with st.spinner("Simulating..."):
        res = run_simulation(
            controller=ctrl,
            duration=duration_min * 60,
            setpoint=setpoint,
            enable_disturbances=enable_dist,
        )
        m = compute_metrics(res, name=controller_type)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rise time (s)", f"{m.rise_time:.0f}")
    col2.metric("Overshoot %", f"{m.overshoot:.1f}")
    col3.metric("SSE (°C)", f"{m.steady_state_error:.3f}")
    col4.metric("Energy (kWh)", f"{m.energy_kwh:.3f}")

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(res.time / 60, res.temperature, label="Room")
    ax.plot(res.time / 60, res.setpoint, "r--", label="Setpoint")
    ax.set_xlabel("Time (min)")
    ax.set_ylabel("Temperature (°C)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
