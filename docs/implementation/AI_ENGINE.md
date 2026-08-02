# SceneSense AI Engine

> **Version:** 1.0  
> **Status:** Phase 1 Design  
> **Module:** `ai`

---

# Table of Contents

1. Purpose
2. Goals
3. Responsibilities
4. High-Level Architecture
5. AI Pipeline
6. Model Selection
7. Semantic Scene Recognition
8. Scene Labels
9. Inference Pipeline
10. Confidence Scoring
11. Prompt Engineering
12. Performance Optimization
13. Events
14. Configuration
15. Error Handling
16. Testing
17. Future Improvements

---

# Purpose

The AI Engine is responsible for understanding **what the player is currently experiencing**.

Unlike traditional game integrations, SceneSense has no knowledge of:

- The game title
- The game engine
- The level
- The map

Instead, it infers the current environment directly from screen pixels.

```
Frame

↓

AI Engine

↓

Scene Prediction
```

The output is a semantic description of the environment rather than raw image classifications.

---

# Goals

The AI Engine should:

- Be game-independent
- Support thousands of games
- Require zero game integration
- Operate in real time
- Produce confidence scores
- Be replaceable with future models

---

# Responsibilities

The AI Engine is responsible for:

- Image preprocessing
- AI inference
- Scene classification
- Confidence calculation
- Publishing prediction events

It is **not** responsible for:

- Capturing the screen
- Stabilizing predictions
- Triggering scents
- Hardware communication

---

# High-Level Architecture

```
Captured Frame

↓

Preprocessing

↓

Vision Model

↓

Prompt Matching

↓

Confidence Scores

↓

Best Scene

↓

SceneDetectedEvent
```

---

# AI Pipeline

```
Frame

↓

Resize

↓

Normalize

↓

Vision Encoder

↓

Embedding

↓

Compare With Labels

↓

Confidence Scores

↓

Top Prediction
```

---

# Why Semantic Scene Recognition?

Traditional object detection answers:

> "What objects exist?"

Examples:

- Tree
- Car
- Rock
- Person

SceneSense instead asks:

> "What environment does this represent?"

Examples:

- Forest
- Ocean
- Snow
- Rain
- Fire

This higher-level understanding maps naturally to scents.

---

# Model Selection

Phase 1 uses a zero-shot vision-language model.

Recommended options:

| Model | Status |
|---------|--------|
| CLIP | ✅ Recommended |
| SigLIP | Future |
| Florence-2 | Future |
| BLIP | Future |

The architecture abstracts model implementation so replacements require minimal changes.

---

# Why CLIP?

Advantages:

- Zero-shot classification
- Excellent semantic understanding
- No custom training required
- Mature ecosystem
- Fast inference
- Cross-platform

---

# AI Components

```
AI

├── Model Loader
├── Image Preprocessor
├── Prompt Generator
├── Inference Engine
├── Confidence Calculator
└── Prediction Publisher
```

---

# Folder Structure

```
ai/

pipeline/
    inference.py
    preprocessing.py
    prompts.py

models.py

labels/

clip_adapter.py
```

---

# Scene Labels

Instead of classes like:

```
Dog

Cat

Chair
```

SceneSense uses semantic prompts.

Examples:

```
A dense green forest

A rainy environment

A snowy landscape

An ocean view

A burning environment
```

The AI compares the image against these descriptions.

---

# Prompt Engineering

Example prompts:

```
"A lush green forest"

"A tropical beach"

"A cold snowy mountain"

"A peaceful ocean"

"A room filled with smoke"

"A cave"

"A rainy landscape"

"A city at night"
```

Well-designed prompts significantly improve recognition quality.

---

# Supported Scenes (Phase 1)

```
Forest

Rain

Ocean

Snow

Fire
```

Additional labels will be added in later phases.

---

# Image Preprocessing

Before inference:

```
Captured Frame

↓

Resize

↓

RGB Conversion

↓

Normalization

↓

Tensor

↓

Model
```

Recommended size:

```
512 × 512
```

---

# Inference Pipeline

```
Frame

↓

Vision Encoder

↓

Image Embedding

↓

Prompt Embeddings

↓

Cosine Similarity

↓

Confidence Scores

↓

Prediction
```

The highest confidence prediction becomes the current scene candidate.

---

# Confidence Scoring

Example output:

```
Forest      0.91

Rain        0.83

Ocean       0.21

Snow        0.09
```

The top prediction is published with its confidence score.

---

# Prediction Object

Example:

```python
@dataclass(frozen=True)
class ScenePrediction:
    scene: str
    confidence: float
    timestamp: datetime
```

This object is consumed by the Scene Stabilizer.

---

# Events

The AI Engine publishes:

```
SceneDetectedEvent
```

Example:

```python
SceneDetectedEvent(
    prediction=ScenePrediction(...)
)
```

Subscribers:

- Scene Stabilizer
- Logger
- Dashboard

---

# Performance Optimization

## Batch-Free Inference

Process one frame at a time.

Lower latency is preferred over throughput.

---

## Resize Early

Smaller images reduce inference time.

---

## Cached Prompt Embeddings

Text prompts never change.

Generate embeddings once during startup.

```
Startup

↓

Create Prompt Embeddings

↓

Cache

↓

Reuse
```

---

## Skip Duplicate Frames

If the capture module reports no meaningful screen change, AI inference can be skipped.

---

# Threading

AI runs independently from screen capture.

```
Capture Thread

↓

Frame Queue

↓

AI Thread

↓

Prediction Queue
```

This prevents capture from blocking during inference.

---

# Configuration

Example:

```yaml
ai:

  model: clip

  image_size: 512

  confidence_threshold: 0.80

  device: auto
```

Supported devices:

```
auto

cpu

gpu
```

---

# Logging

Useful logs include:

```
Model Loaded

Inference Started

Inference Finished

Prediction Published

Low Confidence

Inference Failed
```

Do not log every tensor or embedding.

---

# Error Handling

Possible failures:

- Model missing
- GPU unavailable
- Invalid image
- Inference timeout

Recovery:

```
Log

↓

Skip Frame

↓

Continue
```

The AI Engine should never terminate the application.

---

# Metrics

Expose:

| Metric | Description |
|----------|-------------|
| Inference Time | Average milliseconds |
| FPS | AI processing rate |
| Model | Current model |
| Device | CPU/GPU |
| Predictions | Total processed |
| Errors | Total failures |

---

# Testing

## Unit Tests

- Prompt generation
- Confidence calculation
- Label loading
- Preprocessing

---

## Integration Tests

- Capture → AI
- AI → Stabilizer

---

## Performance Tests

Measure:

- Average inference time
- Peak memory
- CPU utilization
- GPU utilization

---

# Future Improvements

Possible future enhancements:

## Better Models

- Florence
- SigLIP
- OpenCLIP
- Custom fine-tuned models

---

## Multi-Label Recognition

Example:

```
Forest

+

Rain

+

Night
```

Instead of a single scene.

---

## Temporary Event Detection

Examples:

- Explosion
- Gunfire
- Campfire
- Vehicle
- Magic

These would complement, not replace, the environment prediction.

---

## Adaptive Prompt Generation

Prompts could evolve based on user feedback or custom scent packs.

---

## Fine-Tuned Scene Models

Eventually, SceneSense may use a custom-trained model optimized specifically for gaming environments.

---

# Design Principles

The AI Engine should always be:

- Stateless
- Replaceable
- Game-independent
- Deterministic
- Fast
- Easy to benchmark

All downstream modules should consume standardized `ScenePrediction` objects rather than model-specific outputs.

---

# Sequence Diagram

```
FrameCapturedEvent

↓

Preprocess Frame

↓

Run Inference

↓

Generate Confidence Scores

↓

Create ScenePrediction

↓

Publish SceneDetectedEvent
```

---

# Summary

The AI Engine is the perception layer of SceneSense.

It transforms raw pixels into semantic understanding without relying on game-specific integrations.

```
Pixels

↓

Vision Model

↓

Semantic Scene

↓

Confidence

↓

Event Bus
```

By separating perception from decision-making, SceneSense remains flexible, allowing future AI models to be integrated with minimal impact on the rest of the system. This modular design ensures that improvements in computer vision can immediately enhance the immersive experience without requiring changes to the hardware or application architecture.