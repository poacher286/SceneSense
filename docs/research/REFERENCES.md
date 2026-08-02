# SceneSense References

> **Version:** 1.0  
> **Status:** Research  
> **Module:** `research`

---

# Table of Contents

1. Purpose
2. Research Philosophy
3. AI & Computer Vision
4. Screen Capture Technologies
5. Machine Learning Frameworks
6. Python Libraries
7. Hardware References
8. Communication Protocols
9. Scientific Research
10. Human Olfaction
11. Gaming Industry
12. Future Reading
13. Development Tools
14. Licensing
15. Acknowledgements

---

# Purpose

This document contains the primary references, research papers, open-source projects, technical documentation, and industry standards used during the design and development of **SceneSense**.

Rather than reinventing existing solutions, SceneSense builds upon decades of research in:

- Computer Vision
- Artificial Intelligence
- Human-Computer Interaction
- Embedded Systems
- Real-Time Systems
- Olfactory Interfaces
- Gaming Technologies

---

# Research Philosophy

The project follows these principles:

- Prefer proven technologies.
- Use open standards whenever possible.
- Build on well-maintained open-source software.
- Keep all AI processing local.
- Prioritize cross-platform compatibility.

---

# Artificial Intelligence

## OpenAI CLIP

Purpose:

Zero-shot image classification using natural language.

Research Paper:

> Learning Transferable Visual Models From Natural Language Supervision

Authors:

- Alec Radford
- Jong Wook Kim
- Chris Hallacy
- et al.

Publisher:

OpenAI

Why it matters:

CLIP enables SceneSense to recognize environments without training a custom model.

---

## Florence-2

Publisher:

Microsoft Research

Purpose:

Vision Foundation Model

Capabilities:

- Captioning
- Detection
- OCR
- Region Understanding

Why it matters:

Potential future AI engine for SceneSense.

---

## BLIP / BLIP-2

Publisher:

Salesforce Research

Purpose:

Image Captioning

Potential future use:

Generate richer environmental descriptions before scent mapping.

---

## SigLIP

Publisher:

Google Research

Purpose:

Improved vision-language embeddings.

Potential future replacement for CLIP.

---

## Segment Anything Model (SAM)

Publisher:

Meta AI

Purpose:

Image segmentation.

Potential future use:

Separate foreground from environmental background.

---

## YOLO

Publisher:

Ultralytics

Purpose:

Object detection.

Potential future use:

Recognize gameplay events such as:

- Fire
- Vehicle
- Weapon
- Animal

---

# Machine Learning Frameworks

## PyTorch

Used for:

- AI inference
- Model loading
- Tensor operations

Advantages:

- Excellent ecosystem
- Large community
- Strong GPU support

---

## ONNX Runtime

Purpose:

Cross-platform inference.

Benefits:

- Faster inference
- Multiple hardware backends
- Optimized deployment

Future optimization target.

---

## Hugging Face Transformers

Purpose:

Access to pretrained AI models.

Used for:

- CLIP
- Florence
- BLIP
- SigLIP

Provides a unified interface for state-of-the-art models.

---

# Screen Capture

## MSS

Purpose:

Cross-platform screen capture.

Platforms:

- Windows
- macOS
- Linux

Selected as the Phase 1 implementation.

---

## ScreenCaptureKit

Platform:

macOS

Purpose:

Modern GPU-accelerated capture.

Future optimization.

---

## DXGI Desktop Duplication

Platform:

Windows

Purpose:

Native high-performance capture.

Future optimization.

---

## Quartz Display Services

Platform:

macOS

Purpose:

Native screen capture.

Useful for advanced platform-specific features.

---

# Computer Vision Libraries

## OpenCV

Used for:

- Image resizing
- Image conversion
- Basic preprocessing

Not used for scene understanding itself.

---

## Pillow (PIL)

Used for:

- Image loading
- Format conversion
- Buffer manipulation

---

# Python Libraries

Core libraries planned for Phase 1:

| Library | Purpose |
|----------|---------|
| mss | Screen capture |
| OpenCV | Image preprocessing |
| Pillow | Image utilities |
| NumPy | Numerical computing |
| PyTorch | AI inference |
| Transformers | AI models |
| PySerial | ESP32 communication |
| PyYAML | Configuration |
| Loguru / Logging | Logging |
| pytest | Testing |

---

# Embedded Systems

## ESP32

Manufacturer:

Espressif Systems

Role:

Hardware controller.

Responsibilities:

- Receive commands
- Drive valves
- Control fan
- Execute diffusion events

---

# Communication

## USB Serial

Purpose:

Desktop ↔ ESP32 communication.

Phase 1 transport.

---

## JSON

Purpose:

Human-readable communication protocol.

Advantages:

- Easy debugging
- Language independent
- Extensible

---

# Scientific Research

Relevant fields:

- Computer Vision
- Deep Learning
- Pattern Recognition
- Real-Time Systems
- Human Perception
- Human-Computer Interaction

These disciplines provide the theoretical foundation for SceneSense.

---

# Human Olfaction

Relevant research topics:

- Scent perception latency
- Olfactory adaptation
- Fragrance diffusion
- Cross-sensory perception
- Environmental scent recognition

These studies influence:

- Diffusion duration
- Cooldown periods
- Intensity mapping
- Scent transitions

---

# Human-Computer Interaction (HCI)

Relevant concepts:

- Multisensory interfaces
- Immersive experiences
- User feedback loops
- Attention management
- Cognitive load

SceneSense extends traditional audiovisual interaction with controlled olfactory feedback.

---

# Gaming Technologies

SceneSense is intentionally game-independent.

Target compatibility includes games built with:

- Unreal Engine
- Unity
- Source Engine
- RE Engine
- Frostbite
- Godot
- Decima
- Custom engines

No engine-specific APIs are required.

---

# Development Tools

Recommended tools:

| Tool | Purpose |
|------|---------|
| VS Code | Development |
| PyCharm | Python IDE |
| Git | Version control |
| GitHub | Source repository |
| PlatformIO | ESP32 development |
| Arduino IDE | Firmware prototyping |
| CMake | Future native components |

---

# Testing Tools

Suggested tools:

- pytest
- unittest
- time.perf_counter
- cProfile
- memory_profiler

Future:

- py-spy
- Perfetto
- Instruments (macOS)
- Windows Performance Analyzer

---

# Hardware Components

Prototype hardware:

- ESP32 DevKit
- PWM Fan
- MOSFET Driver
- Solenoid Valves
- USB-C Power
- 3D Printed Enclosure
- Replaceable Scent Cartridges

---

# Standards

Relevant standards include:

- USB Serial Communication
- JSON Specification
- UTF-8 Encoding
- Semantic Versioning
- IEEE Floating Point
- YAML Configuration

---

# Licensing Considerations

SceneSense should respect the licenses of all third-party software.

Common licenses include:

- MIT
- Apache 2.0
- BSD
- GPL (evaluate carefully before inclusion)

Every dependency should be reviewed before distribution.

---

# Future Research Topics

Potential future areas of investigation:

- Event detection using multimodal AI
- Predictive scene recognition
- Dynamic scent blending
- Emotional state recognition
- Weather estimation
- Indoor airflow simulation
- Adaptive fragrance intensity
- Reinforcement learning for scent timing

---

# Books

Recommended reading:

### Computer Vision

- Computer Vision: Algorithms and Applications — Richard Szeliski

### Deep Learning

- Deep Learning — Ian Goodfellow, Yoshua Bengio, Aaron Courville

### Pattern Recognition

- Pattern Recognition and Machine Learning — Christopher Bishop

### Human-Computer Interaction

- Designing Interactive Systems — David Benyon

---

# Conferences

Useful conferences:

- CVPR
- ICCV
- ECCV
- NeurIPS
- ICML
- SIGGRAPH
- CHI
- ICRA

These conferences often introduce technologies relevant to future SceneSense improvements.

---

# Online Resources

Useful documentation sources:

- Python Documentation
- PyTorch Documentation
- Hugging Face Documentation
- OpenCV Documentation
- PlatformIO Documentation
- Espressif ESP32 Documentation
- Apple Developer Documentation
- Microsoft Learn
- Linux Kernel Documentation

---

# Best Practices

✔ Prefer actively maintained libraries

✔ Use pretrained foundation models

✔ Keep dependencies minimal

✔ Validate licenses

✔ Track upstream updates

✔ Document technology decisions

✔ Benchmark before replacing components

✔ Favor portability over platform-specific optimizations

---

# Acknowledgements

SceneSense is inspired by decades of work in:

- Artificial Intelligence
- Embedded Systems
- Computer Vision
- Human-Computer Interaction
- Game Development
- Open Source Software

The project would not be possible without the contributions of researchers, engineers, and open-source communities around the world.

---

# Summary

This reference collection represents the technical foundation on which SceneSense is built.

```text
Computer Vision

↓

AI Models

↓

Screen Capture

↓

Embedded Systems

↓

Human Perception

↓

SceneSense
```

By relying on established research, widely adopted libraries, and proven engineering practices, SceneSense minimizes technical risk while remaining flexible enough to adopt future advances in AI, computer vision, hardware control, and multisensory interaction.

---

# Appendix A – Core Technologies

| Category | Selected Technology |
|----------|---------------------|
| Language | Python |
| AI Framework | PyTorch |
| Model Access | Hugging Face Transformers |
| Initial AI Model | CLIP |
| Screen Capture | MSS |
| Image Processing | OpenCV |
| Communication | USB Serial (JSON) |
| Microcontroller | ESP32 |
| Configuration | YAML |
| Testing | pytest |

---

# Appendix B – Technology Evolution

| Phase | Primary Focus |
|--------|---------------|
| **Phase 1** | CLIP, MSS, USB Serial, ESP32 |
| **Phase 2** | Native screen capture APIs, GPU inference |
| **Phase 3** | Florence-2, event detection, adaptive processing |
| **Phase 4** | HDMI capture, console support, predictive AI, multi-device ecosystem |

This roadmap ensures that the core technology stack remains modern, maintainable, and capable of supporting SceneSense's long-term vision of bringing environmental scents to games across PCs, consoles, and future entertainment platforms.