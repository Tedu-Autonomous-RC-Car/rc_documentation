# 🔩 Hardware Architecture & Interface

This document specifies the physical layer, wiring protocols, and power distribution for the TAVP Autonomous RC Car. The architecture follows a **Distributed Control System (DCS)** pattern, offloading real-time actuation to secondary microcontrollers.

---

## 🏗 High-Level System Topology

The system is centered around the **NVIDIA Jetson Orin Nano**, which serves as the primary compute node. Actuation is decoupled into two dedicated **Arduino** microcontrollers to ensure high-precision PWM timing and safety.



### 🛰 Component Specifications

| Component | model | Purpose |
| :--- | :--- | :--- |
| **Main Compute** | NVIDIA Jetson Orin Nano | ROS2 Node execution, AI Inference (SAC/PPO), LIDAR processing. |
| **Steering MCU** | Arduino Nano/Uno | Real-time PWM generation for high-torque steering servo. |
| **Drive MCU** | Arduino Nano/Uno | Speed control logic and H-Bridge direction switching. |
| **DC Motor Driver** | BTS7960 / IBT-2 | High-current (43A) H-Bridge for drive motor traction. |
| **Power Source** | 3S/4S LiPo Battery | 11.1V - 14.8V main power rail. |

---

## 🔌 Actuator Subsystems

### 1. Steering Control (Arduino Node A)
To ensure smooth and jitter-free cornering, the Steering MCU maintains a constant 50Hz PWM signal. It receives steering angles from the Jetson via Serial at 115200 baud.

| Arduino Pin | Connection | Logic/Function |
| :--- | :--- | :--- |
| **D9** | Servo Signal | PWM (Pulse Width Modulation) |
| **5V / VIN** | External BEC | Dedicated 5V/3A Power source |
| **GND** | Common Ground | Reference ground for signal integrity |

### 2. Traction Control (Arduino Node B)
The Drive MCU translates throttle commands into PWM duty cycles and manages the "Direction" pins for the H-Bridge motor driver.

| Arduino Pin | Connection | Logic/Function |
| :--- | :--- | :--- |
| **D5 (PWM)** | RPWM / LPWM | Speed Control (Duty Cycle) |
| **D4** | L_EN / R_EN | Enable pins for Motor Driver |
| **GND** | Common Ground | Reference ground |



---

## ⚡ Power Distribution & Safety

Autonomous systems require stable power to prevent logic brownouts during high-current motor surges.

### 🔋 Power Rails
1.  **Logic Rail (5V):** Powered by a 5V/5A Buck Converter. Feeds the Jetson and USB peripherals.
2.  **Actuator Rail (Main Battery V):** Direct connection to the Motor Driver.
3.  **Servo Rail:** Separate 6V regulator to prevent servo noise from affecting the Arduinos.

> [!CAUTION]
> **Common Ground Rule:** All ground (GND) wires from the Jetson, Arduinos, Motor Driver, and Battery **must** be connected at a single point (Star Ground) to prevent ground loops and data corruption.

---

## 📡 Data Handshake Protocol

The communication between the Jetson (Master) and Arduinos (Slaves) follows a simple packet format to minimize latency:

| Header | Steering | Throttle | Checksum | End |
| :--- | :--- | :--- | :--- | :--- |
| `$` | `-45.0` to `45.0` | `0` to `255` | `HEX` | `\n` |

### 🔍 Udev Rule Configuration
To ensure the Jetson always identifies the correct Arduino for the correct task, we use persistent device naming:

```bash
# /etc/udev/rules.d/99-arduino-tavp.rules
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", SYMLINK+="ttySteering"
SUBSYSTEM=="tty", ATTRS{idVendor}=="2341", ATTRS{idProduct}=="0043", SYMLINK+="ttyDrive"
```