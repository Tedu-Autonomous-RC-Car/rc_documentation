# Jetson Orin Nano Documentation

## Overview

This section contains comprehensive documentation for the NVIDIA Jetson Orin Nano configuration and usage in the RC robot project. The Jetson serves as the onboard computer, running ROS 2 Humble for robot control, sensor integration, and autonomous operation.

## Hardware Specifications

- **Model**: NVIDIA Jetson Orin Nano
- **OS**: Ubuntu 22.04 LTS
- **ROS Version**: ROS 2 Humble
- **GPU**: NVIDIA Ampere architecture with 1024 CUDA cores
- **Memory**: 8GB LPDDR5
- **Storage**: NVMe SSD

## Table of Contents

### Setup and Configuration
- [GPIO Configuration](gpio-config.md) - Configure GPIO pins for motor control and sensors
- [RPLidar Setup](rplidar.md) - Install and configure the RPLidar A1 sensor
- [Teleop Node](teleop-node.md) - Set up teleoperation communication with host computer

### Troubleshooting
- [WiFi Connectivity Issues](wifi-issue.md) - Fix Intel WiFi adapter problems
- [Driver Issues](driver-issue.md) - Recover from critical driver deletion

## Quick Start

### Initial Setup

1. **Flash the Jetson** with Ubuntu 22.04 and JetPack
2. **Install ROS 2 Humble**:
   ```bash
   sudo apt update
   sudo apt install ros-humble-desktop
   ```

3. **Set up the workspace**:
   ```bash
   mkdir -p ~/ros2_ws/src
   cd ~/ros2_ws
   colcon build
   ```

4. **Configure environment** (add to `~/.bashrc`):
   ```bash
   source /opt/ros/humble/setup.bash
   source ~/ros2_ws/install/setup.bash
   export ROS_DOMAIN_ID=0
   ```

### Network Configuration

For communication with the host computer:

1. Connect both devices to the same network
2. Set the same ROS_DOMAIN_ID on both devices
3. Configure firewall rules if needed:
   ```bash
   sudo ufw allow from <host_ip>
   ```

## Development Workflow

1. **Edit code** on the host computer
2. **Transfer files** to Jetson via SSH/SCP or Git
3. **Build** the workspace on Jetson
4. **Test** functionality locally
5. **Deploy** for autonomous operation

## Useful Commands

### System Information
```bash
# Check Jetpack version
sudo apt-cache show nvidia-jetpack

# Monitor system resources
tegrastats

# Check GPU usage
jtop
```

### ROS 2 Operations
```bash
# List active nodes
ros2 node list

# Check topic data
ros2 topic echo /topic_name

# View node information
ros2 node info /node_name
```

## Additional Resources

- [NVIDIA Jetson Documentation](https://docs.nvidia.com/jetson/)
- [JetsonHacks](https://jetsonhacks.com/)
- [ROS 2 Humble Documentation](https://docs.ros.org/en/humble/)

## Next Steps

- Configure GPIO pins for your specific hardware setup
- Set up RPLidar for environment mapping
- Test teleoperation between host and Jetson
- Implement autonomous navigation algorithms