# Controllers Explained

All controllers output a signal `u ∈ [0, 1]` that is multiplied by the maximum heater power.

## 1. ON/OFF (Bang-Bang)

```
if T < setpoint − hysteresis → u = 1
if T > setpoint + hysteresis → u = 0
else keep previous state
```

- Extremely simple and robust.
- Produces characteristic oscillation around the setpoint.
- Energy inefficient and causes mechanical wear if the actuator is a relay.
- Hysteresis prevents rapid chattering.

## 2. Proportional (P)

```
u(t) = Kp · e(t)
e(t) = setpoint − measurement
```

- Larger Kp → faster response, higher risk of overshoot and oscillation.
- Pure P control usually leaves a **steady-state error** when there is constant heat loss or a constant disturbance (the heater must stay partially on, which requires a non-zero error).

## 3. PI (Proportional-Integral)

```
u(t) = Kp · e(t) + Ki · ∫ e(τ) dτ
```

- The integral term accumulates past error and keeps increasing the control signal until the error is driven to zero.
- This eliminates steady-state error for constant disturbances.
- **Anti-windup** is essential: when the heater is already at 100 %, we must stop integrating, otherwise the integral grows huge and causes large overshoot when the error finally changes sign.

## 4. PID (Proportional-Integral-Derivative)

```
u(t) = Kp · e(t) + Ki · ∫ e(τ) dτ + Kd · de/dt
```

- **Derivative term** anticipates the future error (it looks at the slope). It adds damping and reduces overshoot.
- Pure differentiation amplifies noise, so we apply a simple first-order low-pass filter to the derivative.
- Anti-windup is still applied to the integral term.

### Tuning intuition (very rough)

- Increase Kp until the response is reasonably fast but not too oscillatory.
- Add Ki to remove steady-state error; increase carefully to avoid instability.
- Add Kd to reduce overshoot and damp oscillations.

In this project the gains in `src/config.py` are reasonable starting points for the chosen plant parameters.
