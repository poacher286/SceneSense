# Event Bus Architecture

> **Version:** 1.0  
> **Status:** Active  
> **Module:** Core Infrastructure

---

# Table of Contents

1. Introduction
2. Why an Event Bus?
3. Design Goals
4. Architecture
5. Event Lifecycle
6. Event Types
7. Event Structure
8. Publishers
9. Subscribers
10. Event Flow
11. Thread Safety
12. Error Handling
13. Future Expansion

---

# Introduction

The Event Bus is the communication backbone of SceneSense.

Instead of allowing modules to directly call each other, every module communicates by publishing and subscribing to events.

Without an Event Bus:

```
Capture
    │
    ▼
AI
    │
    ▼
Decision
    │
    ▼
Device
```

Every module depends on another module.

As the project grows, this becomes difficult to maintain.

---

With an Event Bus:

```
Capture

↓

Event Bus

↓

AI

↓

Event Bus

↓

Decision

↓

Event Bus

↓

Device
```

Each module only knows about the Event Bus.

---

# Why an Event Bus?

Imagine we later add:

- RGB Lights
- Fan Controller
- Discord Integration
- Logging
- Recording
- Analytics

Without an Event Bus:

```
Decision

├── Device
├── Lights
├── Fan
├── Logger
├── Analytics
└── Recorder
```

Every new module requires modifying existing code.

With an Event Bus:

```
Decision

↓

SceneChanged

↓

Subscribers

├── Device
├── Lights
├── Fan
├── Logger
├── Recorder
└── Analytics
```

No existing code changes.

New modules simply subscribe.

---

# Design Goals

The Event Bus should:

- Decouple modules
- Be lightweight
- Be thread-safe
- Be asynchronous
- Support multiple subscribers
- Never contain business logic

---

# Architecture

```
                 +-----------------------+
                 |      Event Bus        |
                 +----------+------------+
                            |
      +---------------------+----------------------+
      |                     |                      |
      ▼                     ▼                      ▼

Capture Module       Device Module          Dashboard

      ▲                     ▲                      ▲
      |                     |                      |
      +---------------------+----------------------+
                            |
                            ▼
                      Decision Module
```

Every module both publishes and subscribes to events.

---

# Event Lifecycle

```
Frame Captured

↓

Publish

↓

Event Queue

↓

Subscribers

↓

Processing

↓

Publish Next Event
```

The Event Bus never processes the event itself.

It only delivers it.

---

# Event Structure

Every event should share a common structure.

```python
Event
```

```python
{
    "id": "uuid",
    "type": "SceneChanged",
    "timestamp": "...",
    "source": "decision_engine",
    "payload": {}
}
```

---

## Fields

| Field | Description |
|---------|-------------|
| id | Unique identifier |
| type | Event name |
| timestamp | Creation time |
| source | Publisher |
| payload | Event-specific data |

---

# Event Types

## Application Events

```
ApplicationStarted

ApplicationStopped
```

---

## Capture Events

```
FrameCaptured
```

---

## AI Events

```
SceneDetected
```

---

## Stabilizer Events

```
StableSceneDetected
```

---

## Decision Events

```
SceneChanged

ScentRequested
```

---

## Device Events

```
DeviceConnected

DeviceDisconnected

DeviceError

CommandSent
```

---

## UI Events

```
WindowOpened

WindowClosed
```

---

# Publishers

Each module publishes only its own events.

| Module | Publishes |
|---------|-----------|
| Capture | FrameCaptured |
| AI | SceneDetected |
| Stabilizer | StableSceneDetected |
| Decision | SceneChanged, ScentRequested |
| Device | DeviceConnected, DeviceError |
| UI | WindowOpened |

A module should never publish another module's events.

---

# Subscribers

Subscribers react to events.

Example

```
SceneChanged
```

Subscribers

```
Dashboard

↓

Logger

↓

Device Controller
```

Every subscriber is independent.

---

# Event Flow Example

## Step 1

Capture

Publishes

```
FrameCaptured
```

↓

AI receives it

---

## Step 2

AI

Publishes

```
SceneDetected
```

↓

Stabilizer receives it

---

## Step 3

Stabilizer

Publishes

```
StableSceneDetected
```

↓

Decision receives it

---

## Step 4

Decision

Publishes

```
SceneChanged
```

↓

Device Controller

↓

Dashboard

↓

Logger

---

## Step 5

Device Controller

Publishes

```
CommandSent
```

↓

Dashboard

↓

Logger

---

# Complete Flow

```
Capture

↓

FrameCaptured

↓

AI

↓

SceneDetected

↓

Stabilizer

↓

StableSceneDetected

↓

Decision

↓

SceneChanged

↓

ScentRequested

↓

Device

↓

CommandSent
```

---

# Event Queue

Events should not be delivered immediately.

Instead:

```
Publish

↓

Queue

↓

Dispatcher

↓

Subscribers
```

Benefits

- Better performance
- Thread safety
- No recursive calls
- Better debugging

---

# Thread Safety

Each module may run on a different thread.

Example

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

The Event Bus must guarantee safe communication between threads.

Python's `queue.Queue` is sufficient for Phase 1.

Future versions may adopt `asyncio` if asynchronous I/O becomes beneficial.

---

# Event Ordering

Events should be processed in the order they were published.

Example

Correct

```
FrameCaptured

↓

SceneDetected

↓

SceneChanged

↓

ScentRequested
```

Incorrect

```
SceneChanged

↓

FrameCaptured
```

Maintaining order is essential for predictable behavior.

---

# Error Handling

Subscriber failures should never crash the Event Bus.

Example

```
SceneChanged

↓

Dashboard

✔ Success

↓

Logger

✔ Success

↓

Device

❌ Failure
```

Only the Device subscriber fails.

The Dashboard and Logger still receive the event.

Failures should be isolated.

---

# Event Replay (Future)

Future versions may optionally record events.

```
FrameCaptured

↓

SceneDetected

↓

SceneChanged

↓

ScentRequested
```

A recorded event stream allows developers to replay an entire session without running a game.

Benefits

- Debugging
- Performance testing
- Regression testing

This feature is intentionally out of scope for Phase 1.

---

# Future Subscribers

As SceneSense evolves, new modules can subscribe without changing existing code.

Examples

```
SceneChanged

↓

Lighting

↓

Fan

↓

Haptic Vest

↓

Fog Machine

↓

Streaming Overlay

↓

Smart Home
```

The Decision Engine remains unchanged.

---

# Design Rules

Every event must satisfy the following rules.

## Immutable

Events should never be modified after publication.

---

## Serializable

Events should be easy to serialize to JSON.

---

## Timestamped

Every event should include its creation time.

---

## Self-Contained

Subscribers should not require additional context.

Everything needed should exist inside the event payload.

---

## Small

Events should contain metadata.

Avoid sending large images or AI models.

Example

Good

```json
{
  "scene": "Forest"
}
```

Bad

```
Entire Screenshot
```

Large objects should remain in their originating module.

---

# Future Enhancements

Possible improvements include:

- Event priorities
- Event filtering
- Wildcard subscriptions
- Event persistence
- Event replay
- Remote subscribers
- WebSocket broadcasting
- Performance metrics

None of these are required for Phase 1.

---

# Summary

The Event Bus is the central communication mechanism within SceneSense.

It allows independent modules to collaborate without direct dependencies, making the system easier to extend, test, and maintain.

The guiding principle is simple:

```
Modules never talk to each other.

Modules talk to events.
```

This approach keeps the architecture clean today while making it straightforward to add new capabilities—such as lighting, haptics, or smart-home integrations—without redesigning the application's core.