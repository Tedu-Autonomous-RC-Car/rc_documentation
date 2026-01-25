# Teleop Listener Node

## Overview

The `teleopt_listener_node` runs on the Jetson Orin Nano and receives teleoperation commands from the host computer. This guide covers the setup and execution of the node.

## Prerequisites

Before running the node, ensure the following requirements are met:

- Jetson Orin Nano and host computer are connected to the same network
- Both devices are configured to use the same ROS 2 domain ID
- ROS 2 workspace is properly set up with the teleop listener package

## Building the Workspace

Navigate to the workspace root directory (one level above `src`):

```bash
cd ~/ros2_ws  # Adjust path to your workspace
```

Build the workspace to ensure all changes are applied:

```bash
colcon build
```

## Setting Up the Environment

Source the workspace setup script based on your shell:

**For Bash:**
```bash
source install/setup.bash
```

**For Zsh:**
```bash
source install/setup.zsh
```

## Running the Node

Execute the teleop listener node:

```bash
ros2 run teleopt_listener teleopt_listener_node
```

## Network Configuration

### Verify Network Connectivity

Ensure both devices are on the same network:

```bash
ping <host_computer_ip>
```

### ROS Domain ID

Verify that both the Jetson and host computer use the same ROS_DOMAIN_ID. Check the current domain ID:

```bash
echo $ROS_DOMAIN_ID
```

If needed, set the domain ID (add to `~/.bashrc` or `~/.zshrc` for persistence):

```bash
export ROS_DOMAIN_ID=<your_domain_id>
```

## Troubleshooting

- **Node not receiving commands**: Verify network connectivity and ROS_DOMAIN_ID configuration
- **Build errors**: Ensure all dependencies are installed with `rosdep install`
- **Package not found**: Confirm the workspace is properly sourced after building

## Additional Resources

- [ROS 2 Network Configuration](https://docs.ros.org/en/rolling/Concepts/About-Domain-ID.html)
- [ROS 2 Launch and Run Documentation](https://docs.ros.org/en/rolling/Tutorials/Beginner-CLI-Tools/Launching-Multiple-Nodes/Launching-Multiple-Nodes.html)