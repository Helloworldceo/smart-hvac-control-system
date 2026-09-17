# Limitations & Possible Extensions

## Limitations of the current model

- Single thermal zone (real houses have multiple rooms).
- No humidity, radiation, or solar gain model.
- Heater is idealized (instantaneous power, no dynamics).
- Sensor is perfect (no noise, no delay).
- Parameters are constant (real R and C change with wind, furniture, etc.).

## Natural extensions you can try

1. Add sensor noise and a simple low-pass filter on the measurement.
2. Add actuator dynamics (first-order lag on heater power).
3. Implement a two-zone model (living room + bedroom) with coupling.
4. Replace PID with a simple Model Predictive Controller (MPC).
5. Learn the plant parameters online (system identification).
6. Connect the controller to a real microcontroller + temperature sensor (hardware-in-the-loop).

These extensions bridge classical control toward the more advanced methods used in modern energy management systems.
