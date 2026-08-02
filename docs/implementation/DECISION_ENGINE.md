# SceneSense Decision Engine

> **Version:** 1.0  
> **Status:** Phase 1 Design  
> **Module:** `decision`

---

# Table of Contents

1. Purpose
2. Design Goals
3. Responsibilities
4. High-Level Architecture
5. Decision Pipeline
6. Rule Engine
7. Scene Transition Detection
8. Cooldown Management
9. Scent Mapping
10. Event Generation
11. State Management
12. Configuration
13. Error Handling
14. Performance
15. Testing
16. Future Improvements

---

# Purpose

The Decision Engine is the **brain** of SceneSense.

It transforms stable AI scene predictions into meaningful actions while preventing unnecessary or repetitive scent activations.

The AI Engine answers:

> **"What environment is currently visible?"**

The Decision Engine answers:

> **"Should anything happen?"**

Without this layer, every AI prediction could trigger a scent, creating an unpleasant and chaotic user experience.

---

# Design Goals

The Decision Engine should be:

- Deterministic
- Predictable
- Rule-based
- Easily configurable
- Independent of hardware
- Independent of AI implementation

---

# Responsibilities

The Decision Engine is responsible for:

- Detecting scene transitions
- Applying business rules
- Managing scent cooldowns
- Converting scenes into scent requests
- Publishing events

The Decision Engine is **not** responsible for:

- AI inference
- Screen capture
- Serial communication
- Activating hardware

---

# High-Level Architecture

```text
StableSceneDetectedEvent
            │
            ▼
   Rule Evaluation
            │
            ▼
 Duplicate Detection
            │
            ▼
 Cooldown Check
            │
            ▼
  Scene → Scent Mapping
            │
            ▼
 Generate Scent Event
            │
            ▼
        Event Bus
```

---

# Decision Pipeline

Every stable scene passes through the same sequence.

```text
Stable Scene

↓

Validate Scene

↓

Check Transition

↓

Apply Rules

↓

Check Cooldown

↓

Resolve Scent

↓

Publish Event
```

If any step fails, processing stops.

---

# Input

The Decision Engine subscribes to:

```python
StableSceneDetectedEvent(
    scene="Forest",
    confidence=0.94
)
```

Only stabilized scenes enter the engine.

---

# Output

The Decision Engine publishes:

```python
SceneChangedEvent
```

and

```python
ScentRequestedEvent
```

The Device Controller listens for `ScentRequestedEvent`.

---

# Rule Engine

The Decision Engine evaluates a sequence of rules.

```text
Rule 1

↓

Rule 2

↓

Rule 3

↓

Generate Event
```

Each rule is isolated and independently testable.

---

# Rule 1 – Scene Validation

Ensure the scene exists.

Example:

```text
Forest
```

↓

Valid

Example:

```text
AlienPlanet
```

↓

Unknown

↓

Ignore

---

# Rule 2 – Duplicate Detection

Repeated scenes should not generate duplicate events.

Example:

```text
Forest

↓

Forest
```

Result:

```
Ignore
```

---

# Rule 3 – Transition Detection

A new scene triggers evaluation.

Example:

```text
Forest

↓

Ocean
```

Result:

```
Continue
```

---

# Rule 4 – Cooldown

Repeated activations within a cooldown period are ignored.

Example:

```
Forest

↓

Pine

↓

5 Seconds

↓

Forest
```

↓

Ignore

---

# Rule 5 – Mapping

Convert the semantic scene into a scent.

Example:

```
Forest

↓

Pine
```

---

# Rule Flow

```text
Stable Scene

↓

Known?

↓

Changed?

↓

Cooldown Finished?

↓

Mapped?

↓

Publish
```

---

# Scene Transition Detection

The engine stores the last accepted scene.

Example:

```
Previous

Forest

Current

Forest
```

↓

Ignore

Example:

```
Previous

Forest

Current

Ocean
```

↓

Publish

---

# State Management

The engine maintains lightweight runtime state.

```text
Current Scene

Previous Scene

Last Scent

Cooldown Timers
```

This state is held in memory.

---

# Cooldown Management

Cooldown prevents repeated scent releases.

Example configuration:

```yaml
decision:

  cooldown_seconds: 15
```

Per-scent cooldown is recommended.

Example:

```
Forest

↓

Pine

↓

15 Seconds
```

↓

Eligible Again

---

# Scent Mapping

The engine delegates mapping to the Scent Mapper.

Example:

| Scene | Scent |
|--------|-------|
| Forest | Pine |
| Rain | Petrichor |
| Ocean | Sea Breeze |
| Snow | Cold Mint |
| Fire | Smoke |

Mappings are configuration-driven.

---

# Event Generation

Example:

```python
SceneChangedEvent(
    previous_scene="Forest",
    current_scene="Ocean"
)
```

```python
ScentRequestedEvent(
    scent="SeaBreeze",
    intensity=0.40,
    duration=2.5
)
```

The engine never communicates directly with hardware.

---

# Sequence Diagram

```text
StableSceneDetectedEvent

↓

Decision Engine

↓

Evaluate Rules

↓

Generate Scent Request

↓

Event Bus

↓

Device Controller
```

---

# Configuration

Example:

```yaml
decision:

  cooldown_seconds: 15

  ignore_duplicates: true

  default_duration: 2.5

  default_intensity: 0.40
```

Business logic should be configurable whenever practical.

---

# Logging

Useful log entries include:

```
Scene Accepted

Scene Ignored

Cooldown Active

Unknown Scene

Scent Requested

Rule Failed
```

Logging should explain *why* an event was or was not generated.

---

# Error Handling

Possible failures:

- Missing scent mapping
- Invalid configuration
- Unknown scene
- Rule evaluation exception

Recovery strategy:

```text
Log

↓

Ignore Event

↓

Continue
```

No recoverable error should stop the pipeline.

---

# Performance

The Decision Engine performs simple comparisons and rule evaluations.

Expected complexity:

```
O(1)
```

Processing time should remain well below 1 ms for Phase 1.

---

# Testing

## Unit Tests

- Duplicate detection
- Cooldown logic
- Transition detection
- Scene validation
- Mapping resolution

---

## Integration Tests

- Stabilizer → Decision
- Decision → Event Bus
- Decision → Device Controller

---

## Manual Tests

Verify:

- Forest → Forest → No scent
- Forest → Ocean → Sea Breeze
- Ocean → Ocean → No duplicate
- Unknown scene → Ignored
- Cooldown active → Ignored

---

# Metrics

Expose runtime metrics:

| Metric | Description |
|---------|-------------|
| Current Scene | Latest accepted scene |
| Previous Scene | Last stable scene |
| Events Published | Total scent requests |
| Events Ignored | Duplicate/cooldown count |
| Unknown Scenes | Invalid scene count |
| Average Decision Time | Processing latency |

These metrics aid debugging and optimization.

---

# Future Improvements

## Rule Engine DSL

Future rules could be declared using configuration.

Example:

```yaml
rules:

  - if:
      scene: Forest

    then:
      scent: Pine
```

---

## Layered Scenes

Support combinations.

Example:

```
Forest

+

Rain
```

↓

```
Wet Pine
```

---

## Temporary Events

Future event types:

- Explosion
- Gunfire
- Campfire
- Lava
- Vehicle
- Magic

These events may trigger short-lived scents without changing the primary environment.

---

## Adaptive Intensity

Increase or reduce scent intensity based on:

- Confidence
- Duration in scene
- User preferences

---

## User Profiles

Different users may customize mappings.

Example:

```
Forest

↓

Cedar
```

instead of

```
Forest

↓

Pine
```

---

## AI Feedback Loop

Future versions could learn user preferences.

Example:

```
User frequently skips Smoke

↓

Reduce Smoke intensity
```

---

# Design Principles

The Decision Engine should:

- Be deterministic
- Remain independent of hardware
- Operate only on domain objects
- Avoid AI-specific logic
- Publish events instead of invoking devices directly

Business rules should be centralized here rather than scattered across modules.

---

# Example End-to-End Flow

```text
Stable Scene

Forest

↓

Decision Engine

↓

Scene Changed

↓

Cooldown Passed

↓

Map → Pine

↓

Create ScentRequestedEvent

↓

Event Bus

↓

Device Controller

↓

ESP32

↓

Diffuse Pine
```

---

# Summary

The Decision Engine is the intelligence layer of SceneSense.

It transforms semantic understanding into deliberate actions while ensuring that scent activations remain meaningful, timely, and non-intrusive.

```text
Stable Scene

↓

Evaluate

↓

Decide

↓

Publish

↓

Immerse
```

By centralizing all business rules in a single module, SceneSense achieves a clean separation between perception and action. This makes the system easier to test, easier to extend, and resilient as new scene types, devices, and immersive outputs are introduced in future phases.