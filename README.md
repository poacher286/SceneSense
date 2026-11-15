# SceneSense

> **Understand the Scene. Enhance the Experience.**

SceneSense is an AI-powered desktop application that analyzes a game's visual output in real time and triggers immersive scent effects based on the player's environment.

Unlike traditional game integrations, SceneSense does **not** require mods, plugins, or access to the game's internal APIs. Instead, it uses semantic scene recognition to understand what the player is experiencing directly from the rendered frames.

The long-term vision is to build a platform capable of driving multiple immersive devices—including scent, lighting, fans, haptics, and environmental effects—from a single AI-powered context engine.

---

## Table of Contents

- [Project Status](#project-status)
- [Vision](#vision)
- [Phase 1 Goal](#phase-1-goal)
- [Features](#features)
- [How SceneSense Works](#how-scenesense-works)
- [Architecture Overview](#architecture-overview)
- [Repository Structure](#repository-structure)
- [Technology Stack](#technology-stack)
- [Development Roadmap](#development-roadmap)
- [Project Principles](#project-principles)
- [Documentation](#documentation)
- [Getting Started](#getting-started)
- [Future Vision](#future-vision)
- [Contributing](#contributing)
- [License](#license)

---

# Project Status

🚧 **Phase 1 – Proof of Concept**

The current goal is to validate the core idea:

1. Capture the active game window.
2. Understand the current environment using AI.
3. Detect meaningful scene transitions.
4. Trigger a scent device through USB.

Everything else is considered future work.

---

# Vision

Most gaming peripherals react only to user input.

SceneSense reacts to **what the player is actually experiencing**.

Instead of reading game memory or relying on game-specific integrations, SceneSense observes the rendered scene just like a human would.

Example:

```
Dense Forest

↓

SceneSense recognizes

Forest

↓

Trigger Pine scent
```

Another example:

```
Heavy Rain

↓

SceneSense recognizes

Rain

↓

Trigger Petrichor scent
```

The AI understands context rather than individual objects.

---

# Phase 1 Goal

Build a working prototype capable of:

- Capturing the game screen
- Running semantic scene recognition
- Producing stable scene predictions
- Triggering scent events
- Communicating with an ESP32 diffuser

Success is measured by demonstrating the complete pipeline rather than supporting many games or scents.

---

# Features

## Current

- Desktop screen capture
- Semantic scene recognition
- Scene stabilization
- Decision engine
- USB serial communication
- Simple desktop dashboard

## Planned

- Event detection (fire, explosions, vehicles)
- Improved AI models
- User-configurable scent mappings
- Multiple scent cartridges
- Better diagnostics

## Future

- HDMI input
- Console support
- Smart lighting
- Fans
- Haptic devices
- Standalone hardware
- Developer SDK

---

# How SceneSense Works

```
Game Window

      │

      ▼

Screen Capture

      │

      ▼

Semantic Scene Recognition

      │

      ▼

Scene Stabilizer

      │

      ▼

Decision Engine

      │

      ▼

Scent Mapping

      │

      ▼

USB Controller

      │

      ▼

ESP32 Diffuser
```

---

# Architecture Overview

SceneSense is divided into independent modules.

```
SceneSense

├── Capture
├── AI
├── Stabilizer
├── Decision Engine
├── Device Controller
├── Configuration
└── Desktop UI
```

Each module has a single responsibility and can be developed or tested independently.

---

# Repository Structure

```
SceneSense/

├── docs/
│
├── src/
│   └── scenesense/
│       ├── capture/
│       ├── ai/
│       ├── stabilizer/
│       ├── decision/
│       ├── device/
│       ├── config/
│       ├── ui/
│       └── common/
│
├── tests/
├── models/
├── scripts/
├── firmware/
└── assets/
```

---

# Technology Stack

## Language

Python 3.12+ (currently using Python 3.12 in development)

---

## Computer Vision

- **OpenCV** (`cv2`): Image preprocessing and analysis
- **MSS**: Lightweight screenshot capture

---

## AI

- **PyTorch**: Deep learning framework
- **Transformers**: Hugging Face models library
- **CLIP**: Vision-language model for scene recognition (Phase 1)
- Future: SigLiP, Florence-2 for enhanced capabilities

---

## UI

- **PySide6**: Desktop dashboard and monitoring interface

---

## Device Communication

- **PySerial**: USB serial communication with ESP32 diffuser
- Protocol: Custom binary protocol defined in `docs/hardware/PROTOCOL.md`

---

## Hardware

- **ESP32**: Wi-Fi/Bluetooth-enabled microcontroller for scent diffuser
- Current: Single output (solenoid valve control)
- Future: Multiple cartridge support, RGB indicators

---

## Logging

- **Loguru**: Structured logging with file rotation
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

---

# Development Roadmap

## Phase 1

Proof of Concept

- Screen Capture
- AI Scene Recognition
- Scene Stabilizer
- USB Communication
- ESP32 Prototype

---

## Phase 2

AI Improvements

- Better models
- Event detection
- Faster inference
- More environments

---

## Phase 3

Platform Features

- Profiles
- Configuration
- Plugin system
- Scene editor

---

## Phase 4

Developer SDK

Allow game developers to emit SceneSense events directly.

---

## Long-Term

Expand SceneSense into a general-purpose immersion platform supporting multiple output devices.

---

# Project Principles

SceneSense follows four guiding principles.

## 1. Scene First

Understand the player's environment from visuals rather than game-specific APIs.

---

## 2. Local First

Gameplay frames never leave the user's computer.

No cloud inference.

No gameplay recording.

---

## 3. Modular

Each subsystem should remain independently replaceable.

Examples:

- Capture module
- AI model
- Hardware controller

---

## 4. Output Agnostic

The AI produces context.

Different devices consume that context.

Today:

- Scent

Tomorrow:

- Lighting
- Fans
- Haptics
- Environmental effects

---

# Documentation

The project documentation is organized into multiple sections.

```
docs/

vision/

architecture/

implementation/

hardware/

research/

development/

adr/
```

Each section focuses on one aspect of the system.

---

# Getting Started

Clone the repository.

```
git clone https://github.com/<username>/SceneSense.git

cd SceneSense
```

Create a virtual environment.

```
python -m venv .venv
```

Activate it.

macOS / Linux

```
source .venv/bin/activate
```

Install dependencies.

```
pip install -r requirements.txt
```

Run the application.

```
python -m scenesense
```

---

# Future Vision

The scent diffuser is only the first output device.

Future versions of SceneSense may control:

- Smart lighting
- Fans
- Temperature
- Fog machines
- Haptic devices
- VR accessories

The AI remains the same.

Only the output devices change.

---

# Contributing

SceneSense is currently under active development.

Contribution guidelines will be published once the core architecture stabilizes.

---

# License

This project is licensed under the MIT License.

---

## Author

Created by **Buland Sahu**

Building the future of AI-powered immersive gaming.