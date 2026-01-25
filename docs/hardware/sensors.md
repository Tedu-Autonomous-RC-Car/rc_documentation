# 📡 Sensors Documentation

This document provides technical specifications and integration guides for the perception layer of the **TAVP Autonomous RC Car**. All sensors are interfaced via USB to the **NVIDIA Jetson Orin Nano**.

---

## 🏎️ Overview

The car utilizes a hybrid perception stack combining 2D Laser Scanning (LIDAR) for spatial mapping and a Monocular USB Camera for visual processing.

---

## 🔄 RPLIDAR A1 (LIDAR)

The **Slamtec RPLIDAR A1** is a 360-degree 2D laser scanner used for obstacle avoidance and SLAM (Simultaneous Localization and Mapping).

### 🛰️ Technical Specifications

| Parameter | Value |
| --- | --- |
| **Distance Range** | 0.15m – 12m |
| **Angular Range** | 0 – 360 Degree |
| **Sample Frequency** | ≥ 8000 Hz |
| **Scan Rate** | Typical 5.5 Hz (Configurable up to 10 Hz) |
| **Resolution** | < 0.5mm (Distance), ≤ 1° (Angular) |
| **Interface** | UART @ 115200bps (Interfaced via USB Adapter) |

### 🔌 Physical Integration

* **Connection:** Connect the RPLIDAR A1 to the Jetson Orin Nano using the provided Micro-USB to USB-A adapter board.
* **Power:** The sensor draws ~100mA during normal operation and is powered directly via the USB port.

---

## 📷 Vision System (USB Camera)

A generic USB camera is used as the primary sensor for the **Vision** repository's lane detection and object recognition logic.

### 🛠️ Hardware Setup

* **Mounting:** The camera must be mounted at a fixed tilt angle (typically 20°-30°) to maximize the view of the track while maintaining a horizon line for orientation.
* **Interface:** Standard UVC (USB Video Class) interface, compatible with `v4l2` (Video4Linux2) drivers on Linux.

### ⚙️ Calibration Data

> [!NOTE]
> To ensure accurate Reinforcement Learning (RL) training, the camera must be calibrated to remove barrel distortion.

* **Target Resolution:** 640x480 @ 30 FPS.
* **Color Space:** RGB (converted to Grayscale for some lane detection algorithms).

---

## 🔍 USB Device Management (Udev Rules)

Since both sensors use USB, Linux may assign random device names (e.g., `/dev/ttyUSB0` vs `/dev/ttyUSB1`). To ensure the code always finds the correct sensor, we use persistent symlinks.

### Persistent Naming Configuration

1. **Identify the Vendor/Product IDs:**
```bash
lsusb

```


2. **Create a Udev Rule:**
Add the following to `/etc/udev/rules.d/99-tavp-sensors.rules`:
```bash
# RPLIDAR A1 Rule
SUBSYSTEM=="tty", ATTRS{idVendor}="10c4", ATTRS{idProduct}=="ea60", SYMLINK+="ttyLidar"
# USB Camera Rule
SUBSYSTEM=="video4linux", ATTRS{idVendor}=="xxxx", ATTRS{idProduct}=="xxxx", SYMLINK+="videoVision"

```


3. **Permissions:** Run `sudo chmod 666 /dev/ttyLidar` to allow ROS2 nodes to read data without root access.

---

## 🚀 ROS2 Integration

For the TAVP project, we use the following packages to publish sensor data:

* **LIDAR:** `sllidar_ros2` package (publishes to `/scan` topic).
* **Camera:** `v4l2_camera` node (publishes to `/image_raw` topic).
