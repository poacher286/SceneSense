# ADR-0005: Event-Driven Architecture

> **Status:** Accepted  
> **Date:** 2026-08-02  
> **Decision Makers:** SceneSense Project  
> **Module:** Architecture Decision Records (ADR)

---

# Table of Contents

1. Status
2. Context
3. Problem Statement
4. Decision
5. Why Event-Driven Architecture
6. Alternatives Considered
7. Event Flow
8. Event Types
9. Trade-offs
10. Consequences
11. Future Evolution
12. Summary

---

# Status

**Accepted**

SceneSense will use an **event-driven architecture** as the primary communication mechanism between software modules.

Modules will communicate by **publishing and subscribing to events** rather than calling each other directly.

---

# Context

SceneSense consists of multiple independent components:

- Screen Capture
- AI Engine
- Scene Stabilizer
- Decision Engine
- Scent Mapper
- Device Controller
- ESP32 Communication
- Logging
- Diagnostics

Each component operates independently and at different execution speeds.

A tightly coupled architecture would make future expansion difficult.

---

# Problem Statement

If modules directly invoke one another, the application becomes:

- Difficult to extend
- Difficult to test
- Difficult to replace
- Difficult to debug

Example:

```text
Capture

↓

AI.detect()

↓

Decision.make()

↓

Device.send()

↓

Logger.write()
```

Every module depends on the previous one.

Adding new functionality requires modifying existing code.

This violates the project's modular design principle.

---

# Decision

Modules communicate exclusively through events.

Instead of direct function calls:

```text
Capture

↓

FrameCaptured Event

↓

AI Engine

↓

SceneDetected Event

↓

Decision Engine

↓

ScentTrigger Event

↓

Device Controller
```

Each module reacts only to events that it understands.

---

# Why Event-Driven?

An event-driven architecture provides:

- Loose coupling
- Clear module boundaries
- Easier testing
- Better scalability
- Improved extensibility
- Simpler debugging
- Future plugin support

Modules become independent producers and consumers of information.

---

# Event Bus

The Event Bus acts as the central communication hub.

Responsibilities include:

- Publishing events
- Delivering events
- Managing subscribers
- Preserving event order
- Logging event activity

It contains no business logic.

---

# Event Flow

Complete runtime flow:

```text
Screen Capture

↓

FrameCaptured

↓

AI Engine

↓

SceneDetected

↓

Scene Stabilizer

↓

StableSceneDetected

↓

Decision Engine

↓

ScentTriggerRequested

↓

Device Controller

↓

CommandSent

↓

ESP32

↓

ScentActivated
```

Each event represents a meaningful state change.

---

# Example Event

```python
@dataclass(frozen=True)
class SceneDetected:
    timestamp: float
    scene: str
    confidence: float
```

Events should be:

- Immutable
- Lightweight
- Serializable where practical

---

# Event Categories

## Capture Events

Examples:

- FrameCaptured
- CaptureStarted
- CaptureStopped
- CaptureError

---

## AI Events

Examples:

- SceneDetected
- ConfidenceUpdated
- AIModelLoaded
- AIError

---

## Stabilization Events

Examples:

- StableSceneDetected
- SceneChanged
- SceneRejected

---

## Decision Events

Examples:

- ScentSelected
- ScentTriggerRequested
- CooldownStarted
- CooldownExpired

---

## Device Events

Examples:

- DeviceConnected
- DeviceDisconnected
- CommandSent
- CommandAcknowledged
- DeviceError

---

## System Events

Examples:

- ApplicationStarted
- ConfigurationLoaded
- ShutdownRequested
- FatalError

---

# Threading Model

Different modules execute independently.

Example:

```text
Capture Thread

↓

AI Thread

↓

Decision Thread

↓

Serial Thread

↓

Logging Thread
```

Events are passed safely between threads using thread-safe queues.

---

# Why Not Direct Calls?

Example:

```python
capture.detect_scene()

decision.make()

device.send()
```

Problems:

- Tight coupling
- Harder testing
- Difficult dependency management
- Circular references
- Limited scalability

Decision:

Rejected.

---

# Why Not Global State?

Example:

```python
current_scene = "forest"
```

Problems:

- Race conditions
- Hidden dependencies
- Difficult debugging
- Thread-safety concerns

Decision:

Rejected.

---

# Why Not Polling?

Polling architecture:

```text
Capture

↓

Decision asks AI

↓

AI asks Capture

↓

Device asks Decision
```

Problems:

- Wasted CPU cycles
- Increased latency
- Complex synchronization
- Poor scalability

Decision:

Rejected.

---

# Benefits

## Loose Coupling

Modules know only about events.

They do not know which module produced the event.

---

## Extensibility

New functionality can subscribe to existing events without modifying current modules.

Example:

Future analytics module:

```text
SceneDetected

↓

Analytics Module
```

No changes to the AI engine are required.

---

## Testability

Modules can be tested independently.

Example:

Publish:

```text
SceneDetected
```

Verify:

```text
ScentTriggerRequested
```

No screen capture or hardware is required.

---

## Fault Isolation

If one subscriber fails, the event bus can continue delivering events to others.

This improves resilience.

---

## Observability

Every event can be logged.

Example:

```text
09:14:10 FrameCaptured

09:14:10 SceneDetected

09:14:10 StableSceneDetected

09:14:11 ScentTriggered
```

This greatly simplifies debugging.

---

# Event Ordering

Events should preserve logical ordering.

Example:

Correct:

```text
FrameCaptured

↓

SceneDetected

↓

StableSceneDetected

↓

ScentTriggered
```

Incorrect:

```text
ScentTriggered

↓

SceneDetected
```

The event bus is responsible for maintaining consistent ordering where required.

---

# Performance

Events should be:

- Small
- Immutable
- Fast to create
- Fast to dispatch

Avoid placing full image buffers inside events.

Instead:

```text
Frame ID

Timestamp

Scene

Confidence
```

Large binary data should remain within processing modules.

---

# Error Handling

Failures generate events rather than terminating the application.

Example:

```text
DeviceError

↓

Logger

↓

Notification

↓

Recovery Logic
```

This keeps error handling modular.

---

# Trade-offs

## Advantages

- Loose coupling
- Modular architecture
- Easier testing
- Better scalability
- Cleaner dependency graph
- Improved debugging
- Plugin-friendly

---

## Disadvantages

- Slightly more infrastructure
- Harder to trace event chains without logging
- Potential event storms if not managed carefully
- Requires thoughtful event naming and versioning

These costs are outweighed by the architectural benefits.

---

# Consequences

The project structure reflects the event-driven approach.

```text
Capture

↓

Events

↓

AI

↓

Events

↓

Decision

↓

Events

↓

Device
```

Each module owns its internal logic while communicating through well-defined event contracts.

---

# Future Evolution

The event-driven design naturally supports future capabilities such as:

- Plugin system
- Live diagnostics
- Multiple diffusers
- Companion mobile app
- HDMI capture devices
- Cloud synchronization (optional)
- Metrics collection
- User automation rules

Most additions can subscribe to existing events without altering core modules.

---

# Non-Goals

The event bus is **not** intended to be:

- A message broker
- A distributed queue
- A persistent event store
- A network protocol

Its purpose is in-process communication within the SceneSense application.

---

# Related ADRs

- ADR-0001 — Project Principles
- ADR-0002 — Python-Only Implementation
- ADR-0003 — Semantic Scene Recognition
- ADR-0004 — Local Processing

---

# Summary

SceneSense adopts an event-driven architecture to keep modules independent, testable, and extensible.

```text
Screen Capture

↓

FrameCaptured

↓

AI Engine

↓

SceneDetected

↓

Scene Stabilizer

↓

StableSceneDetected

↓

Decision Engine

↓

ScentTriggerRequested

↓

Device Controller

↓

ESP32
```

By exchanging immutable events instead of direct method calls, the system remains loosely coupled and easier to evolve. New features can be added by subscribing to existing events rather than modifying core components, enabling the architecture to scale from a simple desktop prototype to a broader ecosystem supporting new hardware, platforms, and plugins.

---

# Appendix A – Core Event Types

| Event | Producer | Consumer |
|--------|----------|----------|
| FrameCaptured | Screen Capture | AI Engine |
| SceneDetected | AI Engine | Scene Stabilizer |
| StableSceneDetected | Scene Stabilizer | Decision Engine |
| ScentTriggerRequested | Decision Engine | Device Controller |
| CommandSent | Device Controller | Logger, Diagnostics |
| CommandAcknowledged | ESP32 | Device Controller |
| DeviceError | Device Controller | Recovery, Logger |
| ApplicationStarted | Bootstrap | Logger, Diagnostics |

---

# Appendix B – Event Lifecycle

```text
+----------------------+
|  Screen Capture      |
+----------+-----------+
           |
           | FrameCaptured
           v
+----------------------+
|     AI Engine        |
+----------+-----------+
           |
           | SceneDetected
           v
+----------------------+
| Scene Stabilizer     |
+----------+-----------+
           |
           | StableSceneDetected
           v
+----------------------+
|  Decision Engine     |
+----------+-----------+
           |
           | ScentTriggerRequested
           v
+----------------------+
| Device Controller    |
+----------+-----------+
           |
           | CommandSent
           v
+----------------------+
|       ESP32          |
+----------+-----------+
           |
           | CommandAcknowledged
           v
+----------------------+
| Logging / Metrics    |
+----------------------+
```

This event lifecycle illustrates how information flows through SceneSense without creating direct dependencies between modules, ensuring that each subsystem remains focused on a single responsibility while contributing to the overall real-time scent experience.