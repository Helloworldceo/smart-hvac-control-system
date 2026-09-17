# Controllers

All controllers output a signal `u ∈ [0, 1]` that is multiplied by the maximum heater power.

## ON/OFF (Bang-Bang)

```
if T < setpoint − hysteresis → u = 1
if T > setpoint + hysteresis → u = 0
else keep previous state
```

Produces characteristic oscillation around the setpoint. Simple and robust but energy-inefficient and causes wear.

## Proportional (P)

```
u = Kp · e
e = setpoint − measurement
```

- Larger Kp → faster response, higher risk of overshoot/oscillation.
- Pure P control usually leaves a steady-state error when there is a constant disturbance or heat loss.

## PI

```
u = Kp · e + Ki · ∫e dt
```

The integral term accumulates past error and drives steady-state error to zero (for constant disturbances). Anti-windup is implemented by freezing the integrator when the output saturates.

## PID

```
u = Kp · e + Ki · ∫e dt + Kd · de/dt
```

- Derivative term anticipates the future error and adds damping → reduces overshoot.
- A simple first-order filter is applied to the derivative to limit high-frequency noise amplification.
- Anti-windup protects the integral term.

## Tuning notes (used in this project)

The gains provided in `main.py` are reasonable starting points for the chosen plant parameters. In a real system you would use step-response methods, Ziegler–Nichols, or automated tuning.
