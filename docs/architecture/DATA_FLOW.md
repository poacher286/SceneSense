# SceneSense Data Flow

> **Version:** 1.0  
> **Status:** Active  
> **Audience:** Developers & Contributors

---

# Table of Contents

1. Purpose
2. High-Level Data Flow
3. Pipeline Overview
4. Step 1 - Screen Capture
5. Step 2 - Scene Recognition
6. Step 3 - Scene Stabilization
7. Step 4 - Decision Engine
8. Step 5 - Event Bus
9. Step 6 - Device Controller
10. Step 7 - ESP32
11. Complete Example
12. Data Objects
13. Event Definitions
14. Thread Communication
15. Error Flow
16. Future Expansion

---

# Purpose

This document describes how information moves through the SceneSense application.

Unlike traditional software where modules directly call one another, SceneSense transforms data into progressively higher-level information until a hardware action is produced.

Think of it as a perception pipeline.

```
Pixels

↓

Meaning

↓

Decision

↓

Action
```

---

# High-Level Data Flow

```
┌─────────────────────┐
│     Game Window     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Screen Capture     │
└──────────┬──────────┘
           │ Frame
           ▼
┌─────────────────────┐
│ Scene Recognition   │
└──────────┬──────────┘
           │ Prediction
           ▼
┌─────────────────────┐
│ Scene Stabilizer    │
└──────────┬──────────┘
           │ Stable Scene
           ▼
┌─────────────────────┐
│ Decision Engine     │
└──────────┬──────────┘
           │ Event
           ▼
┌─────────────────────┐
│ Event Bus           │
└───────┬─────┬───────┘
        │     │
        ▼     ▼
   UI Dashboard
        │
        ▼
Device Controller
        │
        ▼
ESP32
        │
        ▼
Diffuser
```

---

# Pipeline Overview

Each module transforms the previous output into something more meaningful.

| Stage | Input | Output |
|--------|-------|--------|
| Capture | Screen | Frame |
| AI | Frame | Scene Prediction |
| Stabilizer | Prediction | Stable Scene |
| Decision | Stable Scene | Scene Event |
| Device | Scene Event | Serial Command |
| Hardware | Serial Command | Physical Action |

Every stage is independent.

---

# Step 1 — Screen Capture

The Capture module continuously grabs frames from the selected window.

Example:

```
Desktop

↓

RGB Image

↓

1920 x 1080

↓

FrameCapturedEvent
```

Captured frames remain in memory.

No screenshots are written to disk.

---

## Output Object

```python
FrameCapturedEvent

{
    frame: Image,
    timestamp: 1723039200
}
```

---

# Step 2 — Scene Recognition

The AI model receives the frame.

It performs semantic scene classification.

Example:

Input

```
Frame
```

Output

```python
SceneDetectedEvent

{
    scene: "Forest",
    confidence: 0.96
}
```

Notice that the AI returns **meaning**, not actions.

The AI never knows anything about scent.

---

# Step 3 — Scene Stabilization

AI predictions fluctuate.

Example:

```
Forest

Trees

Forest

Forest

Grass

Forest
```

The Stabilizer converts this into:

```
Forest
```

Possible algorithms include:

- Majority voting
- Sliding window
- Confidence threshold
- Exponential smoothing

---

## Output

```python
StableSceneDetectedEvent

{
    scene: "Forest"
}
```

---

# Step 4 — Decision Engine

The Decision Engine determines whether something meaningful has changed.

Example:

Current Scene

```
Forest
```

New Scene

```
Forest
```

Result

```
No Action
```

Example

```
Forest

↓

Rain
```

Result

```
SceneChanged
```

The Decision Engine also handles:

- cooldown timers
- duplicate suppression
- future event rules

---

## Output

```python
SceneChangedEvent

{
    previous: "Forest",
    current: "Rain"
}
```

---

# Step 5 — Event Bus

The Event Bus broadcasts events to interested modules.

Example

```
SceneChanged

↓

Publish

↓

Subscribers
```

Subscribers include:

- Device Controller
- Dashboard
- Logger
- Future plugins

The Event Bus performs no business logic.

It only routes events.

---

# Step 6 — Device Controller

The Device Controller converts a scene into a hardware command.

Example

```
Scene

↓

Forest

↓

Scent

↓

Pine

↓

Command

↓

SPRAY:PINE
```

The mapping is configurable.

The AI never determines which scent should be used.

---

## Output

```python
SerialCommand

{
    command: "SPRAY:PINE"
}
```

---

# Step 7 — ESP32

The ESP32 receives the command.

Example

```
SPRAY:PINE
```

↓

Activate Relay

↓

Pump

↓

Valve

↓

Diffuse Pine Scent

The ESP32 acknowledges completion.

Future versions may report:

- cartridge level
- temperature
- device status
- errors

---

# Complete Example

A user enters a forest in a game.

```
Frame

↓

Capture

↓

FrameCapturedEvent

↓

AI

↓

Forest (96%)

↓

Stabilizer

↓

Forest

↓

Decision Engine

↓

SceneChanged

↓

Event Bus

↓

Device Controller

↓

SPRAY:PINE

↓

ESP32

↓

Diffuser

↓

Pine Scent
```

No module needs to know how another module works internally.

---

# Data Objects

The following objects travel through the system.

---

## FrameCapturedEvent

```python
{
    frame,
    timestamp
}
```

---

## SceneDetectedEvent

```python
{
    scene,
    confidence
}
```

---

## StableSceneDetectedEvent

```python
{
    scene
}
```

---

## SceneChangedEvent

```python
{
    previous_scene,
    current_scene
}
```

---

## ScentRequestedEvent

```python
{
    scent,
    intensity,
    duration
}
```

---

## SerialCommand

```python
{
    command
}
```

---

# Event Definitions

The application publishes the following events.

```
ApplicationStarted

ApplicationStopped

FrameCaptured

SceneDetected

StableSceneDetected

SceneChanged

ScentRequested

CommandSent

DeviceConnected

DeviceDisconnected

DeviceError
```

New modules should subscribe to existing events instead of introducing direct dependencies.

---

# Thread Communication

Each processing stage runs independently.

```
Capture Thread

↓

Queue

↓

AI Thread

↓

Queue

↓

Decision Thread

↓

Queue

↓

Serial Thread
```

This prevents slow AI inference from blocking frame capture.

Queues also simplify back-pressure handling if the AI falls behind.

---

# Error Flow

Errors should remain isolated.

Example

```
AI Error

↓

Log Error

↓

Skip Frame

↓

Continue Processing
```

Another example

```
USB Disconnected

↓

Publish DeviceDisconnected

↓

Retry Connection

↓

Continue Running
```

The system should degrade gracefully.

---

# Future Expansion

The pipeline intentionally separates perception from output.

Today

```
Scene

↓

Pine Scent
```

Tomorrow

```
Scene

↓

Pine Scent

↓

Smart Lights

↓

Fan

↓

Haptic Vest

↓

Fog Machine
```

The Event Bus allows multiple output devices to react to the same scene without changing the AI or Decision Engine.

---

# Design Principles

Every stage should:

- Accept a well-defined input.
- Produce a well-defined output.
- Perform one responsibility.
- Never bypass the Event Bus.
- Avoid direct knowledge of downstream modules.

---

# Summary

SceneSense transforms raw pixels into meaningful physical experiences through a sequence of independent processing stages.

```
Pixels

↓

Semantic Understanding

↓

Stable Context

↓

Meaningful Decision

↓

Standardized Event

↓

Hardware Command

↓

Immersive Experience
```

By treating data as a pipeline rather than tightly coupled function calls, SceneSense remains modular, testable, and extensible. As the project grows, new AI models, devices, or event consumers can be added without redesigning the existing architecture.