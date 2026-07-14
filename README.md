# PID-Based DC Motor Speed Control 🚀

This repository contains the Arduino code and documentation for implementing a PID (Proportional-Integral-Derivative) controller to precisely regulate the speed of a DC motor using an L298N motor driver and a quadrature encoder.

## How It Works
The system uses a closed-loop feedback mechanism:
1. **Target (Setpoint):** The desired speed in RPM.
2. **Measurement (Feedback):** The quadrature encoder reads the actual motor rotations.
3. **Error Calculation:** `Error = Target - Actual`
4. **PID Algorithm:** Computes a correction value based on the error (P), the accumulation of past errors (I), and the rate of change of the error (D).
5. **Control Output:** The Arduino translates the PID output into a PWM (Pulse Width Modulation) signal, adjusting the voltage sent to the L298N motor driver.

## Hardware Requirements
*   Arduino Uno / Nano / Mega
*   DC Motor with Quadrature Encoder
*   L298N Motor Driver Module
*   12V DC Power Supply (for the motor)
*   Jumper wires

## Wiring Diagram

| Arduino Pin | Component Pin | Function |
| :--- | :--- | :--- |
| `Pin 2` | Encoder A | Interrupt for counting pulses |
| `Pin 3` | Encoder B | Direction sensing |
| `Pin 9` | L298N `ENA` | PWM speed control |
| `Pin 8` | L298N `IN1` | Direction control 1 |
| `Pin 7` | L298N `IN2` | Direction control 2 |
| `5V` / `GND` | Encoder VCC/GND | Power for encoder |
| `VIN` / `GND` | L298N 12V/GND | Power from external supply |

> **Note:** Ensure the grounds of the Arduino, L298N, and 12V power supply are tied together.

## Tuning the PID
To get smooth motor performance, you need to tune the `kp`, `ki`, and `kd` variables in the code:
*   **Kp (Proportional):** Increases the response speed but can cause overshoot if too high.
*   **Ki (Integral):** Eliminates steady-state error (getting stuck just below the target) but can cause oscillation.
*   **Kd (Derivative):** Dampens the system, reducing overshoot and settling time.
