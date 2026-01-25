
# TAVP: TED Autonomous Vehicle Project

Welcome to the central documentation hub for **TAVP**. This project aims to develop a 1/10th scale autonomous racing car capable of navigating complex environments using Reinforcement Learning and Computer Vision.

## 🏎 Project Vision
Our goal is to implement a robust autonomous stack on a Husqvarna Svartpilen-inspired RC platform, utilizing the **NVIDIA Jetson Orin Nano** for high-level AI and **STM32** for low-level real-time control.

## 🏗 System Overview

```mermaid
graph TD
    subgraph "High-Level Processing (Jetson Orin Nano)"
        A[Camera/LIDAR] --> B{ROS2 Stack}
        B --> C[Vision Module]
        B --> D[RL Agent - SAC/PPO]
    end

    subgraph "Low-Level Control (STM32)"
        D -->|Serial/UART| E[Drive Controller]
        E --> F[Servo/Motor]
    end

    F -->|Telemetry| B
```