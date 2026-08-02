# SceneSense Diffuser System

> **Version:** 1.0  
> **Status:** Phase 1 Design  
> **Module:** `hardware`

---

# Table of Contents

1. Purpose
2. Vision
3. Design Goals
4. Diffuser Overview
5. How It Works
6. System Components
7. Airflow Design
8. Scent Delivery
9. Cartridge System
10. Fan System
11. Control Electronics
12. Mechanical Design
13. Safety
14. Maintenance
15. Testing
16. Future Improvements

---

# Purpose

The diffuser is the physical device responsible for delivering scents into the user's environment.

It receives commands from the ESP32 and converts them into controlled bursts of fragrance.

The diffuser is the final stage of the SceneSense pipeline.

```text
Game

↓

Scene Detection

↓

Decision Engine

↓

ESP32

↓

Diffuser

↓

User Experiences Scent
```

Unlike conventional aroma diffusers that continuously release fragrance, the SceneSense diffuser delivers **short, precise, event-driven scent bursts** synchronized with gameplay.

---

# Vision

The long-term vision is to build a compact desktop device capable of reproducing environmental scents in real time.

Examples:

| Scene | Scent |
|--------|--------|
| Forest | Pine |
| Rain | Petrichor |
| Ocean | Sea Breeze |
| Campfire | Wood Smoke |
| Snow | Cold Air |
| Desert | Dry Sand |
| Flower Field | Floral |

The user should perceive scents as subtle environmental cues rather than overpowering room fragrances.

---

# Design Goals

The diffuser should be:

- Compact
- Quiet
- Modular
- Safe
- Easy to refill
- Easy to clean
- Low power
- Fast responding
- Replaceable
- Expandable

---

# High-Level Architecture

```text
Desktop App

↓

ESP32

↓

Fan Controller

↓

Cartridge Valve

↓

Airflow

↓

User
```

---

# Phase 1 Objectives

Phase 1 focuses on proving the concept.

Features:

- USB powered
- One fan
- Multiple scent cartridges
- One active scent at a time
- Fixed airflow
- Manual cartridge replacement

The objective is reliability rather than maximum realism.

---

# Diffusion Workflow

```text
Scene Detected

↓

Pine Selected

↓

ESP32 Receives Command

↓

Open Pine Valve

↓

Start Fan

↓

Diffuse for 2 Seconds

↓

Close Valve

↓

Stop Fan
```

---

# System Components

The diffuser consists of:

```
Housing

Fan

Air Chamber

Cartridge Rack

Valve System

ESP32

Power Supply

USB Interface
```

---

# Airflow Design

The diffuser uses forced airflow.

```text
Air Intake

↓

Fan

↓

Selected Cartridge

↓

Mixing Chamber

↓

Outlet Nozzle

↓

User
```

Fresh air passes through the selected scent cartridge and carries the fragrance toward the player.

---

# Why Forced Air?

Compared to passive diffusion:

| Passive | Forced Air |
|----------|------------|
| Slow | Fast |
| Difficult to control | Precise |
| Constant scent | Event-driven |
| Weak response | Strong response |

Forced airflow enables low-latency scent activation.

---

# Scent Delivery

Each scent is released only when requested.

```text
Idle

↓

Valve Opens

↓

Air Passes Through Cartridge

↓

Fragrance Released

↓

Valve Closes
```

No scent should leak while idle.

---

# Cartridge Rack

Phase 1 supports multiple cartridges.

Example:

```text
+---------------------------+
| Pine      Ocean           |
| Rain      Smoke           |
| Floral    Neutral         |
+---------------------------+
```

Only one cartridge is active at any given time.

---

# Air Mixing Chamber

The mixing chamber smooths airflow before it exits the diffuser.

Benefits:

- Uniform scent output
- Reduced turbulence
- Lower fan noise
- More natural scent delivery

---

# Fan System

The fan controls airflow intensity.

Speed levels:

| Level | PWM |
|--------|-----|
| Low | 25% |
| Medium | 50% |
| High | 75% |
| Maximum | 100% |

The Decision Engine determines the requested intensity, while the ESP32 translates it into fan speed.

---

# Fan Placement

Recommended layout:

```text
Air Intake

↓

Fan

↓

Cartridge

↓

Mixing Chamber

↓

Outlet
```

This minimizes scent residue inside the enclosure.

---

# Outlet Design

The outlet should:

- Direct airflow toward the player
- Minimize resistance
- Reduce turbulence
- Prevent scent buildup

An adjustable nozzle is recommended for future versions.

---

# Valve System

Each cartridge is connected to an independent valve.

```text
Pine

↓

Valve 1
```

```text
Rain

↓

Valve 2
```

```text
Ocean

↓

Valve 3
```

Only the selected valve opens during diffusion.

---

# Cartridge Activation

Example sequence:

```text
Forest Detected

↓

Valve Opens

↓

Fan Starts

↓

Diffuse

↓

Valve Closes

↓

Fan Stops
```

---

# Mechanical Housing

The enclosure should provide:

- Cartridge access
- Air intake
- Air outlet
- USB connector
- Ventilation
- Electronics compartment

Recommended construction:

- 3D printed PLA/PETG (prototype)
- Injection-molded plastic (future production)

---

# Power Requirements

Phase 1:

```
USB-C

5V
```

Power consumers:

- ESP32
- Fan
- Valve drivers
- Status LED

Future versions may use an external power supply for higher airflow.

---

# Noise Reduction

The diffuser should remain unobtrusive during gameplay.

Recommendations:

- Large, low-RPM fan
- Rubber vibration mounts
- Smooth airflow channels
- Balanced fan blades

Target noise level:

```
< 30 dB
```

Comparable to a quiet room.

---

# Scent Persistence

One challenge is lingering scent after activation.

Mitigation strategies:

- Short diffusion bursts
- Fresh-air purge after each activation
- Internal airflow optimization
- Neutral airflow between scents

---

# Cross-Contamination

Prevent mixing of scents by:

- Dedicated airflow paths
- Well-sealed valves
- Automatic purge cycle
- Replaceable cartridges

Future versions may include active cleaning cycles.

---

# Safety Features

The diffuser should include:

- Maximum diffusion duration
- Overcurrent protection
- Fan timeout
- Safe startup state
- Temperature monitoring (future)
- Fault detection

Safety takes priority over scent output.

---

# Maintenance

Routine maintenance:

- Replace cartridges
- Clean air passages
- Inspect fan
- Check valve operation
- Remove dust

Recommended interval:

```
Every 2–3 months
```

Depending on usage.

---

# Cleaning Procedure

1. Power off the device.
2. Remove cartridges.
3. Wipe internal surfaces.
4. Clean the outlet.
5. Reinstall cartridges.
6. Run a purge cycle.

Avoid using harsh chemicals inside the airflow path.

---

# Testing

## Functional Tests

Verify:

- Fan starts correctly
- Correct valve opens
- Correct duration
- Airflow consistency
- No leakage while idle

---

## Performance Tests

Measure:

- Airflow rate
- Fan response time
- Valve response time
- Diffusion duration
- Noise level

---

## Reliability Tests

Run repeated activation cycles:

```
10,000+

Activation Tests
```

Observe:

- Valve wear
- Fan reliability
- Cartridge sealing
- Mechanical stability

---

# Future Improvements

## Variable Airflow

Allow continuous fan speed adjustment based on scent intensity.

---

## Multiple Simultaneous Scents

Support scent blending.

Example:

```text
70% Pine

30% Rain
```

To create richer environments.

---

## Smart Cartridge Detection

Detect installed cartridges automatically using RFID or NFC.

---

## Replaceable Fan Module

Simplify maintenance by allowing quick fan replacement.

---

## Compact Consumer Design

Reduce overall size while improving airflow efficiency.

---

## Wireless Diffuser

Communicate with the desktop application via Wi-Fi or Bluetooth.

---

## Silent Mode

Reduce airflow and fan speed for quieter operation during late-night gaming.

---

# Best Practices

✔ Keep airflow unobstructed

✔ Prevent scent leakage

✔ Use replaceable cartridges

✔ Design for easy maintenance

✔ Prioritize safety

✔ Keep noise low

✔ Minimize scent residue

✔ Build modular components

---

# Example End-to-End Flow

```text
Scene Detection

↓

Forest

↓

Decision Engine

↓

Pine Selected

↓

ESP32

↓

Open Pine Valve

↓

Fan Starts

↓

Air Passes Through Cartridge

↓

Fragrance Released

↓

Fan Stops

↓

Valve Closes
```

---

# Summary

The diffuser is the physical interface between SceneSense's software and the user's senses.

```text
Air

↓

Fan

↓

Cartridge

↓

Mixing Chamber

↓

User
```

Its purpose is not simply to emit fragrance, but to deliver subtle, timely, and repeatable scent cues that enhance immersion without overwhelming the player. By combining controlled airflow, modular cartridges, and reliable hardware control, the diffuser forms the foundation for future multi-scent, adaptive, and highly immersive gaming experiences.

---

# Appendix A – Example Prototype Components

| Component | Suggested Part |
|-----------|----------------|
| Controller | ESP32 DevKit |
| Fan | 40–60 mm PWM Brushless Fan |
| Valve | Mini Solenoid Valve |
| Housing | 3D Printed PLA/PETG |
| Power | USB-C 5V |
| Driver | MOSFET Module |
| Status Indicator | RGB LED |

---

# Appendix B – Phase Evolution

| Version | Capabilities |
|----------|--------------|
| **Phase 1** | USB, single active scent, manual cartridges |
| **Phase 2** | Wireless communication, improved airflow, automatic purge |
| **Phase 3** | Multi-scent blending, smart cartridges, adaptive intensity |
| **Phase 4** | Consumer-ready enclosure, silent operation, companion app |

This phased approach allows SceneSense to validate the core concept early while providing a clear roadmap toward a polished consumer hardware product.