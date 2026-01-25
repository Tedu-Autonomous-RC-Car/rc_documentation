# WiFi Connectivity Issues

## Problem Description

The Intel® Dual Band Wireless-AC 8265 network adapter may not function properly out of the box or may stop working unexpectedly on Jetson devices running Ubuntu 22.04.

## Diagnostic Steps

### 1. Verify Network Card Recognition

First, confirm that the network card is correctly recognized by the system:

```bash
lspci -v
```

Look for the Intel Wireless-AC 8265 adapter in the output. This confirms the hardware is detected at the PCI level.

## Solution

### Step 1: Download Latest Firmware

Download the latest firmware for the Intel 8265 adapter:

```bash
wget https://wireless.wiki.kernel.org/_media/en/users/drivers/iwlwifi-8265-ucode-22.361476.0.tgz
```

### Step 2: Extract and Install Firmware

Extract the firmware archive and copy the firmware file to the system firmware directory:

```bash
tar -xzf iwlwifi-8265-ucode-22.361476.0.tgz
sudo cp iwlwifi-8265-ucode-22.361476.0/*.ucode /lib/firmware/
```

### Step 3: Install Backport Modules (if required)

For Ubuntu 22.04 with kernel version 5.15, the iwlwifi module requires backport installation:

```bash
sudo apt update
sudo apt install iwlwifi-modules
```

**Note:** The iwlwifi module was integrated as a built-in component in kernel versions >5.19. For earlier kernels (such as 5.15 on Ubuntu 22.04), the backports package is necessary.

### Step 4: Reboot the System

After installing the firmware and modules, reboot the Jetson to apply the changes:

```bash
sudo reboot
```

## Verification

After rebooting, verify that the WiFi adapter is functioning:

```bash
nmcli device status
```

The WiFi adapter should appear in the list with an "available" or "connected" state.

## Additional Resources

For more detailed information and community discussion, refer to:
- [NVIDIA Developer Forum - Intel Wireless 8265/8275 Network Card Issue](https://forums.developer.nvidia.com/t/issue-with-intel-wireless-8265-8275-network-card-on-ubuntu-22-04/279938)
