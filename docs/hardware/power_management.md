
## 🔋 Battery Specifications: 3S LiPo

The system is powered by a high-capacity **3S (3-Cell) Lithium Polymer (LiPo)** battery designed for long-duration autonomous testing.

| Parameter | Specification |
| --- | --- |
| **Capacity** | 5500 mAh |
| **Nominal Voltage** | 11.1V (3.7V per cell) |
| **Max Voltage** | 12.6V (4.2V per cell) |
| **Storage Voltage** | 11.4V (3.8V per cell) |
| **Discharge Rating** | ~35C - 50C (Estimated) |

---

## 🏗️ Power Distribution Architecture

The electrical system is split into three isolated rails to prevent the high-frequency noise of the motors from affecting the AI inference logic.

### 1. High-Power Actuator Rail (11.1V - 12.6V)

* **Source:** Direct connection from the 3S LiPo XT60 connector.
* **Loads:** **BTS7960B 43A Motor Driver** and the **RS775 DC Motors**.
* **Safety:** Connects to the **B+ and B-** terminals of the BTS7960.

### 2. Logic Rail (5.1V)

* **Converter:** **XL4005 DC-DC Buck Converter**.
* **Settings:** Input (11.1V) → Output (5.1V / 5A).
* **Loads:** **NVIDIA Jetson Orin Nano**, **RPLIDAR A1**, and the **USB Hub**.
* **Note:** Set the voltage slightly higher than 5.0V (to 5.1V) to account for voltage drops across USB cables under load.

### 3. Servo Rail (6.0V)

* **Converter:** Secondary **XL4005** or dedicated BEC.
* **Loads:** **DSSERVO DS3235 (35kg)**.
* **Rationale:** This high-torque servo can draw up to 3A during rapid cornering. Powering it separately prevents "brownouts" on the Jetson's logic rail.

---

## 🔌 Wiring Guide: Component Integration

### XL4005 Buck Converter Setup

1. Connect the LiPo leads to the **IN+** and **IN-** terminals.
2. Use a multimeter to adjust the onboard potentiometer until the **OUT+** reads exactly **5.1V**.
3. Connect the **OUT+** to the Jetson's 5V DC barrel jack or GPIO pins (Pins 2 or 4).

### BTS7960B Motor Driver Integration

* **VCC:** Connect to the Arduino's 5V pin for logic.
* **GND:** Connect to the **Common Star Ground**.
* **RPWM / LPWM:** Connect to Arduino Drive Node (D5/D6).
* **R_EN / L_EN:** Connect to Arduino Drive Node (D4).
* **B+ / B-:** Direct LiPo connection.
* **M+ / M-:** Output to the **RS775 Motors**.

---

## ⚠️ Safety Protocols & Maintenance

> [!DANGER]
> **Low Voltage Cutoff (LVC):** Never let your 3S LiPo drop below **3.0V per cell (9.0V total)**. Use a LiPo buzzer set to **3.4V per cell** to avoid permanent battery damage.

### 1. The Star Ground Rule

To ensure sensor accuracy (especially the **RPLIDAR A1** and **IMU**), all ground wires must meet at a single point near the battery connector.

* **DO NOT** daisy-chain ground wires from the motor driver to the Jetson.

### 2. Heat Management

* The **BTS7960B** and **XL4005** can get hot during intensive RL training sessions.
* **Maintenance:** Check the heat sinks for the **Creality Apple Green PLA+** decks to ensure they aren't deforming the plastic.

### 3. Charging Procedure

* Always use a balance charger in **Balance Charge** mode at **1C (5.5A)**.
* Never leave the 5500mAh LiPo charging unattended.
* Store in a LiPo-Safe bag when not in use.

---

## 📊 Power Budget Consumption (Idle vs. Peak)

| Component | Idle Current | Peak Current |
| --- | --- | --- |
| Jetson Orin Nano | 0.8A | 2.5A |
| RPLIDAR A1 | 0.1A | 0.5A |
| DS3235 Servo | 0.1A | 3.2A |
| Dual RS775 Motors | 2.0A | 25.0A+ |
| **Estimated Total** | **~3.0A** | **~31.4A** |

**Would you like me to create a "Software Installation" guide next for the Jetson Orin Nano, including ROS2 and the LIDAR drivers?**