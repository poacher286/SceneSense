# SceneSense Roadmap

> **Version:** 1.0  
> **Status:** Living Document  
> **Last Updated:** August 2026

---

# Table of Contents

1. Purpose
2. Guiding Principles
3. Development Phases
4. Phase 1 - Proof of Concept
5. Phase 2 - Intelligence
6. Phase 3 - Productization
7. Phase 4 - Platform
8. Future Vision
9. Release Strategy
10. Success Criteria

---

# Purpose

This roadmap defines the planned evolution of SceneSense.

The roadmap serves two purposes:

- Define the direction of the project.
- Prevent feature creep by clearly separating current work from future ambitions.

Only the current phase should influence implementation decisions.

---

# Guiding Principles

Every milestone should satisfy one or more of the following goals.

- Improve scene understanding
- Improve immersion
- Improve reliability
- Improve performance
- Improve extensibility
- Keep the architecture modular

The roadmap is intentionally incremental.

A working prototype is more valuable than a large collection of unfinished features.

---

# Development Phases

```
Phase 1

Proof of Concept

↓

Phase 2

Intelligence

↓

Phase 3

Product

↓

Phase 4

Platform

↓

Future

Immersion Ecosystem
```

---

# Phase 1 — Proof of Concept

## Objective

Validate the core concept.

Can SceneSense understand what is happening on the screen and trigger the correct scent?

Nothing else matters until this question is answered.

---

## Deliverables

### Screen Capture

- Capture active game window
- Capture desktop
- Configurable FPS
- Process frames in memory only

---

### AI

- Semantic scene recognition
- Local inference
- Five initial environments

Initial environments:

- Forest
- Rain
- Ocean
- Snow
- Fire

---

### Scene Stabilization

Prevent unstable AI predictions.

Examples:

```
Forest

Forest

Trees

Forest

↓

Forest
```

---

### Decision Engine

Detect meaningful scene transitions.

Avoid duplicate scent activation.

Support cooldown timers.

---

### Device Communication

USB Serial communication.

Support one prototype device.

---

### Desktop Dashboard

Display:

- Current scene
- Confidence
- FPS
- Device status
- Current scent
- Logs

---

## Success Criteria

The MVP is successful when the following demo works.

```
Launch SceneSense

↓

Start a game

↓

Enter forest

↓

Pine scent activates

↓

Walk into rain

↓

Petrichor activates

↓

Remain in rain

↓

No duplicate activation
```

---

# Phase 2 — Intelligence

## Objective

Improve AI understanding.

Instead of recognizing only environments, SceneSense begins understanding events.

---

## New Features

### Additional Environments

- Desert
- Beach
- Cave
- Mountain
- City
- Village
- Space
- Indoor

---

### Weather

Detect:

- Rain
- Snow
- Fog
- Storm
- Sunny

---

### Lighting

Recognize:

- Morning
- Day
- Sunset
- Night

---

### Event Detection

Examples:

- Fire
- Explosion
- Campfire
- Vehicle
- Smoke
- Magic
- Lava
- Boss Fight

Events become temporary scent triggers.

---

### Better AI

Evaluate models including:

- CLIP
- SigLIP
- Florence-2
- Qwen2.5-VL

---

## Performance Goals

- Lower latency
- Better confidence
- Fewer false positives
- Improved scene stability

---

# Phase 3 — Productization

## Objective

Transform the prototype into a usable desktop application.

---

## Features

### Configuration

- Scene mappings
- Scent mappings
- Cooldowns
- Profiles

---

### Device Manager

Support multiple devices.

Display:

- Connection status
- Firmware version
- Diagnostics

---

### Dashboard

Modern UI.

Statistics.

Logs.

Device controls.

---

### Profiles

Examples:

- RPG
- FPS
- Racing
- Horror

Users can customize scent behavior.

---

### Updates

Automatic firmware updates.

Application updates.

Configuration backup.

---

# Phase 4 — Platform

## Objective

Build a complete immersion platform.

The AI becomes independent of any specific hardware.

---

## Event System

Instead of directly triggering scents:

```
Forest

↓

Scene Event

↓

Subscribers
```

Subscribers:

- Diffuser
- LEDs
- Fan
- Haptic device

---

## Plugin System

Allow third-party extensions.

Example:

```
SceneSense

↓

Plugin

↓

Custom Device
```

---

## SDK

Developers can emit SceneSense events directly.

Example:

```cpp
SceneSense.EmitScene("Forest");
SceneSense.EmitWeather("Rain");
SceneSense.EmitEvent("Explosion");
```

---

## Profiles

Community-created profiles.

Downloadable mappings.

Custom rules.

---

# Future Vision

The following ideas are intentionally outside the current implementation.

These should not influence Phase 1 decisions.

---

## Console Support

Possible future support for:

- PlayStation
- Xbox
- Nintendo Switch

Likely through HDMI capture.

---

## Standalone Hardware

Dedicated SceneSense appliance.

```
HDMI IN

↓

SceneSense Hardware

↓

HDMI OUT

↓

TV
```

---

## Smart Home

Integration with:

- Smart lights
- RGB strips
- Fans
- Temperature
- Fog machines

---

## VR

Support immersive VR environments.

---

## Movies

Support films and streaming content.

---

## Accessibility

Provide environmental awareness.

Examples:

- Fire detected
- Heavy rain
- Indoor vs outdoor

---

# Release Strategy

## v0.1

Repository

Documentation

Architecture

---

## v0.2

Screen capture

Dashboard

Logging

---

## v0.3

AI integration

Scene recognition

---

## v0.4

Decision engine

Scene stabilization

---

## v0.5

ESP32 communication

LED prototype

---

## v0.6

First scent activation

---

## v0.7

Performance improvements

Testing

---

## v1.0

Proof of Concept Complete

---

# Success Criteria

## Technical

- Stable screen capture
- Local AI inference
- End-to-end latency under one second
- Stable scene detection
- Reliable USB communication

---

## Product

A user can:

1. Launch SceneSense.
2. Start a supported PC game.
3. Walk into a forest.
4. Receive the correct scent.
5. Move into another environment.
6. Observe the scent transition.

Without any manual interaction.

---

## Long-Term Goal

SceneSense should evolve from a scent controller into a general-purpose perception engine capable of understanding digital environments and enabling immersive physical experiences through interchangeable hardware.

---

# Out of Scope

The following are intentionally excluded from the current roadmap phase.

- Cloud AI
- Online accounts
- Multiplayer synchronization
- Game-specific integrations
- Console support
- HDMI capture
- Mobile applications
- Subscription services
- Analytics
- Telemetry

These may be revisited in future roadmap revisions but should not delay the successful completion of Phase 1.