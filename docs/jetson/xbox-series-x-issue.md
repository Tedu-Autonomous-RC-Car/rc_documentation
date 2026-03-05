# Xbox Series X Controller Bluetooth Compatibility Issue

## Overview

This document addresses the Bluetooth Low Energy (BLE) compatibility limitation with the Jetson Orin Nano's wireless adapter and provides alternative solutions for game controller connectivity.

## Issue Description

**Problem**: The Intel® Dual Band Wireless-AC 8265 network adapter installed on the Jetson Orin Nano does not support Bluetooth Low Energy (BLE) protocol.

**Impact**: Controllers that rely on BLE for wireless connectivity cannot be connected via Bluetooth.

**Affected Devices**:
- Xbox Series X Controller
- Xbox Series S Controller
- Other BLE-based game controllers

## Workaround Solutions

### Option 1: Wired Connection

Connect BLE-based controllers (such as Xbox Series X) using a USB cable.

**Advantages**:
- Reliable connection
- No latency issues
- No battery concerns

### Option 2: Classic Bluetooth Controllers

Use game controllers that support the classic Bluetooth protocol instead of BLE.

**Compatible Controllers**:
- Sony DualShock 4
- Other controllers with classic Bluetooth support

## Post-Connection Configuration

After connecting any controller (wired or wireless), you must reconfigure the key mappings.

### Using jstest-gtk

1. Install jstest-gtk if not already installed:
   ```bash
   sudo apt-get install jstest-gtk
   ```

2. Launch the configuration tool:
   ```bash
   jstest-gtk
   ```

3. Select your controller from the device list

4. Remap the buttons and axes as needed

5. Save the configuration

!!! warning "Deadzone Configuration"
    Pay special attention to the deadzone settings during configuration. Improper deadzone values can result in unwanted stick drift or reduced precision.

## Technical Details

**Network Adapter**: Intel® Dual Band Wireless-AC 8265  
**Bluetooth Version**: Classic Bluetooth (not BLE)  
**Limitation**: No Bluetooth Low Energy support

## Summary

| Connection Method | Xbox Series X | DualShock 4 | Other BLE Controllers |
|------------------|---------------|-------------|----------------------|
| Wireless (BLE)   | ❌ Not Supported | ✅ Supported | ❌ Not Supported |
| Wired (USB)      | ✅ Supported | ✅ Supported | ✅ Supported |