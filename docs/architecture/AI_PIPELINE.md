# AI Pipeline

> **Version:** 1.0  
> **Status:** Active  
> **Audience:** Developers & AI Contributors

---

# Table of Contents

1. Introduction
2. Objectives
3. Design Principles
4. AI Pipeline Overview
5. Stage 1 - Frame Capture
6. Stage 2 - Image Preprocessing
7. Stage 3 - Semantic Scene Recognition
8. Stage 4 - Confidence Filtering
9. Stage 5 - Scene Stabilization
10. Stage 6 - Decision Engine
11. Stage 7 - Event Generation
12. Model Selection
13. Performance Goals
14. Error Handling
15. Future Improvements
16. Summary

---

# Introduction

The AI Pipeline is the heart of SceneSense.

Its responsibility is **not** to recognize games or detect individual objects.

Instead, the pipeline understands the **semantic meaning** of what is currently displayed on the screen.

Example:

Instead of detecting:

```
Tree
Grass
Rock
```

The AI should understand:

```
Forest
```

That semantic understanding drives every immersion event.

---

# Objectives

The AI pipeline must:

- Understand environments
- Operate in real time
- Run entirely on the user's computer
- Produce stable predictions
- Avoid unnecessary hardware activations
- Be replaceable without affecting other modules

---

# Design Principles

The AI system follows these principles.

## Semantic Understanding

Recognize scenes rather than objects.

Example:

```
Snow

instead of

White pixels
Ice
Trees
```

---

## Local First

Inference happens locally.

Gameplay images are never uploaded.

---

## Model Agnostic

Any compatible vision model should be replaceable without changing the surrounding architecture.

---

## Stateless Inference

Each frame is evaluated independently.

Temporal consistency is handled by the **Scene Stabilizer**, not the AI model itself.

---

# AI Pipeline Overview

```
Game Window
      │
      ▼
Screen Capture
      │
      ▼
Image Preprocessing
      │
      ▼
Semantic Scene Recognition
      │
      ▼
Confidence Filtering
      │
      ▼
Scene Stabilizer
      │
      ▼
Decision Engine
      │
      ▼
SceneChanged Event
      │
      ▼
Event Bus
```

---

# Stage 1 — Frame Capture

The Capture module continuously retrieves frames from the selected window.

Responsibilities:

- Capture active window
- Convert to RGB
- Resize if necessary
- Forward image to AI

The AI never captures its own frames.

---

## Input

```
Desktop Image
```

---

## Output

```python
FrameCapturedEvent
```

---

# Stage 2 — Image Preprocessing

Before inference, images are normalized.

Possible preprocessing steps:

- Resize
- RGB conversion
- Normalization
- Tensor conversion

Example

```
1920x1080

↓

512x512

↓

Tensor
```

The exact preprocessing depends on the selected AI model.

---

# Stage 3 — Semantic Scene Recognition

This is the core AI stage.

The model predicts the current environment.

Example:

Input

```
Game Frame
```

Output

```json
{
    "scene": "Forest",
    "confidence": 0.96
}
```

The prediction represents a **scene**, not a list of detected objects.

---

## Initial Scene Categories

Phase 1 supports a small vocabulary.

| Scene | Example Scent |
|--------|---------------|
| Forest | Pine |
| Rain | Petrichor |
| Ocean | Sea Breeze |
| Snow | Cold Mint |
| Fire | Smoke |

These categories are intentionally limited for the MVP.

---

# Stage 4 — Confidence Filtering

Not every prediction should be accepted.

Example

```
Forest

Confidence

22%
```

This prediction should be ignored.

Only predictions above a configurable threshold proceed.

Example configuration:

```yaml
ai:
  confidence_threshold: 0.80
```

---

# Stage 5 — Scene Stabilization

Predictions fluctuate because of:

- Camera movement
- Motion blur
- Lighting changes
- HUD overlays
- Temporary effects

Example:

```
Forest
Forest
Trees
Forest
Grass
Forest
```

The stabilizer produces:

```
Forest
```

Suggested techniques:

- Sliding window
- Majority voting
- Confidence weighting
- Exponential smoothing

The stabilizer is responsible for temporal consistency—not the AI model.

---

# Stage 6 — Decision Engine

The Decision Engine compares the current stable scene with the previous one.

Example

```
Previous

Forest

Current

Forest
```

Result

```
No Action
```

Example

```
Previous

Forest

Current

Rain
```

Result

```
SceneChangedEvent
```

Additional responsibilities:

- Cooldowns
- Duplicate suppression
- Future rule evaluation

---

# Stage 7 — Event Generation

When a meaningful transition occurs, the Decision Engine publishes a standardized event.

Example

```python
SceneChangedEvent(
    previous_scene="Forest",
    current_scene="Rain",
    confidence=0.95
)
```

Subscribers decide how to react.

Examples:

- Diffuser
- Dashboard
- Logger

The AI never interacts with hardware directly.

---

# Model Selection

The architecture should support multiple vision models.

Potential candidates:

| Model | Purpose | Phase |
|--------|----------|-------|
| OpenAI CLIP | Zero-shot scene recognition | Phase 1 |
| SigLIP | Improved semantic understanding | Future |
| Florence-2 | Multi-task vision | Future |
| Qwen2.5-VL | Vision-language reasoning | Future |

The AI module should expose a common interface so models can be swapped without affecting downstream components.

---

# Suggested Interface

```python
class SceneRecognizer:

    def predict(frame) -> ScenePrediction:
        pass
```

Example return object:

```python
ScenePrediction(
    scene="Forest",
    confidence=0.96
)
```

---

# Performance Goals

| Metric | Target |
|--------|--------|
| Capture Rate | 5 FPS |
| AI Inference | <100 ms |
| Total Pipeline | <1 second |
| Memory Usage | <500 MB |
| CPU Usage | Minimize continuous load |

These values are guidelines for the MVP and may be refined through benchmarking.

---

# Error Handling

AI failures should not stop the application.

Example

```
Frame

↓

Inference Error

↓

Log Error

↓

Discard Frame

↓

Continue Processing
```

If the model becomes unavailable:

- notify the UI
- log the failure
- continue attempting inference

---

# Future Improvements

Potential enhancements include:

### Expanded Scene Vocabulary

- Desert
- City
- Village
- Cave
- Beach
- Mountain
- Space

---

### Weather Recognition

- Rain
- Snow
- Fog
- Storm
- Sunshine

---

### Event Detection

Temporary events such as:

- Explosion
- Campfire
- Vehicle
- Lava
- Magic
- Smoke

These events may trigger short-lived scent effects.

---

### Multi-Modal Context

Future versions may combine:

- Vision
- Audio
- Game metadata (where available)

to improve scene understanding.

---

### Adaptive Models

Possible future capabilities:

- Dynamic model switching
- Hardware-aware optimization
- GPU/CPU selection
- Quantized models

These enhancements are intentionally out of scope for Phase 1.

---

# Pipeline Example

```
Game Window

↓

Capture Frame

↓

Preprocess Image

↓

CLIP Prediction

↓

Forest (96%)

↓

Confidence Filter

↓

Scene Stabilizer

↓

Forest

↓

Decision Engine

↓

SceneChangedEvent

↓

Event Bus

↓

Device Controller

↓

SPRAY:PINE
```

---

# Summary

The AI Pipeline converts raw visual data into semantic understanding through a sequence of focused processing stages.

```
Pixels

↓

Semantic Scene

↓

Stable Context

↓

Meaningful Transition

↓

Standardized Event
```

By separating perception, stabilization, and decision-making, SceneSense remains modular, efficient, and adaptable. New AI models can be introduced without affecting hardware integration or application logic, allowing the platform to evolve while preserving a stable architectural foundation.