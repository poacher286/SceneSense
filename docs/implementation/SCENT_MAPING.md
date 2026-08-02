# SceneSense Scent Mapping

> **Version:** 1.0  
> **Status:** Phase 1 Design  
> **Module:** `decision / mapping`

---

# Table of Contents

1. Purpose
2. Design Goals
3. Responsibilities
4. Why Scent Mapping?
5. Architecture
6. Mapping Pipeline
7. Mapping Configuration
8. Scent Profiles
9. Intensity
10. Duration
11. Cooldowns
12. Events
13. Configuration
14. Error Handling
15. Testing
16. Future Improvements

---

# Purpose

The Scent Mapping module is responsible for translating semantic scene information into physical scent actions.

The AI Engine understands **what the player is seeing**.

The Scent Mapping module determines **what the player should smell**.

```
Scene

↓

Scent Mapping

↓

Scent Request
```

The module contains **no AI logic** and **no hardware communication**.

---

# Design Goals

The Scent Mapping module should be:

- Configuration-driven
- Easy to customize
- Independent of AI models
- Independent of hardware
- Easy to extend
- Safe to modify without code changes

---

# Responsibilities

The module is responsible for:

- Scene → scent translation
- Default intensity selection
- Default duration selection
- Scent profile loading
- Mapping validation

The module is **not** responsible for:

- AI inference
- Cooldown decisions
- Device communication
- Diffuser control

---

# Why Scent Mapping?

Multiple games can represent the same environment.

Example:

```
Minecraft

↓

Forest

↓

Pine
```

```
Red Dead Redemption

↓

Forest

↓

Pine
```

```
The Witcher

↓

Forest

↓

Pine
```

The mapping depends on the **scene**, not the game.

---

# High-Level Architecture

```text
Stable Scene

↓

Decision Engine

↓

Scent Mapper

↓

Scent Request

↓

Event Bus
```

---

# Mapping Pipeline

```
Scene

↓

Lookup Mapping

↓

Load Defaults

↓

Create Scent Request

↓

Publish Event
```

The mapping process should be deterministic.

---

# Mapping Database

Phase 1 uses a YAML configuration file.

Example:

```yaml
Forest:

  scent: Pine

Rain:

  scent: Petrichor

Ocean:

  scent: SeaBreeze

Snow:

  scent: ColdMint

Fire:

  scent: Smoke
```

No mappings should be hardcoded.

---

# Scent Object

Example:

```python
@dataclass(frozen=True)
class Scent:
    name: str
    intensity: float
    duration: float
```

The Scent object is immutable.

---

# Scent Request

Example:

```python
@dataclass(frozen=True)
class ScentRequest:
    scent: Scent
    timestamp: datetime
```

This request is published to the Event Bus.

---

# Default Mapping

Suggested Phase 1 mappings:

| Scene | Scent |
|--------|-------|
| Forest | Pine |
| Rain | Petrichor |
| Ocean | Sea Breeze |
| Snow | Cold Mint |
| Fire | Smoke |

These scents provide clear environmental associations and are readily available from fragrance suppliers.

---

# Intensity

Each scent has a default intensity.

Range:

```
0.0

↓

1.0
```

Recommended values:

| Scene | Intensity |
|--------|-----------|
| Forest | 0.35 |
| Rain | 0.45 |
| Ocean | 0.30 |
| Snow | 0.25 |
| Fire | 0.50 |

Intensity should remain subtle to avoid overwhelming the user.

---

# Duration

Each scent also specifies a diffusion duration.

Example:

| Scene | Duration |
|--------|----------|
| Forest | 2 s |
| Rain | 3 s |
| Ocean | 2 s |
| Snow | 2 s |
| Fire | 2 s |

Duration should be configurable.

---

# Mapping Configuration

Example:

```yaml
Forest:

  scent: Pine

  intensity: 0.35

  duration: 2

Rain:

  scent: Petrichor

  intensity: 0.45

  duration: 3
```

The configuration loader validates these values during startup.

---

# Scent Profiles

Future versions may support user-selectable scent profiles.

Example:

```
Default Profile

Forest

↓

Pine
```

```
Alternative Profile

Forest

↓

Cedar
```

Profiles allow personalization without changing application logic.

---

# Mapping Resolution

When a stable scene arrives:

```
Forest

↓

Lookup

↓

Pine

↓

Scent Request
```

If no mapping exists:

```
Unknown Scene

↓

Warning

↓

Ignore
```

---

# Event Generation

Example:

```python
ScentRequestedEvent(
    scent="Pine",
    intensity=0.35,
    duration=2.0
)
```

The Device Controller subscribes to this event.

---

# Validation

Configuration validation checks:

- Duplicate scenes
- Missing scents
- Invalid intensity
- Invalid duration

Example:

```yaml
intensity: 1.5
```

↓

Invalid

↓

Configuration Error

---

# Configuration

Example:

```yaml
mapping:

  default_intensity: 0.35

  default_duration: 2.0

  fallback_scent: null
```

Defaults are used when individual mappings omit optional fields.

---

# Logging

Useful log entries:

```
Mapping Loaded

Unknown Scene

Scent Resolved

Invalid Mapping

Configuration Error
```

Logging helps diagnose configuration issues.

---

# Error Handling

Possible failures:

- Missing YAML
- Invalid values
- Duplicate mappings
- Unknown scent

Recovery:

```text
Log

↓

Ignore Mapping

↓

Continue
```

The application should never crash due to a mapping error.

---

# Performance

Mapping lookup should be constant time.

Expected complexity:

```
O(1)
```

A dictionary or hash map provides efficient scene resolution.

---

# Testing

## Unit Tests

- Mapping lookup
- Default values
- Validation
- Scent request creation

---

## Integration Tests

- Decision Engine → Mapping
- Mapping → Event Bus

---

## Manual Tests

Verify:

- Forest → Pine
- Rain → Petrichor
- Unknown scene → Ignored
- Invalid configuration → Warning
- Default values applied correctly

---

# Future Improvements

## Layered Scents

Example:

```
Forest

+

Rain

↓

Wet Pine
```

Generated by combining two scent cartridges.

---

## Temporary Effects

```
Explosion

↓

Gunpowder

↓

2 Seconds

↓

Return to Forest
```

Temporary effects overlay the current environmental scent.

---

## Adaptive Intensity

Adjust intensity using:

- Confidence
- Scene duration
- User preferences
- Diffuser size

---

## Seasonal Variants

```
Forest

+

Winter

↓

Evergreen
```

```
Forest

+

Autumn

↓

Dry Leaves
```

---

## Dynamic Blending

Future hardware may support simultaneous diffusion.

Example:

```
70%

Pine

+

30%

Petrichor
```

Creating a richer and more realistic scent.

---

## Marketplace

Community-created scent packs.

Example:

```
Fantasy Pack

Sci-Fi Pack

Horror Pack

Retro Pack
```

Users could swap profiles without changing code.

---

# Design Principles

The Scent Mapping module should:

- Be deterministic
- Be configuration-driven
- Avoid hardware dependencies
- Produce immutable Scent objects
- Support future customization

Business logic should remain separate from configuration data.

---

# Sequence Diagram

```text
Stable Scene

↓

Lookup Scene

↓

Resolve Mapping

↓

Create Scent

↓

Create ScentRequest

↓

Publish ScentRequestedEvent
```

---

# Metrics

Expose runtime metrics:

| Metric | Description |
|---------|-------------|
| Mappings Loaded | Total valid mappings |
| Mapping Failures | Invalid lookups |
| Unknown Scenes | Unmapped scene count |
| Scent Requests | Total requests generated |
| Average Lookup Time | Mapping latency |

These metrics assist with debugging and future optimization.

---

# Example End-to-End Flow

```text
Stable Scene

Forest

↓

Lookup

↓

Pine

↓

Intensity

0.35

↓

Duration

2 Seconds

↓

ScentRequestedEvent

↓

Device Controller

↓

ESP32

↓

Diffuse Pine
```

---

# Summary

The Scent Mapping module bridges the semantic world of AI with the physical world of scent.

It converts recognized environments into consistent, configurable scent experiences without depending on the underlying AI model or hardware implementation.

```text
Scene

↓

Lookup

↓

Scent

↓

Request

↓

Event Bus

↓

Device
```

By keeping mappings externalized in configuration files and separating them from application logic, SceneSense remains flexible, customizable, and ready to support richer scent profiles, blended fragrances, and new immersive devices in future releases.
