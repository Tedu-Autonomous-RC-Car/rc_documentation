# 🛠️ Chassis & Mechanical Design Guide

This page serves as the technical reference for the physical assembly of the **TAVP Autonomous RC Car**. Documenting the mechanical integrity is just as critical as the AI for ensuring a stable racing platform.

---

## 🏗️ 1. Structural Overview

* **Chassis Type:** Describe the base RC frame being used.
* **Modifications:** Detail any cuts, extensions, or reinforcements made to the original frame.
* **Material Choice:** Explain the use of **Creality Ender PLA+** for custom parts. Mention why PLA+ was chosen over standard PLA (e.g., higher impact resistance and durability for high-speed runs).

## ⚙️ 2. Custom 3D Printed Components

List all custom-designed parts. For each part, your team member should include:

* **Component Name:** (e.g., Jetson Mounting Deck, LIDAR Tower, Camera Bracket).
* **Design Rationale:** Why is it shaped this way? (e.g., "The LIDAR tower is elevated by 5cm to clear the front wheels and avoid signal occlusion").
* **Print Settings:**
* **Infill:** (e.g., 40% Gyroid for strength).
* **Wall Count:** (e.g., 4 walls for structural rigidity).
* **Filament Used:** Creality Apple Green PLA+.



## 🏎️ 3. Drivetrain & Suspension

* **Motor Integration:** Detail the mounting of the **RS775 DC Motors**.
* **Bearings:** Specify the placement of the **MR105ZZ Miniature Ball Bearings** within the wheel hubs or transmission.
* **Suspension Tuning:** Document any changes to the spring rates or oil viscosity in the shocks to account for the added weight of the **Jetson Orin Nano** and the **3S/4S LiPo battery**.

## 📏 4. Technical Drawings & Dimensions

* **Weight Distribution:** Provide the final weight of the car and the Center of Mass (CoM).
* **Dimensions:** Width, length, and wheelbase in millimeters.
* **Clearance:** Ground clearance, especially regarding the bottom-mounted components.

## 🤝 5. Assembly Instructions

A step-by-step guide for rebuilding the chassis if a component breaks during testing:

1. Base frame preparation.
2. Drivetrain and bearing installation.
3. Mounting the lower electronics deck.
4. Installing the sensor towers (LIDAR and Camera).

---

### Tips for the Mechanical Lead:

> [!TIP]
> **CAD Integration:** Encourage them to export "Exploded View" images from Fusion360 or SolidWorks to put into this page. It makes the documentation look professional for the **November 2026 graduation** presentation.


This troubleshooting and maintenance guide is designed for the mechanical lead of the **TAVP project**. It focuses on the specific hardware components you've procured, such as the **PLA+ 3D printed parts**, **RS775 motors**, and **MR105ZZ bearings**.

---

# 🔧 Mechanical Troubleshooting & Maintenance

High-speed autonomous testing puts significant stress on the chassis. Use this guide to identify, document, and resolve mechanical failures during the development of the TAVP RC car.

## 🛠️ 1. 3D Printed Component Issues (PLA+)

Since the chassis relies on **Creality Ender PLA+** for structural decks and sensor towers, monitor these specific failure points:

| Issue | Potential Cause | Recommended Fix |
| --- | --- | --- |
| **Layer Delamination** | Low print temperature or high stress on the **LIDAR tower**. | Increase print temperature by 5°C; check infill density. |
| **Heat Deformation** | The **Jetson Orin Nano** or **BTS7960 driver** is overheating the mounting deck. | Install thermal spacers or add active cooling (fans) to the electronics deck. |
| **Impact Cracking** | PLA+ is tough, but high-speed collisions exceed its limit. | Increase "Wall Count" to 6-8 in CAD; consider TPU for front bumpers. |
| **Warping** | Uneven cooling during the print of the large main chassis plates. | Use a heated bed (60°C) and ensure a draft-free printing environment. |

---

## ⚙️ 2. Drivetrain & Actuation

The **RS775 DC Motors** and **DSSERVO 35kg servo** provide high power, which can lead to rapid wear on moving parts.

| Symptom | Diagnosis | Solution |
| --- | --- | --- |
| **High-Pitched Grinding** | Gear misalignment or debris in the **MR105ZZ bearings**. | Clean and lubricate bearings; re-align motor pinion gear. |
| **Steering Jitter** | Mechanical binding in the steering linkage or servo horn slip. | Ensure the **DSSERVO DS3235** is securely mounted with Loctite on the horn screw. |
| **Reduced Traction** | Differential wear or suspension bottoming out due to **3S/4S LiPo** weight. | Adjust spring preload; check for oil leaks in the shocks. |
| **Motor Overheating** | The **RS775** is drawing too much current due to high gear ratios. | Check for drivetrain friction; verify **BTS7960** current limits. |

---

## 📋 3. Pre-Test Maintenance Checklist

The mechanical team should perform this "Bolt-Check" before every autonomous run:

* **[ ] Fasteners:** Check that all M3 screws in the **3D printed decks** are snug; PLA+ can "creep" under pressure.
* **[ ] Bearings:** Spin the wheels manually to ensure the **MR105ZZ bearings** move freely without resistance.
* **[ ] Sensor Alignment:** Verify the **RPLIDAR A1** is perfectly level; even a 2° tilt will cause "ground hits" in the laser scan.
* **[ ] Battery Security:** Ensure the **3S/4S LiPo** is strapped down; a shifting battery will change the car's Center of Mass (CoM) and ruin RL training.

---

## 📈 4. Documentation Strategy

The mechanical lead should record every failure in the `docs/hardware/chassis_mechanical.md` page using this format:

> **Failure Log:** [Date] - [Component] - [Cause] - [Resolution]
