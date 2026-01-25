# RPLidar Configuration

## Overview
This guide provides instructions for setting up and configuring the RPLidar sensor on the Jetson Orin Nano with ROS 2.

## Prerequisites
- Jetson Orin Nano with ROS 2 Humble installed
- RPLidar A1M8 sensor
- USB connection to the Jetson

## Setup Instructions

### 1. Create ROS 2 Workspace

First, create a development workspace for ROS 2. If the Jetson hasn't been reset, the source code from GitHub should already be present in `~/ros2_ws/src`.

If the workspace doesn't exist, create it:

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
```

### 2. Clone RPLidar ROS 2 Package

Clone the official RPLidar ROS 2 repository from Slamtec:

```bash
git clone -b ros2 https://github.com/Slamtec/rplidar_ros.git
```

### 3. Build the Workspace

Navigate to the workspace root and build the package:

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
colcon build --symlink-install
```

**Note:** The Jetson Orin Nano is configured with ROS 2 Humble distribution.

### 4. Source the Workspace

After building, source the workspace setup file:

For bash users:
```bash
source ./install/setup.bash
```

For zsh users:
```bash
source ./install/setup.zsh
```

### 5. Launch the RPLidar Node

To start the RPLidar node and visualize the data:

```bash
ros2 launch rplidar_ros view_rplidar_a1_launch.py
```

This command launches the RPLidar A1 node along with RViz2 for real-time visualization of the lidar data.

## Troubleshooting

If you encounter permission issues with the USB device, add your user to the dialout group:

```bash
sudo usermod -a -G dialout $USER
```

Then log out and log back in for the changes to take effect.