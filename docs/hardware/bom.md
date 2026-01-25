# 📋 Bill of Materials (BOM) - Updated

This document provides a comprehensive, professional breakdown of all hardware costs and components for the **TAVP Autonomous RC Car** project. The budget reflects high-performance edge computing, precision actuation, and 360-degree environmental perception.

---

## 💰 Budget Summary

The following tables summarize the total expenditure for the project. All prices include KDV (VAT) and reflect the current 2026 market rates.

### 1. Core Compute & Networking

| Component | Description | Qty | Unit Price | Total Price |
| --- | --- | --- | --- | --- |
| **NVIDIA Jetson Orin Nano** | Waveshare 8GB AI Development Kit | 1 | ₺27,718.20 | ₺27,718.20 |
| **Power Adapter** | 12V/5A DC Power Supply | 1 | ₺1,200.60 | ₺1,200.60 |
| **Storage (NVMe SSD)** | CS2230 M.2 NVMe SSD 500GB | 1 | ₺4,698.00 | ₺4,698.00 |
| **Wireless Module** | Wireless-AC8265 NIC (Dual Antenna) | 1 | ₺1,096.20 | ₺1,096.20 |
| **Subtotal** |  |  |  | **₺34,713.00** |

### 2. Perception & Sensors

| Component | Description | Qty | Unit Price | Total Price |
| --- | --- | --- | --- | --- |
| **RPLIDAR A1M8-R6** | 360° Laser Scanner (6m Range) | 1 | ₺6,269.07 | ₺6,269.07 |
| **USB Camera** | Standard UVC Vision Module | 1 | *Existing* | ₺0.00 |
| **Subtotal** |  |  |  | **₺6,269.07** |

### 3. Actuation & Drive System

| Component | Description | Qty | Unit Price | Total Price |
| --- | --- | --- | --- | --- |
| **Steering Servo** | DSSERVO DS3235 35kg (180°) | 1 | ₺270.10 | ₺270.10 |
| **Main Drive Motor** | RS775 DC Motor (12V 12000Rpm) | 2 | ₺270.10 | ₺540.20 |
| **Motor Driver** | BTS7960B 43A High-Current H-Bridge | 1 | ₺231.20 | ₺231.20 |
| **Subtotal** |  |  |  | **₺1,041.50** |

### 4. Chassis & Mechanical Parts

| Component | Description | Qty | Unit Price | Total Price |
| --- | --- | --- | --- | --- |
| **3D Printing Filament** | Creality Ender PLA+ (Apple Green) | 3 | ₺532.40 | ₺1,597.20 |
| **Bearings** | MR105ZZ Miniature Ball Bearings | 8 | ₺29.73 | ₺237.80 |
| **Subtotal** |  |  |  | **₺1,835.00** |

---

## 📉 Total Project Expenditure

| Category | Allocated Cost |
| --- | --- |
| Core Compute & Networking | ₺34,713.00 |
| Perception & Sensors | ₺6,269.07 |
| Actuation & Drive System | ₺1,041.50 |
| Mechanical & Materials | ₺1,835.00 |
| **Grand Total** | **₺43,858.57** |

---

## 📦 Component Technical Details

### Slamtec RPLIDAR A1M8-R6

* **360° Scanning:** Provides a full 2D laser scan of the environment for SLAM and obstacle avoidance.
* **High Sampling Rate:** Capable of up to **8000 samples per second**, making it ideal for high-speed autonomous RC racing.
* **6-Meter Range:** Sufficient for indoor racing tracks and laboratory testing environments.
* **OPTMAG Technology:** Uses a patented optical-magnetic design to extend the system's operational lifespan and stability.

### Waveshare Jetson Orin Nano 8GB

* **AI Compute:** Delivers up to 40 TOPS for real-time Reinforcement Learning inference.
* **Architecture:** Compatible with the latest NVIDIA JetPack SDK, supporting ROS2 and TensorRT.

> [!TIP]
> **Procurement Note:** The LIDAR was sourced via **Robotistan**, while the Jetson and drive components were sourced via **OpenZeka**. Both are official distributors in Türkiye, ensuring warranty support for your graduation project.

