# SceneSense AI Models

> **Version:** 1.0  
> **Status:** Research  
> **Module:** `research`

---

# Table of Contents

1. Purpose
2. Problem Statement
3. AI Requirements
4. Vision Pipeline
5. Model Categories
6. Evaluated Models
7. Model Comparison
8. Recommended Architecture
9. Why Semantic Scene Recognition
10. Hardware Considerations
11. Future Models
12. Conclusion

---

# Purpose

Artificial Intelligence is the core technology behind SceneSense.

Unlike traditional automation software that relies on predefined rules or direct game integration, SceneSense observes what is visible on the screen and understands the scene in a human-like way.

The AI system answers a simple question:

> **"What environment is currently being displayed?"**

Examples:

```
Dense Forest

↓

Trigger Pine
```

```
Ocean

↓

Trigger Sea Breeze
```

```
Heavy Rain

↓

Trigger Petrichor
```

The AI never needs to know which game is running.

---

# Problem Statement

Games use different:

- Graphics engines
- Lighting systems
- Camera angles
- HUD layouts
- Art styles

A rule-based system would require game-specific integrations.

Instead, SceneSense recognizes **semantic meaning**, not pixels.

Example:

```
The Last of Us

Forest
```

```
Skyrim

Forest
```

```
Minecraft

Forest
```

Although visually different, all represent the same environment.

---

# Design Goals

The AI should:

- Work with any game
- Require no plugins
- Require no game APIs
- Work offline
- Be fast
- Be accurate
- Understand environments
- Ignore HUD elements
- Ignore UI overlays
- Scale to future platforms

---

# High-Level AI Pipeline

```text
Screen Capture

↓

Image Resize

↓

Image Normalization

↓

Semantic Scene Recognition

↓

Scene Stabilizer

↓

Decision Engine

↓

Scent Mapping
```

---

# Why Semantic Scene Recognition?

SceneSense is interested in **meaning**, not objects.

Example:

Image contains:

- Trees
- Grass
- River
- Mountains

Instead of detecting:

```
Tree

Grass

Rock
```

We want:

```
Forest
```

This dramatically simplifies scent selection.

---

# AI Model Categories

Several AI approaches were evaluated.

---

# 1. CNN Classification

Examples:

- ResNet
- EfficientNet
- MobileNet

Advantages:

- Small
- Fast
- Easy deployment

Disadvantages:

- Limited understanding
- Requires custom training
- Poor zero-shot performance

Conclusion:

Not suitable for SceneSense.

---

# 2. Object Detection

Examples:

- YOLO
- DETR
- Grounding DINO

Purpose:

Detect objects.

Example:

```
Tree

Rock

Car

Person
```

Advantages:

Very fast.

Disadvantages:

SceneSense needs environments rather than individual objects.

Conclusion:

Useful as a future enhancement.

---

# 3. Image Captioning

Examples:

- BLIP
- BLIP-2
- Florence-2

Output:

```
"A snowy mountain overlooking a frozen lake."
```

Advantages:

Rich semantic understanding.

Disadvantages:

Slightly slower than classifiers.

Excellent candidate.

---

# 4. Vision-Language Models

Examples:

- CLIP
- SigLIP
- Florence-2

These models understand relationships between images and text.

Example:

Compare image against labels:

```
Forest

Ocean

Rain

Snow

Desert
```

Highest similarity wins.

Advantages:

- Zero-shot
- No retraining
- Very flexible

Excellent choice.

---

# 5. Segmentation Models

Examples:

- SAM
- MobileSAM

Purpose:

Separate image regions.

Useful for:

- Sky
- Water
- Ground

SceneSense does not require segmentation in Phase 1.

---

# Models Evaluated

## OpenAI CLIP

Strengths

- Extremely popular
- Zero-shot
- Fast
- Huge community

Weaknesses

- Limited descriptive capability
- Older architecture

Suitability:

★★★★★

---

## SigLIP

Google's successor to CLIP.

Advantages:

- Better embeddings
- Better accuracy
- Faster convergence

Suitability:

★★★★★

---

## Florence-2

Microsoft's vision foundation model.

Capabilities:

- Captioning
- Detection
- OCR
- Region understanding
- Prompt-based inference

Advantages:

Very versatile.

Suitability:

★★★★★

Recommended for future versions.

---

## BLIP-2

Advantages:

Very strong image descriptions.

Disadvantages:

Large memory footprint.

Suitability:

★★★★☆

---

## MobileNet

Advantages:

Tiny model.

Disadvantages:

Needs training.

Poor semantic understanding.

Suitability:

★★☆☆☆

---

## EfficientNet

Advantages:

Fast.

Disadvantages:

Classification only.

Suitability:

★★★☆☆

---

## YOLOv11

Purpose:

Object detection.

Excellent for:

```
Person

Gun

Car

Animal
```

Not suitable for environment classification alone.

Suitability:

★★★☆☆

---

# Comparison

| Model | Speed | Accuracy | Zero-shot | Recommended |
|---------|----------|----------|------------|------------|
| CLIP | Excellent | Excellent | Yes | ✅ |
| SigLIP | Excellent | Excellent | Yes | ✅ |
| Florence-2 | Very Good | Excellent | Yes | ⭐ Best Long-term |
| BLIP-2 | Good | Excellent | Yes | Future |
| MobileNet | Excellent | Fair | No | No |
| EfficientNet | Excellent | Good | No | No |
| YOLO | Excellent | Object Only | N/A | Future |

---

# Recommended Phase 1 Model

Recommended stack:

```
OpenAI CLIP
```

Reasons:

- Mature
- Stable
- Fast
- Offline
- Easy deployment
- Huge ecosystem
- Excellent semantic understanding

---

# Recommended Future Model

Phase 2+

```
Florence-2
```

Reasons:

- Rich scene understanding
- Better captions
- Multi-task
- Future-proof

---

# Why Not OCR?

OCR only reads text.

Games contain:

- Graphics
- Landscapes
- Lighting
- Weather

Very little useful text.

Therefore OCR adds little value.

---

# Why Not Color Detection?

Simple color rules fail.

Example:

Blue screen:

```
Ocean

OR

Sky

OR

Menu

OR

Magic

OR

Ice
```

Semantic AI solves this ambiguity.

---

# Scene Categories

Phase 1 recognizes:

- Forest
- Rain
- Ocean
- Desert
- Snow
- Mountain
- Cave
- Fire
- Grassland
- Urban
- Night
- Day
- Beach

Future versions may support hundreds of scene labels.

---

# Confidence Score

Example:

```
Forest

96%
```

Only high-confidence predictions trigger scent events.

Suggested threshold:

```
85%
```

---

# Hardware Requirements

Minimum:

- 8 GB RAM
- Quad-core CPU

Recommended:

- Apple M-Series
- NVIDIA GPU
- 16 GB RAM

---

# GPU Acceleration

Supported backends:

- Apple Metal
- CUDA
- DirectML
- ONNX Runtime
- OpenVINO

Phase 1 primarily targets CPU execution with optional GPU acceleration.

---

# Memory Usage

Approximate:

| Model | Memory |
|---------|---------|
| CLIP | 300 MB |
| SigLIP | 350 MB |
| Florence-2 | 700+ MB |
| BLIP-2 | >1 GB |

---

# Performance Targets

Desired inference:

```
<200 ms
```

Target throughput:

```
5 FPS
```

This is sufficient for scene recognition while keeping CPU usage reasonable.

---

# Why Not Train Our Own Model?

Training requires:

- Large dataset
- Labeling
- GPU resources
- Ongoing maintenance

Foundation models already provide excellent generalization.

Using pretrained models significantly accelerates development.

---

# Future AI Roadmap

## Phase 1

Semantic scene recognition.

---

## Phase 2

Weather recognition.

---

## Phase 3

Event recognition.

Examples:

- Explosion
- Gunfire
- Vehicle
- Waterfall

---

## Phase 4

Scene blending.

Example:

```
70% Forest

30% Rain
```

---

## Phase 5

Temporal understanding.

Instead of analyzing a single frame:

```
Video

↓

Context

↓

Scene Evolution
```

This enables smoother transitions and better event detection.

---

# Risks

Potential challenges:

- Stylized graphics
- Abstract art styles
- Dark scenes
- Motion blur
- Menus mistaken for gameplay

These are mitigated through:

- Scene stabilization
- Confidence thresholds
- Cooldowns
- Temporal averaging

---

# Best Practices

✔ Use pretrained foundation models

✔ Keep inference local

✔ Avoid game-specific rules

✔ Ignore HUD

✔ Use semantic understanding

✔ Stabilize predictions

✔ Optimize for latency

✔ Design for future model upgrades

---

# Summary

SceneSense relies on **semantic scene recognition** rather than game integration, object detection, or handcrafted rules.

```text
Screen

↓

AI Model

↓

Semantic Scene

↓

Decision Engine

↓

Scent
```

For Phase 1, **CLIP** offers the best balance of speed, simplicity, and zero-shot capability, making it an excellent starting point. As the project evolves, more advanced vision-language models such as **Florence-2** can provide richer environmental understanding, weather recognition, and event awareness without changing the overall architecture.

The AI layer is intentionally modular, allowing newer models to replace older ones as computer vision technology advances while preserving the rest of the SceneSense pipeline.