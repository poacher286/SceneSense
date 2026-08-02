# SceneSense Decision Engine

> **Version:** 1.0  
> **Status:** Active  
> **Audience:** Developers

---

# Table of Contents

1. Purpose
2. Why a Decision Engine?
3. Responsibilities
4. High-Level Architecture
5. Decision Pipeline
6. Inputs
7. Outputs
8. Decision Rules
9. Cooldown Management
10. Scent Mapping
11. Rule Evaluation
12. Event Generation
13. Error Handling
14. Future Enhancements
15. Summary

---

# Purpose

The Decision Engine is responsible for transforming **stable AI scene predictions** into meaningful immersion events.

It acts as the brain between perception and hardware.

Without the Decision Engine:

```
AI

↓

Forest

↓

Pine
```

The diffuser would activate continuously.

With the Decision Engine:

```
AI

↓

Stable Forest

↓

Evaluate Rules

↓

Trigger Once

↓

Wait

↓

Trigger Again Only If Needed
```

The Decision Engine ensures that physical actions occur only when they provide value to the user.

---

# Why a Decision Engine?

The AI recognizes **what the user is seeing**.

The hardware performs **physical actions**.

The Decision Engine decides **whether anything should happen**.

It answers questions like:

- Did the environment change?
- Has enough time passed?
- Is this confidence high enough?
- Has this scent already been triggered?
- Should this event be ignored?

---

# Responsibilities

The Decision Engine is responsible for:

- Detecting scene transitions
- Preventing duplicate activations
- Managing cooldowns
- Mapping scenes to scents
- Publishing immersion events
- Supporting future rule-based automation

The Decision Engine is **not** responsible for:

- AI inference
- Screen capture
- Hardware communication
- UI rendering

---

# High-Level Architecture

```
                Stable Scene
                      │
                      ▼
             +------------------+
             | Decision Engine  |
             +--------+---------+
                      │
        +-------------+--------------+
        |                            |
        ▼                            ▼
Cooldown Check              Rule Evaluation
        |                            |
        +-------------+--------------+
                      │
                      ▼
             Scent Mapping
                      │
                      ▼
              Event Generation
                      │
                      ▼
                 Event Bus
```

---

# Decision Pipeline

```
StableSceneDetectedEvent

↓

Compare With Previous Scene

↓

Evaluate Rules

↓

Check Cooldown

↓

Map Scene

↓

Generate Event

↓

Publish Event
```

Every step must succeed before an event is published.

---

# Inputs

The Decision Engine receives events from the Scene Stabilizer.

Example:

```python
StableSceneDetectedEvent(
    scene="Forest",
    confidence=0.95
)
```

It also maintains internal state, including:

- Previous stable scene
- Last triggered scent
- Active cooldown timers

---

# Outputs

If a transition is valid, the Decision Engine publishes:

```python
SceneChangedEvent(
    previous_scene="Ocean",
    current_scene="Forest"
)
```

and

```python
ScentRequestedEvent(
    scent="Pine",
    intensity=0.4,
    duration=2.0
)
```

These events are consumed by the Event Bus.

---

# Decision Rules

Rules determine whether a stable scene should produce an action.

## Rule 1 — Ignore Duplicate Scenes

Example:

```
Forest

↓

Forest
```

Result:

```
No Event
```

---

## Rule 2 — Detect Scene Changes

Example:

```
Forest

↓

Rain
```

Result:

```
SceneChangedEvent
```

---

## Rule 3 — Confidence Threshold

Ignore scenes below the configured confidence.

Example:

```
Forest

Confidence

0.45
```

↓

Ignore

---

## Rule 4 — Cooldown

Prevent repeated activation of the same scent.

Example:

```
Forest

↓

Forest

↓

Forest
```

Only the first transition triggers a scent.

---

# Cooldown Management

The Decision Engine tracks when each scent was last activated.

Example configuration:

```yaml
decision:
  cooldown_seconds: 15
```

Example:

```
Forest

↓

SPRAY:PINE

↓

10 Seconds

↓

Forest
```

↓

Ignored

```
Forest

↓

16 Seconds

↓

Forest
```

↓

Eligible again (if triggered by a new transition)

---

## Cooldown Strategies

Possible strategies include:

- Global cooldown
- Per-scene cooldown
- Per-scent cooldown

Phase 1 uses a simple **per-scent cooldown**.

---

# Scent Mapping

The Decision Engine converts scenes into scent requests.

Example mapping:

| Scene | Scent |
|--------|-------|
| Forest | Pine |
| Rain | Petrichor |
| Ocean | Sea Breeze |
| Snow | Cold Mint |
| Fire | Smoke |

Mappings are loaded from configuration rather than hardcoded.

Example:

```yaml
scents:
  Forest: Pine
  Rain: Petrichor
  Ocean: SeaBreeze
  Snow: ColdMint
  Fire: Smoke
```

---

# Rule Evaluation

Each incoming scene passes through a sequence of rules.

```
Stable Scene

↓

Confidence Check

↓

Duplicate Check

↓

Cooldown Check

↓

Scene Mapping

↓

Generate Event
```

If any rule fails, processing stops.

---

# Event Generation

When all rules pass, the Decision Engine publishes standardized events.

Example:

```python
SceneChangedEvent(
    previous_scene="Forest",
    current_scene="Rain"
)
```

```python
ScentRequestedEvent(
    scent="Petrichor",
    intensity=0.5,
    duration=3.0
)
```

The Decision Engine never communicates directly with the ESP32.

---

# State Management

The Decision Engine maintains a small amount of runtime state.

Example:

```text
Current Scene:
Forest

Previous Scene:
Ocean

Last Trigger:
Pine

Cooldown Expiry:
18:35:12
```

This state is held in memory and resets when the application restarts.

---

# Error Handling

Decision failures should never stop the pipeline.

Examples:

Unknown scene:

```
Volcano

↓

No Mapping

↓

Log Warning

↓

Ignore
```

Invalid configuration:

```
Missing scent mapping

↓

Use default behavior

↓

Continue
```

The application should fail gracefully.

---

# Future Enhancements

Future versions may support more advanced rules.

## Layered Scenes

Example:

```
Forest
+
Rain
+
Night
```

↓

Trigger

```
Wet Pine
```

---

## Temporary Events

Examples:

- Explosion
- Gunfire
- Campfire
- Magic
- Vehicle

These events can produce short-lived scent effects without replacing the primary environment.

---

## Dynamic Intensity

Adjust scent strength using confidence or context.

Example:

```
Light Rain

↓

Intensity 0.2
```

```
Heavy Rain

↓

Intensity 0.8
```

---

## User Profiles

Different users may prefer different scent mappings.

Example:

```yaml
profile:
  forest: Cedar
```

Another user:

```yaml
profile:
  forest: Pine
```

---

## Rule Engine

Eventually, rules may become configurable.

Example:

```yaml
rules:

  - if:
      scene: Forest
      weather: Rain

    then:
      scent: WetPine
```

This would allow advanced customization without changing application code.

---

# Design Principles

The Decision Engine should always be:

- Stateless where possible
- Deterministic
- Easy to test
- Configuration-driven
- Independent of hardware
- Independent of AI implementation

It should operate solely on standardized Scene objects and events.

---

# Testing Scenarios

Recommended unit tests include:

| Scenario | Expected Result |
|----------|-----------------|
| Forest → Forest | No event |
| Forest → Rain | SceneChanged + ScentRequested |
| Confidence below threshold | Ignore |
| Cooldown active | Ignore |
| Unknown scene | Warning, no crash |
| Missing scent mapping | Graceful handling |

These tests validate the engine without requiring AI models or hardware.

---

# Summary

The Decision Engine is the intelligence layer between perception and action.

It transforms stable semantic understanding into meaningful, well-timed immersion events.

```
Stable Scene

↓

Evaluate

↓

Decide

↓

Publish

↓

React
```

By centralizing all decision-making logic, SceneSense remains modular, predictable, and easy to extend. As the platform grows to support richer scenes, multiple devices, and configurable behaviors, the Decision Engine can evolve without affecting the AI pipeline or hardware integrations.