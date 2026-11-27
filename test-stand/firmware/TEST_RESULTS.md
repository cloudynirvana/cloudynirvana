# Stand controller v2: commands + sensor calibration, Wokwi results (17 Nov 2026)

ESP32 DevKitC + MPU6050 IMU + 3 pressure inputs, real-board pin map (V1 GPIO26, V2 GPIO33, arm sense GPIO25, I2C 21/22).
The IMU in the diagram is given a deliberate error: gyro bias 1.6 / -0.9 deg/s and a 2.0 deg tilt (accelX 0.035 g).
The pressure inputs get zero errors of 0.31 / -0.12 / 0.22 bar in test mode. Commands are injected on a timer (TEST_SCRIPT 1-4); TEST_SCRIPT 0 takes them live from the Serial monitor.

| Case | Commands | Expected | Result |
|---|---|---|---|
| 1 Normal | CAL_P, CAL_IMU, FIRE | offsets found, bias + level found, 3 s countdown, 5 s run, vent opens | PASS: P offsets 0.310 / -0.120 / 0.220 bar; gyro bias 1.595 / -0.893 deg/s; level pitch -2.01 deg; 50 log rows (5.0 s); "RUN COMPLETE" |
| 2 Interlocks | FIRE before arm, FIRE before CAL_IMU, CAL_IMU during run, ABORT | each refused / aborts | PASS: "NAK FIRE: not ARMED", "NAK FIRE: calibrate first", "NAK CAL_IMU: not during countdown/run", ABORT -> SAFE + latch |
| 3 Link loss | heartbeats stop at 7.0 s during the run | abort within 500 ms | PASS: last run row 7.304 s, "SAFE: link lost > 500 ms" |
| 4 Drift | STATUS before and after CAL_IMU | uncalibrated attitude wrong, calibrated ~0 | PASS: before roll/pitch 1.86 / -2.21 deg; after 0.00 / 0.00 |

Calibration rules: CAL_P rejects offsets > 0.5 bar or noise > 0.2 bar; CAL_IMU rejects gyro variance > 0.25 (deg/s)^2 (stand moving) and |g| outside 0.95-1.05; FIRE needs both calibrations, ARMED and a live link.
Not tested here: real transducer noise, ADS1115 path, RS-485 framing (the Serial monitor stands in for the bunker), temperature drift of the gyro bias.
