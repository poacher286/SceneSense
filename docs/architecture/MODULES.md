# SceneSense Modules

> **Version:** 1.0  
> **Status:** Active  
> **Audience:** Developers

---

# Table of Contents

1. Purpose
2. Module Philosophy
3. High-Level Architecture
4. Module Overview
5. Capture Module
6. AI Module
7. Stabilizer Module
8. Decision Module
9. Event Module
10. Device Module
11. Configuration Module
12. UI Module
13. Common Module
14. Core Module
15. Module Dependencies
16. Design Rules

---

# Purpose

This document describes every software module in SceneSense, its responsibilities, boundaries, dependencies, and interactions.

Every module should satisfy three rules:

- Have a single responsibility
- Be independently testable
- Be replaceable without affecting the rest of the application

---

# Module Philosophy

SceneSense is intentionally divided into small modules.

Instead of one large application:

```
Application

↓

Everything
```

we build:

```
Capture

↓

AI

↓

Stabilizer

↓

Decision

↓

Events

↓

Device
```

Each layer solves one problem.

---

# High-Level Architecture

```
                      +------------------+
                      |   Configuration  |
                      +--------+---------+
                               |
                               ▼

+------------+     +------------------+     +----------------+
| Screen     | --> | AI Recognition   | --> | Stabilizer     |
| Capture    |     +------------------+     +----------------+
+------------+                                 |
                                               ▼
                                        +---------------+
                                        | Decision      |
                                        +-------+-------+
                                                |
                                                ▼
                                          +-----------+
                                          | Event Bus |
                                          +----+------+
                                               |
                   +---------------------------+----------------------+
                   |                                                  |
                   ▼                                                  ▼
            +--------------+                                  +---------------+
            | Device       |                                  | UI            |
            | Controller   |                                  | Dashboard     |
            +--------------+                                  +---------------+
```

---

# Module Overview

| Module | Responsibility |
|----------|----------------|
| Capture | Acquire screen frames |
| AI | Recognize scenes |
| Stabilizer | Remove noisy predictions |
| Decision | Determine scene transitions |
| Events | Communication between modules |
| Device | Communicate with ESP32 |
| Config | Load application settings |
| UI | Dashboard |
| Common | Shared utilities |
| Core | Application lifecycle |

---

# Capture Module

## Purpose

Acquire frames from the active game window.

---

## Responsibilities

- Capture screen
- Capture active window
- Resize frames
- Convert image format
- Publish FrameCaptured events

---

## Does NOT

- Run AI
- Save screenshots
- Trigger scents
- Communicate with hardware

---

## Input

None

---

## Output

```
FrameCapturedEvent

{
    image,
    timestamp
}
```

---

## Suggested Files

```
capture/

screen_capture.py

window_manager.py

frame_provider.py
```

---

# AI Module

## Purpose

Understand the current scene.

---

## Responsibilities

- Load AI model
- Run inference
- Return confidence
- Publish SceneDetected events

---

## Input

```
FrameCapturedEvent
```

---

## Output

```
SceneDetectedEvent

{
    scene,
    confidence
}
```

---

## Does NOT

- Trigger scents
- Decide transitions
- Talk to hardware

---

## Suggested Files

```
ai/

model_loader.py

scene_classifier.py

labels.py
```

---

# Stabilizer Module

## Purpose

Reduce prediction noise.

---

## Example

Raw predictions

```
Forest

Trees

Forest

Forest

Grass

Forest
```

Stable output

```
Forest
```

---

## Responsibilities

- Sliding window
- Majority vote
- Confidence smoothing
- Publish StableSceneDetected

---

## Input

```
SceneDetected
```

---

## Output

```
StableSceneDetected
```

---

## Suggested Files

```
stabilizer/

scene_stabilizer.py

prediction_buffer.py
```

---

# Decision Module

## Purpose

Determine whether something meaningful happened.

---

Example

```
Forest

↓

Rain
```

Generate

```
SceneChanged
```

Example

```
Forest

↓

Forest
```

Ignore

---

## Responsibilities

- Transition detection
- Cooldowns
- Rule evaluation
- Event generation

---

## Input

```
StableSceneDetected
```

---

## Output

```
SceneChanged

ScentRequested
```

---

## Suggested Files

```
decision/

decision_engine.py

cooldown_manager.py

scent_mapper.py

rules.py
```

---

# Event Module

## Purpose

Provide communication between modules.

---

Instead of

```
AI

↓

Device
```

Use

```
AI

↓

Event Bus

↓

Subscribers
```

---

## Responsibilities

- Publish events
- Subscribe listeners
- Remove dependencies
- Event routing

---

## Events

```
FrameCaptured

SceneDetected

StableSceneDetected

SceneChanged

ScentRequested

CommandSent

DeviceConnected

DeviceDisconnected
```

---

## Suggested Files

```
events/

event_bus.py

event_types.py

subscriber.py

publisher.py
```

---

# Device Module

## Purpose

Communicate with physical hardware.

---

Responsibilities

- Serial communication
- Connection handling
- Retry
- Protocol encoding

---

Input

```
ScentRequested
```

---

Output

```
Serial Command
```

---

Example

```
SPRAY:PINE
```

---

Suggested Files

```
device/

serial_controller.py

protocol.py

device_manager.py
```

---

# Configuration Module

## Purpose

Load application configuration.

---

Responsibilities

- Read YAML
- Read JSON
- Environment variables
- Validation

---

Configuration Example

```yaml
capture:
  fps: 5

ai:
  model: clip

decision:
  cooldown: 10

device:
  port: auto
```

---

Suggested Files

```
config/

settings.py

config_loader.py

validator.py
```

---

# UI Module

## Purpose

Display application state.

---

Dashboard displays

- Current scene
- Confidence
- FPS
- Device
- Current scent
- Logs

---

The UI should never:

- perform AI
- trigger devices
- modify predictions

---

Suggested Files

```
ui/

dashboard.py

widgets.py

theme.py
```

---

# Common Module

## Purpose

Shared utilities.

---

Contains

- Logger
- Constants
- Helpers
- Exceptions
- Utilities

---

Suggested Files

```
common/

logger.py

constants.py

helpers.py

exceptions.py
```

---

# Core Module

## Purpose

Application startup and lifecycle.

---

Responsibilities

- Dependency injection
- Startup
- Shutdown
- Module registration
- Event registration

---

Suggested Files

```
core/

application.py

lifecycle.py

bootstrap.py
```

---

# Module Dependencies

```
Core

│

├──────────────┐
│              │
▼              ▼

Config      Event Bus

                ▲

                │

Capture → AI → Stabilizer → Decision

                │

                ▼

          Device Controller

                │

                ▼

              ESP32
```

Rules

- Capture knows nothing about AI.
- AI knows nothing about hardware.
- Hardware knows nothing about AI.
- Communication happens only through events.

---

# Design Rules

Every new module must follow these principles.

## Single Responsibility

One module.

One job.

---

## Loose Coupling

Modules communicate through events.

Never import another module just to call a method.

---

## High Cohesion

Related logic stays together.

Example:

All serial code belongs in the Device module.

---

## Replaceability

The following should be replaceable without affecting the rest of the system:

- AI model
- Screen capture backend
- Hardware controller
- UI framework

---

## Testability

Each module should be testable in isolation.

Examples:

- Mock FrameCaptured events.
- Mock SceneDetected events.
- Mock Serial responses.

No module should require the entire application to be running.

---

# Module Interaction Example

```
Game

↓

Capture Module

↓

FrameCapturedEvent

↓

AI Module

↓

SceneDetectedEvent

↓

Stabilizer Module

↓

StableSceneDetectedEvent

↓

Decision Module

↓

ScentRequestedEvent

↓

Device Module

↓

ESP32

↓

Diffuser
```

---

# Summary

The modular architecture of SceneSense ensures that each subsystem has a clearly defined responsibility and communicates through events rather than direct dependencies.

This approach provides:

- Better maintainability
- Easier testing
- Improved scalability
- Simpler debugging
- Hardware independence
- AI model flexibility

As SceneSense grows beyond scent generation into a broader immersion platform, this modular design will allow new capabilities to be added with minimal impact on existing components.