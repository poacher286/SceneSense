# SceneSense Goals

> **Version:** 1.0  
> **Status:** Active  
> **Scope:** Phase 1 (Proof of Concept)

---

# Table of Contents

1. Purpose
2. Project Goal
3. Vision Goal
4. Phase 1 Goal
5. Functional Goals
6. Technical Goals
7. AI Goals
8. User Experience Goals
9. Performance Goals
10. Architecture Goals
11. Privacy Goals
12. Success Criteria
13. Future Goals

---

# Purpose

This document defines what SceneSense is expected to achieve.

Every feature, design decision, and implementation should contribute toward one or more of these goals.

If a feature does not support these goals, it should be postponed or removed.

---

# Project Goal

Build an intelligent desktop application capable of understanding what is happening on a computer screen and translating that understanding into real-world sensory experiences.

The first sensory output will be scent.

Future outputs may include:

- Lighting
- Fans
- Haptics
- Environmental effects

---

# Vision Goal

Teach computers to understand virtual environments the same way humans do.

Instead of asking:

> "Which objects are visible?"

SceneSense asks:

> "What is the player currently experiencing?"

That semantic understanding becomes the foundation for every output device.

---

# Phase 1 Goal

The objective of Phase 1 is **not** to build a polished product.

The objective is to validate the core concept.

SceneSense should successfully perform the following workflow:

```
Capture Screen

↓

Understand Scene

↓

Detect Scene Change

↓

Map Scene to Scent

↓

Send Command

↓

Activate Diffuser
```

If this workflow works reliably, the core idea is proven.

---

# Functional Goals

SceneSense should be able to:

## Capture the Screen

- Capture the active game window.
- Capture at a configurable frame rate.
- Process frames in memory.
- Avoid recording gameplay.

---

## Understand the Scene

Recognize semantic environments such as:

- Forest
- Rain
- Ocean
- Snow
- Fire

Future environments can be added without changing the overall architecture.

---

## Stabilize Predictions

AI predictions naturally fluctuate.

SceneSense should:

- Smooth predictions
- Ignore brief misclassifications
- Prevent unnecessary scent changes

---

## Trigger Events

When a meaningful scene transition occurs:

```
Forest

↓

Rain
```

SceneSense should generate a single scent event.

Duplicate events should be ignored.

---

## Communicate with Hardware

SceneSense should send commands to an ESP32 over USB Serial.

Example:

```
SPRAY:PINE
```

---

# Technical Goals

The architecture should be:

- Modular
- Testable
- Maintainable
- Extensible
- Platform independent where possible

Each subsystem should have a single responsibility.

Modules should communicate through well-defined interfaces.

---

# AI Goals

The AI system should:

- Run locally
- Support interchangeable models
- Produce semantic scene labels
- Return confidence scores
- Operate in real time

The AI should identify environments rather than individual objects.

Preferred output:

```
Forest
```

Not:

```
Tree

Grass

Rock
```

---

# User Experience Goals

The application should require minimal interaction.

Desired workflow:

1. Launch SceneSense.
2. Select the game window (or detect it automatically in the future).
3. Start playing.
4. SceneSense runs in the background.
5. Scent transitions occur automatically.

The user should not need to configure the application during normal gameplay.

---

# Performance Goals

## Frame Rate

Target:

```
5 FPS
```

Higher frame rates can be explored later if necessary.

---

## Inference

Target AI inference time:

```
<100 ms
```

---

## End-to-End Latency

From screen capture to hardware activation:

```
<1 second
```

---

## Memory Usage

Target:

```
<500 MB
```

---

## CPU Usage

The application should avoid consuming excessive CPU resources while running continuously.

---

# Architecture Goals

The architecture should satisfy the following principles.

## Modular

Every component should be independently replaceable.

Examples:

- AI model
- Screen capture implementation
- Device controller

---

## Event Driven

Modules should communicate using events rather than direct dependencies.

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

DeviceCommandSent
```

This reduces coupling and simplifies future expansion.

---

## Output Agnostic

The AI should produce context rather than device-specific commands.

Example:

Instead of:

```
Spray Pine
```

Produce:

```
Scene = Forest
```

The scent module decides how to respond.

Future hardware modules can subscribe to the same event.

---

# Privacy Goals

User trust is essential.

SceneSense should:

- Never upload gameplay frames.
- Never save screenshots.
- Never record gameplay.
- Perform all inference locally.

Every captured frame should exist only in memory.

```
Capture

↓

Inference

↓

Discard
```

No persistent image storage should occur unless explicitly enabled for debugging.

---

# Success Criteria

Phase 1 is considered successful when the following demonstration works reliably.

1. Launch SceneSense.
2. Start a supported game.
3. Enter a forest environment.
4. Pine scent activates.
5. Walk into a rainy environment.
6. Petrichor scent activates.
7. Remaining in the same environment does not repeatedly trigger the diffuser.

The user should experience seamless transitions without manual intervention.

---

# Future Goals

After Phase 1, SceneSense should expand its capabilities.

## Improved AI

- More environments
- Better confidence
- Faster inference

---

## Event Recognition

Examples:

- Explosion
- Fire
- Campfire
- Vehicle
- Magic
- Lava

These become temporary immersion events.

---

## Multiple Output Devices

Support additional hardware such as:

- Smart lighting
- RGB LEDs
- Fans
- Haptic devices
- Fog machines

---

## Hardware Independence

The AI should remain independent of hardware.

It produces context.

Hardware modules decide how to react.

---

## Platform Expansion

Future versions may support:

- HDMI capture
- Console gaming
- Movies
- Streaming platforms
- Virtual reality

These are future opportunities and should not influence the implementation of Phase 1.

---

# Summary

SceneSense has one primary objective:

> **Understand the scene and enhance the experience.**

Every engineering decision should support this objective.

When priorities conflict, choose the solution that improves scene understanding, maintains a modular architecture, and keeps the user experience simple.