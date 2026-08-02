# SceneSense Software Architecture

> **Version:** 1.0  
> **Status:** Draft  
> **Audience:** Developers & Contributors

---

# Table of Contents

1. Introduction
2. Architecture Goals
3. High-Level Overview
4. Core Design Principles
5. System Architecture
6. Module Overview
7. Event Flow
8. Data Flow
9. Threading Model
10. Configuration
11. Error Handling
12. Logging
13. Future Extensibility
14. Project Structure

---

# Introduction

SceneSense is an AI-powered desktop application that observes visual content displayed on a computer screen, understands the semantic context of the scene, and generates immersion events for connected hardware devices.

Unlike traditional game integrations, SceneSense does not communicate with game engines, memory, or APIs.

Instead, it relies solely on visual perception.

```
Observe

↓

Understand

↓

Decide

↓

Trigger
```

This document describes the overall software architecture and the responsibilities of each subsystem.

---

# Architecture Goals

The architecture is designed around five primary goals.

## 1. Modular

Each module has one responsibility.

Modules should be independently replaceable.

---

## 2. Event Driven

Modules communicate through events instead of direct dependencies.

This minimizes coupling.

---

## 3. Local First

Everything runs on the user's computer.

No gameplay data leaves the machine.

---

## 4. AI Agnostic

The application should support replacing the AI model without changing the rest of the system.

---

## 5. Output Agnostic

The AI understands scenes.

Hardware reacts to scenes.

The AI never controls hardware directly.

---

# High-Level Overview

```
                    +----------------------+
                    |      Game Window     |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |   Screen Capture     |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |  Scene Recognition   |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Scene Stabilization  |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |  Decision Engine     |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |   Event Bus          |
                    +----------+-----------+
                               |
             +-----------------+----------------+
             |                                  |
             v                                  v
    +------------------+              +------------------+
    | Device Controller|              | Desktop UI       |
    +------------------+              +------------------+
             |
             v
      +--------------+
      | ESP32 Device |
      +--------------+
```

---

# Core Design Principles

## Separation of Responsibilities

Every module performs exactly one task.

| Module | Responsibility |
|---------|----------------|
| Capture | Obtain frames |
| AI | Understand frames |
| Stabilizer | Remove noisy predictions |
| Decision | Determine meaningful events |
| Device | Communicate with hardware |
| UI | Display system status |

---

## Event Driven

Modules never call each other directly.

Instead, modules publish and subscribe to events.

Example:

```
FrameCaptured

↓

SceneDetected

↓

SceneChanged

↓

ScentTriggered

↓

CommandSent
```

Advantages:

- Easier testing
- Better debugging
- Better scalability
- Easier hardware expansion

---

## Replaceable Components

Every module should be replaceable without affecting the rest of the application.

Examples:

Replace

```
CLIP
```

with

```
Florence-2
```

No other module changes.

Replace

```
USB
```

with

```
Bluetooth
```

Decision engine remains unchanged.

---

# System Architecture

```
                ┌────────────────────┐
                │   Configuration    │
                └─────────┬──────────┘
                          │
                          ▼

                 ┌────────────────────┐
                 │ Screen Capture     │
                 └─────────┬──────────┘
                           │ Frame
                           ▼

                 ┌────────────────────┐
                 │ Scene Recognition  │
                 └─────────┬──────────┘
                           │ Prediction
                           ▼

                 ┌────────────────────┐
                 │ Scene Stabilizer   │
                 └─────────┬──────────┘
                           │ Stable Scene
                           ▼

                 ┌────────────────────┐
                 │ Decision Engine    │
                 └─────────┬──────────┘
                           │ Event
                           ▼

                 ┌────────────────────┐
                 │ Event Bus          │
                 └──────┬───────┬─────┘
                        │       │
                        ▼       ▼
               Device Controller UI
```

---

# Module Overview

## 1. Screen Capture

Responsibilities:

- Capture frames
- Resize frames
- Convert to RGB
- Publish FrameCaptured event

Does NOT:

- Perform AI
- Save screenshots
- Trigger hardware

---

## 2. Scene Recognition

Responsibilities:

- Run AI model
- Produce semantic labels
- Return confidence score

Example output:

```
Scene

Forest

Confidence

96%
```

---

## 3. Scene Stabilizer

AI predictions fluctuate.

The stabilizer smooths predictions.

Example:

```
Forest

Forest

Trees

Forest

↓

Forest
```

Possible algorithms:

- Majority vote
- Sliding window
- Confidence threshold
- Exponential smoothing

---

## 4. Decision Engine

Determines whether a scene transition occurred.

Example:

```
Forest

↓

Rain
```

Trigger event.

Example:

```
Forest

↓

Forest
```

Ignore.

Responsibilities:

- Cooldowns
- Transition detection
- Event generation

---

## 5. Event Bus

Acts as the communication backbone.

Example:

```
SceneChanged

↓

Subscribers
```

Subscribers:

- UI
- Device Controller
- Logger
- Future plugins

The Event Bus should not contain business logic.

---

## 6. Device Controller

Receives events.

Converts them into protocol messages.

Example:

```
SceneChanged

↓

SPRAY:PINE
```

Responsibilities:

- Serial communication
- Connection management
- Retry logic

---

## 7. Desktop UI

Displays:

- Current scene
- Confidence
- Connected device
- FPS
- Current scent
- Logs

The UI never performs AI.

---

# Event Flow

```
Capture Thread

↓

FrameCaptured

↓

AI Thread

↓

SceneDetected

↓

Stabilizer

↓

SceneChanged

↓

Decision Engine

↓

ScentTriggered

↓

Device Controller

↓

ESP32
```

---

# Data Flow

```
Image

↓

ScenePrediction

↓

StableScene

↓

ImmersionEvent

↓

HardwareCommand
```

Example:

```
Image

↓

Forest

↓

Forest

↓

SceneChanged

↓

SPRAY:PINE
```

Each stage transforms the data into a higher-level abstraction.

---

# Threading Model

To keep the UI responsive and maximize throughput, SceneSense separates work into dedicated threads.

| Thread | Responsibility |
|---------|----------------|
| Capture Thread | Capture frames |
| AI Thread | Run model inference |
| Decision Thread | Process scene changes |
| UI Thread | Render dashboard |
| Serial Thread | Communicate with ESP32 |

Threads communicate through queues and events.

This prevents slow AI inference from blocking screen capture or UI updates.

---

# Configuration

Configuration should be externalized.

Examples:

```
capture:
    fps: 5

ai:
    model: clip

decision:
    cooldown: 15

device:
    port: COM3

ui:
    dark_mode: true
```

Configuration should never be hardcoded.

---

# Error Handling

Modules should fail independently.

Example:

```
AI Failure

↓

Retry

↓

Log Error

↓

Continue Running
```

The application should not crash because one frame fails inference.

Similarly, temporary hardware disconnections should not terminate the application.

---

# Logging

Every significant event should be logged.

Examples:

```
Application Started

Device Connected

Scene Changed

Prediction Updated

Command Sent

Device Disconnected

Application Closed
```

Logs are essential for debugging AI behavior and hardware interactions.

---

# Future Extensibility

The architecture is intentionally designed to support additional output devices.

Future subscribers to the Event Bus may include:

- RGB lighting
- Smart fans
- Haptic devices
- Fog machines
- Smart home systems

No changes to the AI pipeline should be required.

---

# Project Structure

```
SceneSense/

src/
└── scenesense/
    ├── ai/
    ├── capture/
    ├── config/
    ├── decision/
    ├── device/
    ├── events/
    ├── stabilizer/
    ├── ui/
    ├── common/
    └── main.py

docs/
tests/
models/
assets/
scripts/
firmware/
```

Each package represents a logical subsystem.

Internal dependencies should always point **toward** abstractions (events and interfaces), never directly into another module's implementation.

---

# Architecture Summary

SceneSense is built around a simple pipeline:

```
Observe

↓

Understand

↓

Stabilize

↓

Decide

↓

Publish Event

↓

React
```

This architecture keeps the system modular, testable, and extensible.

By separating perception from hardware control, SceneSense can evolve from a scent prototype into a general-purpose immersive computing platform without requiring fundamental architectural changes.