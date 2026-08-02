# SceneSense Phase 1 Implementation

> **Version:** 1.0  
> **Status:** Planning  
> **Owner:** SceneSense Project  
> **Estimated Duration:** 6–8 Weeks

---

# Table of Contents

1. Overview
2. Objectives
3. Success Criteria
4. Scope
5. User Journey
6. Functional Requirements
7. Non-Functional Requirements
8. System Workflow
9. MVP Architecture
10. Module Breakdown
11. Development Roadmap
12. Milestones
13. Testing Strategy
14. Risks
15. Deliverables
16. Out of Scope
17. Future Phases

---

# Overview

Phase 1 is the **Minimum Viable Product (MVP)** for SceneSense.

The goal is to prove one fundamental concept:

> **Can a computer understand what is displayed on the screen and automatically trigger the correct scent without any game integration?**

If the answer is yes, every future feature becomes significantly easier.

---

# Phase 1 Vision

```
Game

↓

Screen Capture

↓

AI Scene Recognition

↓

Scene Stabilizer

↓

Decision Engine

↓

Scent Mapping

↓

ESP32

↓

Scent Diffuser
```

Everything in Phase 1 revolves around this pipeline.

---

# Objectives

The MVP should achieve the following goals.

## Functional

✓ Capture the screen

✓ Recognize semantic scenes

✓ Stabilize predictions

✓ Detect scene changes

✓ Trigger correct scent

✓ Display current status

---

## Technical

✓ Modular architecture

✓ Event-driven communication

✓ Configurable mappings

✓ Replaceable AI models

✓ Extensible hardware layer

---

# Success Criteria

The MVP is successful if:

- AI correctly recognizes scenes.
- False scent activations are minimal.
- Average latency is under **1 second**.
- System runs continuously without crashing.
- ESP32 receives commands reliably.
- Users perceive scents matching the environment.

---

# Scope

## Included

- Windows/macOS desktop support
- Full-screen capture
- Semantic scene recognition
- Scene stabilization
- Event Bus
- ESP32 communication
- Desktop dashboard
- YAML configuration
- Logging
- Basic error recovery

---

## Excluded

- PS5
- Xbox
- Nintendo Switch
- Smart TVs
- Multiplayer synchronization
- Online services
- Audio analysis
- Cloud AI
- Lighting effects
- Fan control

These are future phases.

---

# User Journey

```
User starts SceneSense

↓

Application launches

↓

ESP32 connects

↓

User starts game

↓

Screen capture begins

↓

AI detects Forest

↓

Scene stabilizer confirms Forest

↓

Decision engine detects new scene

↓

Pine scent triggered

↓

User enters Ocean

↓

Ocean detected

↓

Sea Breeze triggered
```

No user interaction should be required after startup.

---

# Functional Requirements

## Screen Capture

- Capture active screen
- 5 FPS minimum
- Low CPU usage

---

## AI Recognition

Recognize at least:

- Forest
- Rain
- Ocean
- Snow
- Fire

---

## Stabilizer

Prevent rapid switching caused by noisy predictions.

---

## Decision Engine

Trigger scents only when meaningful changes occur.

---

## Device Controller

Communicate with ESP32 using Serial.

---

## Dashboard

Display:

- Current scene
- Confidence
- Device status
- Current scent
- FPS
- Logs

---

# Non-Functional Requirements

## Performance

- Latency < 1 second
- Memory < 500 MB
- Stable CPU usage
- Continuous operation

---

## Reliability

Application should continue despite:

- Lost frames
- AI errors
- USB disconnects
- Unknown scenes

---

## Maintainability

- Modular packages
- Clear interfaces
- Independent testing
- Documentation-first

---

# MVP Architecture

```
                Screen

                  │

                  ▼

          Capture Module

                  │

                  ▼

            AI Pipeline

                  │

                  ▼

       Scene Stabilizer

                  │

                  ▼

        Decision Engine

                  │

                  ▼

           Event Bus

        ┌────────┴────────┐

        ▼                 ▼

   Desktop UI      Device Controller

                           │

                           ▼

                         ESP32

                           │

                           ▼

                      Diffuser
```

---

# Module Breakdown

## Capture

Responsibilities:

- Capture frames
- Publish FrameCaptured events

---

## AI

Responsibilities:

- Semantic scene recognition

---

## Stabilizer

Responsibilities:

- Smooth predictions

---

## Decision Engine

Responsibilities:

- Detect transitions
- Apply cooldowns
- Publish scent requests

---

## Event Bus

Responsibilities:

- Decouple modules
- Deliver events

---

## Device Controller

Responsibilities:

- Convert scent requests to serial commands

---

## UI

Responsibilities:

- Monitor system status

---

# Development Roadmap

## Week 1

Repository setup

Project structure

Configuration

Logging

---

## Week 2

Screen Capture

Window detection

Frame pipeline

---

## Week 3

CLIP integration

Scene labels

Confidence scoring

---

## Week 4

Scene Stabilizer

Decision Engine

Event Bus

---

## Week 5

ESP32 protocol

Serial communication

Dashboard

---

## Week 6

Testing

Bug fixes

Performance optimization

Documentation updates

---

# Milestones

## Milestone 1

Application starts successfully.

---

## Milestone 2

Frames captured continuously.

---

## Milestone 3

AI recognizes environments.

---

## Milestone 4

Stable scene detection works.

---

## Milestone 5

ESP32 receives commands.

---

## Milestone 6

Complete end-to-end demo.

---

# Data Flow

```
Capture

↓

FrameCapturedEvent

↓

AI

↓

SceneDetectedEvent

↓

Stabilizer

↓

StableSceneDetectedEvent

↓

Decision Engine

↓

ScentRequestedEvent

↓

Device Controller

↓

ESP32
```

---

# Configuration Files

```
config/

application.yaml

models.yaml

scents.yaml

logging.yaml
```

All behavior should be configurable without changing code.

---

# Logging

Separate log streams:

```
application.log

ai.log

device.log

events.log
```

Logs aid debugging and performance analysis.

---

# Testing Strategy

## Unit Tests

- Capture
- AI
- Stabilizer
- Decision Engine
- Device

---

## Integration Tests

- AI → Decision
- Decision → Device
- Full pipeline

---

## Manual Tests

- Forest gameplay
- Rain gameplay
- Ocean gameplay
- Device reconnect
- AI restart

---

# Risks

## AI Misclassification

Mitigation:

Scene Stabilizer

---

## Device Disconnect

Mitigation:

Automatic reconnect

---

## High CPU Usage

Mitigation:

5 FPS capture

Frame resizing

---

## Slow AI

Mitigation:

Smaller models

GPU acceleration (future)

---

# Deliverables

At the end of Phase 1, the following should exist:

### Software

- Desktop application
- Modular architecture
- AI pipeline
- Dashboard
- Configuration system
- Logging
- Test suite

---

### Hardware

- ESP32 firmware
- Serial protocol
- Scent diffuser prototype

---

### Documentation

- Vision documents
- Architecture documents
- Implementation documents
- Hardware documentation
- User guide

---

# Out of Scope

The following ideas are intentionally deferred.

## Multi-scent blending

Example:

Forest + Rain

↓

Wet Pine

---

## Temporary events

- Explosion
- Gunfire
- Magic
- Campfire

---

## Weather layers

- Fog
- Wind
- Storm

---

## Console support

- PS5
- Xbox
- Nintendo Switch

---

## TV support

HDMI capture

---

## Smart Home

- Lights
- Fan
- Haptics

---

## Online Features

- Profiles
- Cloud sync
- Analytics

---

# Future Phases

## Phase 2

- More scene categories
- Better AI
- Temporary event detection
- User scent profiles

---

## Phase 3

- HDMI input
- Console support
- Smart TV support
- Lighting integration
- Haptic devices

---

## Phase 4

- AI personalization
- Plugin system
- Marketplace
- Community-created scent packs
- Multi-device orchestration

---

# Phase 1 Exit Checklist

- [ ] Application launches successfully
- [ ] Configuration loads correctly
- [ ] Screen capture operates continuously
- [ ] AI recognizes supported scenes
- [ ] Scene stabilization prevents flickering
- [ ] Decision Engine suppresses duplicates
- [ ] Event Bus delivers events reliably
- [ ] ESP32 receives serial commands
- [ ] Scent diffuser activates correctly
- [ ] Dashboard displays live status
- [ ] Logging captures key events
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Documentation is complete

---

# Success Metrics

| Metric | Target |
|---------|--------|
| Capture Rate | ≥ 5 FPS |
| AI Inference Time | ≤ 100 ms |
| End-to-End Latency | ≤ 1 second |
| Memory Usage | < 500 MB |
| Uptime | > 8 hours continuous |
| Scene Accuracy | > 90% (supported scenes) |
| False Scent Triggers | < 5% |

---

# Summary

Phase 1 establishes the technological foundation for SceneSense.

The objective is not to build the final product—it is to validate the complete perception-to-action pipeline.

```
Screen

↓

Understand

↓

Stabilize

↓

Decide

↓

Trigger

↓

Immerse
```

If Phase 1 succeeds, SceneSense will have a robust, modular platform capable of expanding into richer AI understanding, additional immersive devices, console support, and smart-home integration without requiring a major architectural redesign.