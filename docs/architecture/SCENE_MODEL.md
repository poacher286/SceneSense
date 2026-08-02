# SceneSense Scene Model

> **Version:** 1.0  
> **Status:** Active  
> **Audience:** Developers & AI Contributors

---

# Table of Contents

1. Purpose
2. What is a Scene?
3. Scene Hierarchy
4. Scene Classification Model
5. Scene Object
6. Scene Categories
7. Environmental Attributes
8. Transition Model
9. Confidence Model
10. Scene Mapping
11. Scene Lifecycle
12. Future Extensions
13. Summary

---

# Purpose

The Scene Model defines how SceneSense represents the user's environment after AI inference.

Rather than working with raw AI predictions or detected objects, every component in the application communicates using a standardized **Scene** object.

This abstraction keeps the architecture independent of the underlying AI model.

```
AI Model

↓

Scene

↓

Everything Else
```

---

# What is a Scene?

A **Scene** is the semantic description of what the user is currently experiencing.

A scene is **not**:

- A screenshot
- A list of detected objects
- A game title
- A game level

Instead, it describes the overall environment.

Examples:

| Screenshot Contains | Scene |
|----------------------|-------|
| Trees, rocks, grass | Forest |
| Sand, dunes, sky | Desert |
| Water, waves, beach | Ocean |
| Snow, ice, mountains | Snow |
| Smoke, flames | Fire |

---

# Scene Hierarchy

```
Scene
│
├── Environment
├── Weather
├── Time of Day
├── Mood (Future)
├── Temporary Events (Future)
└── Metadata
```

Example:

```
Forest
│
├── Rain
├── Day
└── Confidence 96%
```

---

# Scene Classification Model

For Phase 1, SceneSense supports a limited number of environments.

```
Environment

├── Forest
├── Rain
├── Ocean
├── Snow
└── Fire
```

These scenes provide enough variety to validate the end-to-end concept.

Additional environments can be introduced without changing the architecture.

---

# Scene Object

Every recognized environment is represented using a common object.

Example:

```python
Scene(
    environment="Forest",
    confidence=0.96,
    timestamp="2026-08-01T18:30:15Z"
)
```

Suggested dataclass:

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Scene:
    environment: str
    confidence: float
    timestamp: datetime
```

This object is immutable and can safely travel through the Event Bus.

---

# Scene Categories

## Phase 1

| Scene | Example Scent |
|--------|---------------|
| Forest | Pine |
| Rain | Petrichor |
| Ocean | Sea Breeze |
| Snow | Cold Mint |
| Fire | Smoke |

---

## Phase 2

Additional environments may include:

- Desert
- Beach
- Cave
- Mountain
- Jungle
- Village
- City
- Space
- Indoor
- Underwater

---

# Environmental Attributes

Future versions may enrich a scene with additional context.

Example:

```python
Scene(
    environment="Forest",
    weather="Rain",
    time_of_day="Night",
    confidence=0.95
)
```

Possible attributes include:

| Attribute | Examples |
|-----------|----------|
| Weather | Rain, Snow, Fog |
| Time | Day, Sunset, Night |
| Season | Spring, Winter |
| Temperature | Hot, Mild, Cold |
| Lighting | Bright, Dark |
| Visibility | Clear, Misty |

Phase 1 intentionally ignores these attributes to keep the model simple.

---

# Transition Model

SceneSense reacts to **changes**, not constant observations.

Example:

```
Forest

↓

Forest

↓

Forest
```

Result:

```
No Event
```

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

The Decision Engine compares consecutive stable scenes to determine whether a transition has occurred.

---

# Confidence Model

Every scene carries a confidence score produced by the AI model.

Example:

```python
Scene(
    environment="Ocean",
    confidence=0.93
)
```

Suggested confidence thresholds:

| Confidence | Action |
|------------|--------|
| ≥ 0.90 | Accept immediately |
| 0.80–0.89 | Accept after stabilization |
| < 0.80 | Ignore |

These thresholds should be configurable.

---

# Scene Mapping

The Scene object is translated into one or more physical outputs.

Example mapping:

| Scene | Scent |
|--------|-------|
| Forest | Pine |
| Rain | Petrichor |
| Ocean | Sea Breeze |
| Snow | Cold Mint |
| Fire | Smoke |

Future mappings may include:

| Scene | Light | Fan |
|--------|-------|-----|
| Forest | Green | Low |
| Ocean | Blue | Medium |
| Fire | Orange | Off |
| Snow | White | High |

The mapping layer remains separate from the AI model.

---

# Scene Lifecycle

```
Captured Frame

↓

AI Prediction

↓

Scene Object

↓

Confidence Filter

↓

Scene Stabilizer

↓

Decision Engine

↓

SceneChangedEvent

↓

Output Devices
```

The Scene object acts as the common language between all modules.

---

# Future Extensions

The Scene model is intentionally extensible.

Potential additions include:

## Weather

- Rain
- Snow
- Fog
- Storm

---

## Time of Day

- Dawn
- Morning
- Afternoon
- Sunset
- Night

---

## Temporary Events

Examples:

- Explosion
- Gunfire
- Campfire
- Vehicle
- Magic
- Lava

These events are short-lived and may trigger temporary scent effects without changing the primary environment.

---

## Mood

Possible emotional context:

- Peaceful
- Tense
- Horror
- Calm
- Dangerous

Mood should influence output intensity rather than replace the environment.

---

## Multi-Label Scenes

Future AI models may identify multiple simultaneous contexts.

Example:

```python
Scene(
    environment="Forest",
    weather="Rain",
    time_of_day="Night",
    temporary_event="Campfire"
)
```

This richer representation enables layered immersion.

---

# Serialization

The Scene object should be easy to serialize for logging, debugging, and event replay.

Example JSON:

```json
{
  "environment": "Forest",
  "confidence": 0.96,
  "timestamp": "2026-08-01T18:30:15Z"
}
```

Future fields can be added without breaking compatibility.

---

# Design Principles

The Scene model should always be:

- Immutable
- Lightweight
- Serializable
- Human-readable
- Independent of any AI model
- Independent of any hardware device

It represents **meaning**, not implementation details.

---

# Summary

The Scene Model is the central semantic representation within SceneSense.

It transforms raw AI predictions into a stable, standardized object that every module understands.

```
Game Frame

↓

AI Prediction

↓

Scene

↓

Decision

↓

Event

↓

Immersive Output
```

By introducing a common Scene abstraction, SceneSense decouples perception from hardware, enabling the platform to evolve with new AI models, richer environmental understanding, and additional immersive devices without changing the application's core architecture.