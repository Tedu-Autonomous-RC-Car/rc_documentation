
# 🚀 Getting Started

This guide will help you set up the development environment for the TAVP Autonomous RC Car. Follow these steps to ensure your system is compatible with our ROS2 stack and hardware interface.

## 📋 Prerequisites

Before starting, ensure your machine (Host PC or Jetson) meets these requirements:

* **OS:** Ubuntu 22.04 LTS (Jammy Jellyfish)
* **Middleware:** ROS2 Humble Hawksbill
* **Python:** 3.10+ (Note: Development on the documentation repo uses 3.12+)

---

## 1. System Workspace Setup

First, create a dedicated ROS2 workspace for the project.

```bash
# Create the workspace directory
mkdir -p ~/tavp_ws/src
cd ~/tavp_ws/src

# Clone the main documentation and sub-modules
git clone https://github.com/Tedu-Autonomous-RC-Car/rc_documentation.git

```

---

## 2. Install Dependencies

We use a specific set of tools for AI inference and embedded communication.

### Python Libraries

Install the core requirements for the documentation and the Jetson control logic:

```bash
cd ~/tavp_ws/src/rc_documentation
pip install -r requirements.txt

```

### ROS2 Packages

Install the necessary ROS2 drivers for our sensors and serial communication:

```bash
sudo apt update
sudo apt install ros-humble-joy ros-humble-teleop-twist-joy \
                 ros-humble-serial-driver ros-humble-v4l2-camera \
                 ros-humble-urg-node # If using Hokuyo LIDAR

```

---

## 3. Hardware Permissions (Critical)

To allow the Jetson to communicate with the **two Arduinos** without `sudo` every time, you must add your user to the `dialout` group.

```bash
sudo usermod -a -G dialout $USER
# REBOOT your machine after running this!

```

### Identifying the Arduinos

Since we have two Arduinos (Steering and Drive), we use **udev rules** to fix their names. Create a new rules file:

```bash
sudo nano /etc/udev/rules.d/99-arduino.rules

```

Add these lines (Update the `idProduct` based on your specific Arduino models):

```text
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", SYMLINK+="ttySteering"
SUBSYSTEM=="tty", ATTRS{idVendor}=="2341", SYMLINK+="ttyDrive"

```

---

## 4. Building the Project

Once the dependencies are installed, build the workspace using `colcon`.

```bash
cd ~/tavp_ws
colcon build --symlink-install
source install/setup.bash

```

---

## 5. Documentation Development

If you are contributing to this documentation site, you can run a local preview server:

```bash
cd ~/tavp_ws/src/rc_documentation
mkdocs serve

```

Your live preview will be available at `http://127.0.0.1:8000`.

---

## 🛠 Troubleshooting Common Issues

* **Serial Port Busy:** Ensure no other serial monitors (like Arduino IDE) are open.
* **ModuleNotFoundError:** Ensure you have activated your Python virtual environment if you are using one.
* **Build Failure:** Check that you have sourced your ROS2 installation: `source /opt/ros/humble/setup.bash`.
