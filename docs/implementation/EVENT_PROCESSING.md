# SceneSense Event Processing

> **Version:** 1.0  
> **Status:** Phase 1 Design  
> **Module:** `events`

---

# Table of Contents

1. Purpose
2. Why Event Processing?
3. Design Goals
4. Architecture
5. Event Lifecycle
6. Event Types
7. Event Bus
8. Publishers
9. Subscribers
10. Event Queue
11. Threading Model
12. Event Ordering
13. Error Handling
14. Performance
15. Configuration
16. Testing
17. Future Improvements

---

# Purpose

The Event Processing subsystem is the communication backbone of SceneSense.

Rather than allowing modules to call each other directly, every module communicates by publishing and subscribing to events.

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
```

This architecture keeps every module independent, testable, and replaceable.

---

# Why Event Processing?

Without an Event Bus:

```
Capture

↓

AI

↓

Decision

↓

Device
```

Every module depends directly on another.

With Event Processing:

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

Each module only understands events.

---

# Design Goals

The Event Processing system should be:

- Lightweight
- Thread-safe
- Asynchronous
- Low latency
- Easy to debug
- Independent of business logic

---

# Responsibilities

The Event subsystem is responsible for:

- Publishing events
- Delivering events
- Managing subscribers
- Preserving event order
- Handling subscriber failures

It is **not** responsible for:

- AI inference
- Business rules
- Device communication
- UI rendering

---

# High-Level Architecture

```text
Publisher

↓

Event Bus

↓

Subscribers
```

Multiple publishers and subscribers can coexist without knowledge of one another.

---

# Event Lifecycle

Every event follows the same lifecycle.

```text
Create Event

↓

Publish

↓

Queue

↓

Dispatch

↓

Subscriber

↓

Complete
```

Events are immutable.

---

# Event Types

Phase 1 uses the following events.

| Event | Published By | Consumed By |
|--------|--------------|-------------|
| FrameCapturedEvent | Capture | AI |
| SceneDetectedEvent | AI | Stabilizer |
| StableSceneDetectedEvent | Stabilizer | Decision Engine |
| SceneChangedEvent | Decision Engine | UI, Logger |
| ScentRequestedEvent | Decision Engine | Device Controller |
| DeviceConnectedEvent | Device | UI |
| DeviceDisconnectedEvent | Device | UI |
| ErrorEvent | Any Module | Logger, UI |

---

# Event Object

Every event shares common metadata.

Example:

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Event:
    timestamp: datetime
```

Specific events inherit or compose this base structure.

---

# Event Bus

The Event Bus manages all event delivery.

Responsibilities:

- Register subscribers
- Publish events
- Dispatch events
- Remove subscribers
- Recover from subscriber failures

Suggested interface:

```python
class EventBus:

    def publish(self, event):
        pass

    def subscribe(self, event_type, handler):
        pass
```

---

# Publishers

Any module may publish events.

Examples:

```
Capture

↓

FrameCapturedEvent
```

```
AI

↓

SceneDetectedEvent
```

```
Decision

↓

ScentRequestedEvent
```

Publishers never know who receives the event.

---

# Subscribers

Modules subscribe only to events they require.

Example:

```
AI

↓

FrameCapturedEvent
```

```
Decision Engine

↓

StableSceneDetectedEvent
```

```
Device Controller

↓

ScentRequestedEvent
```

Subscribers remain loosely coupled.

---

# Event Queue

Events are stored temporarily before processing.

```
Event Queue

↓

Dispatch

↓

Subscriber
```

Recommended queue type:

```
FIFO
```

This preserves ordering.

---

# Queue Size

Recommended default:

```yaml
events:

  queue_size: 100
```

If the queue fills:

- Drop oldest low-priority events
- Preserve high-priority events

Phase 1 keeps a simple bounded FIFO queue.

---

# Threading Model

Each module operates independently.

```text
Capture Thread

↓

Event Queue

↓

AI Thread

↓

Event Queue

↓

Decision Thread

↓

Event Queue

↓

Device Thread
```

This prevents slow modules from blocking the pipeline.

---

# Event Ordering

Events must be processed in publication order.

Example:

```
Frame 1

↓

Frame 2

↓

Frame 3
```

Never:

```
Frame 3

↓

Frame 1
```

Ordering is essential for temporal consistency.

---

# Event Priorities (Future)

Potential priority levels:

| Priority | Example |
|----------|---------|
| High | Device disconnect |
| Medium | Scene transition |
| Low | Debug logging |

Phase 1 processes events in FIFO order only.

---

# Error Handling

Subscriber failures should never interrupt event delivery.

Example:

```
Event

↓

Logger ✔

↓

Dashboard ✔

↓

Device ❌

↓

Continue
```

Each subscriber executes independently.

---

# Event Replay (Future)

Future versions may record events.

```
FrameCapturedEvent

↓

SceneDetectedEvent

↓

StableSceneDetectedEvent

↓

Replay
```

Useful for debugging and regression testing.

---

# Logging

Useful log entries:

```
Subscriber Registered

Event Published

Event Delivered

Subscriber Failed

Queue Overflow
```

Avoid logging every frame in production mode.

---

# Configuration

Example:

```yaml
events:

  queue_size: 100

  asynchronous: true

  log_events: false
```

All settings should be configurable.

---

# Performance

Expected complexity:

Publishing:

```
O(number of subscribers)
```

Dispatch:

```
O(1)
```

The Event Bus should introduce negligible latency.

---

# Testing

## Unit Tests

- Publish
- Subscribe
- Unsubscribe
- Queue ordering
- Subscriber isolation

---

## Integration Tests

- Capture → AI
- AI → Stabilizer
- Stabilizer → Decision
- Decision → Device

---

## Performance Tests

Measure:

- Event throughput
- Queue latency
- Subscriber execution time
- Queue utilization

---

# Metrics

Expose runtime metrics:

| Metric | Description |
|---------|-------------|
| Events Published | Total events |
| Events Delivered | Successful dispatches |
| Active Subscribers | Registered handlers |
| Queue Size | Current queue depth |
| Queue Overflows | Dropped events |
| Average Dispatch Time | Event latency |

These metrics help diagnose bottlenecks.

---

# Future Improvements

## Priority Queue

Support multiple priority levels.

---

## Wildcard Subscribers

Example:

```
*

↓

Receive All Events
```

Useful for diagnostics.

---

## Event Filtering

Allow subscribers to receive only matching events.

Example:

```
StableSceneDetectedEvent

↓

Forest Only
```

---

## Event Persistence

Persist events to disk.

Applications:

- Replay
- Analytics
- Performance tuning

---

## Distributed Event Bus

Future cloud-enabled versions may distribute events across processes or devices.

---

## Remote Monitoring

The Event Bus could stream events to a remote dashboard for development or diagnostics.

---

# Design Principles

The Event Processing subsystem should:

- Use immutable events
- Preserve ordering
- Isolate subscriber failures
- Avoid business logic
- Remain thread-safe
- Minimize latency

It is an infrastructure component, not a decision-making component.

---

# Sequence Diagram

```text
Capture

↓

FrameCapturedEvent

↓

Event Bus

↓

AI

↓

SceneDetectedEvent

↓

Event Bus

↓

Stabilizer

↓

StableSceneDetectedEvent

↓

Event Bus

↓

Decision Engine

↓

ScentRequestedEvent

↓

Event Bus

↓

Device Controller
```

---

# End-to-End Example

```text
Screen

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

Every interaction between modules occurs through events.

---

# Summary

The Event Processing subsystem is the communication foundation of SceneSense.

It enables independent modules to collaborate without direct dependencies, creating a modular, scalable, and maintainable architecture.

```text
Publish

↓

Queue

↓

Dispatch

↓

Process

↓

Continue
```

By adopting an event-driven architecture from the beginning, SceneSense gains flexibility for future expansion, including additional AI models, multiple hardware devices, cloud services, analytics, and plugin systems—all without tightly coupling the application's core components.