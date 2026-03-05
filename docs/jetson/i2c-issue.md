# I2C Bus Configuration Issue

## Overview

This document describes a known issue with I2C Bus 1 on the Jetson platform and provides the recommended workaround for I2C device connections.

## Issue Description

**Problem**: I2C Bus 1 is currently non-functional on the Jetson system.

**Affected Pins**:
- Pin 27 (SDA) - Not operational
- Pin 28 (SCL) - Not operational

## Workaround Solution

### Using I2C Bus 7

Due to the Bus 1 issue, **all I2C protocol devices must be connected to I2C Bus 7**.

**Bus 7 Pin Configuration**:
- **Pin 3**: SDA (Serial Data)
- **Pin 5**: SCL (Serial Clock)

### Detecting Connected Devices

To identify the addresses of devices connected to Bus 7, use the following command:

```bash
sudo i2cdetect -y -r 7
```

**Command Breakdown**:
- `-y`: Disable interactive mode (auto-yes to warnings)
- `-r`: Use SMBus read byte command for probing
- `7`: Target bus number

## Additional Resources

For detailed GPIO header pinout information, refer to the official JetsonHacks documentation:

[NVIDIA Jetson Orin Nano GPIO Header Pinout](https://jetsonhacks.com/nvidia-jetson-orin-nano-gpio-header-pinout/)

## Important Notes

!!! warning "Connection Requirement"
    Ensure all I2C devices are connected to Bus 7 (pins 3 and 5) to avoid connectivity issues. Do not attempt to use Bus 1 until this issue is resolved.