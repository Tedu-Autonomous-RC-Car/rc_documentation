# 🔩 Hardware Architecture & Interface

This document specifies the physical layer, wiring protocols, and power distribution for the **TAVP (TED Autonomous Vehicle Project)**. The architecture employs a **Distributed Control System (DCS)** pattern, utilizing the high-performance computing of the Jetson Orin Nano while offloading time-critical actuation to secondary microcontrollers.

---

## 🏗 High-Level System Topology

The system is centered around the **NVIDIA Jetson Orin Nano**, which serves as the primary compute node for perception and decision-making. To ensure high-precision PWM timing and system safety, actuation is decoupled into two dedicated **Arduino** microcontrollers.

### 🛰 Component Specifications

| Component | Model | Purpose |
| --- | --- | --- |
| **Main Compute** | NVIDIA Jetson Orin Nano (8GB) | ROS2 Node execution, AI Inference (SAC/PPO), and Sensor Fusion. |
| **Perception (Lidar)** | RPLIDAR A1M8-R6 | 360° 2D laser scanning for SLAM and obstacle avoidance. |
| **Perception (Vision)** | USB Camera (Generic) | Monocular vision for lane detection and visual navigation. |
| **Steering MCU** | Arduino Nano/Uno | Real-time 50Hz PWM generation for the high-torque steering servo. |
| **Drive MCU** | Arduino Nano/Uno | Throttle control logic and H-Bridge direction switching. |
| **DC Motor Driver** | BTS7960 (43A) | High-current H-Bridge for high-speed traction control. |
| **Power Source** | 3S/4S LiPo Battery | 11.1V - 14.8V main power rail for high-performance runs. |

---

## 🔌 Actuator Subsystems

### 1. Steering Control (Arduino Node A)

To ensure smooth and jitter-free cornering—essential for Reinforcement Learning stability—the Steering MCU maintains a constant **50Hz PWM signal**. It receives steering angles from the Jetson via Serial at **115200 baud**.

| Arduino Pin | Connection | Logic / Function |
| --- | --- | --- |
| **D9** | **DSSERVO DS3235** | PWM Signal (1000µs - 2000µs range) |
| **5V / VIN** | External BEC | Dedicated 6V/3A Power source to handle 35kg torque |
| **GND** | Common Ground | Signal reference to prevent noise-induced jitter |

### 2. Traction Control (Arduino Node B)

The Drive MCU translates throttle commands into PWM duty cycles and manages the "Direction" pins for the BTS7960 high-current driver.

| Arduino Pin | Connection | Logic / Function |
| --- | --- | --- |
| **D5 (PWM)** | **RPWM / LPWM** | Speed Control via Duty Cycle (0-255) |
| **D4** | **L_EN / R_EN** | H-Bridge Enable pins (Logic High = Active) |
| **GND** | Common Ground | High-current reference ground |

---

## ⚡ Power Distribution & Safety

Autonomous systems require stable power isolation to prevent logic brownouts during high-current surges from the **RS775 DC Motors**.

### 🔋 Power Rails

* **Logic Rail (5V):** Powered by a **5V/5A Buck Converter**. This rail independently feeds the Jetson Orin Nano, USB Hub, and sensors.
* **Actuator Rail (11.1V-14.8V):** Direct connection from the LiPo battery to the BTS7960 Motor Driver B+ terminals.
* **Servo Rail (6V):** A separate **6V Regulator** isolates the high-torque steering servo from the logic rail to eliminate electromagnetic interference (EMI).

> [!CAUTION]
> **Common Ground Rule:** All ground (GND) wires from the Jetson, Arduinos, Motor Driver, and Battery **must** be connected at a single **Star Ground** point. This is critical to prevent ground loops that cause sensor data corruption.

---

## 📡 Data Handshake Protocol

Communication between the Jetson (Master) and Arduinos (Slaves) follows a framed packet format to minimize latency and ensure data integrity:

| Header | Steering Angle | Throttle Value | Checksum | Terminator |
| --- | --- | --- | --- | --- |
| `$` | `-45.0` to `45.0` | `0` to `255` | `HEX` | `\n` |

---

## 🔍 Udev Rule Configuration

To ensure the Jetson consistently identifies the correct MCU for each task, persistent device naming is implemented via Udev rules.

```bash
# /etc/udev/rules.d/99-arduino-tavp.rules

# Steering Controller (CH340/Generic)
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", SYMLINK+="ttySteering"

# Drive Controller (Official/Arduino)
SUBSYSTEM=="tty", ATTRS{idVendor}=="2341", ATTRS{idProduct}=="0043", SYMLINK+="ttyDrive"

```
