# GPIO Configuration

## Overview

The 40-pin expansion header on the Jetson Orin Nano is configured as input mode by default. To configure GPIO pins for output or alternative functions, you need to create and apply Device Tree Overlays.

## Prerequisites

- Jetson Orin Nano with JetPack installed
- Root access (sudo privileges)
- Device Tree Compiler (dtc)

## Pin Reference

Refer to the [official GPIO pinout diagram](https://jetsonhacks.com/nvidia-jetson-orin-nano-gpio-header-pinout/) to identify the pin numbers and their corresponding functions on the 40-pin header.

## Configuration Steps

### 1. Identify Required Pins

Review the pinout diagram and determine which GPIO pins you need to configure for your application.

### 2. Create Device Tree Overlay

1. Clone the sample overlay repository:
   ```bash
   git clone https://github.com/jetsonhacks/jetson-orin-gpio-patch
   cd jetson-orin-gpio-patch
   ```

2. Modify the device tree source file (`.dts`) according to your requirements. Use the sample files as a template.

3. Compile the device tree overlay:
   ```bash
   dtc -O dtb -o <your-filename>.dtbo <your-filename>.dts
   ```

### 3. Install the Overlay

1. Copy the compiled overlay to the boot directory:
   ```bash
   sudo cp <your-filename>.dtbo /boot
   ```

2. Launch the Jetson IO configuration tool:
   ```bash
   sudo /opt/nvidia/jetson-io/jetson-io.py
   ```

3. Select your custom overlay from the list
4. Choose the option to reboot the system
5. The changes will take effect after the system restarts

## Verification

After rebooting, you can verify the GPIO configuration using the `gpioinfo` command or by testing your specific pins with your application.

## Notes

- Device Tree Overlays provide a permanent solution for GPIO configuration
- Always backup your configuration files before making changes
- Incorrect device tree configurations may prevent the system from booting properly