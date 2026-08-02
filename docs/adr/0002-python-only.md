# ADR-0002: Python-Only Implementation for Phase 1

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
5. Why Python
6. Alternatives Considered
7. Trade-offs
8. Consequences
9. Future Evolution
10. Summary

---

# Status

**Accepted**

SceneSense Phase 1 will be implemented entirely in **Python**, including:

- Desktop application
- Screen capture
- AI inference
- Decision engine
- Event bus
- Configuration
- Device communication
- Testing

The only exception is the embedded firmware, which runs on the ESP32 and is written in C++ using the Arduino framework or PlatformIO.

---

# Context

During the initial design of SceneSense, several implementation approaches were considered.

Possible technology stacks included:

- Java + Python
- Python only
- C++
- Rust
- Go
- Electron + Python
- C#/.NET

The project combines:

- Computer Vision
- AI inference
- Image processing
- Real-time event processing
- USB communication
- Hardware control

The chosen language needed to support all of these efficiently while keeping development simple.

---

# Problem Statement

Choosing the wrong primary language could lead to:

- Increased complexity
- Slower development
- Duplicate implementations
- Difficult AI integration
- Higher maintenance costs
- Platform-specific issues

A single, well-supported language simplifies both architecture and onboarding.

---

# Decision

**Python is the primary language for the SceneSense desktop application.**

Python will be used for:

```text
Application

↓

Screen Capture

↓

AI Models

↓

Decision Engine

↓

Configuration

↓

Serial Communication

↓

Testing

↓

Utilities
```

No Java desktop application or secondary runtime is required for Phase 1.

---

# Why Python?

Python provides the strongest ecosystem for the type of work SceneSense performs.

Key advantages include:

- Excellent AI ecosystem
- Mature computer vision libraries
- Cross-platform support
- Fast prototyping
- Large community
- Strong hardware support
- Rich testing ecosystem

---

# AI Ecosystem

SceneSense relies heavily on modern AI models.

Python is the first-class language for:

- PyTorch
- Hugging Face Transformers
- ONNX Runtime
- OpenCV
- NumPy

Most new vision-language models are released with Python APIs first.

Choosing another language would add unnecessary integration complexity.

---

# Computer Vision

Required capabilities include:

- Image preprocessing
- Resizing
- Color conversion
- Buffer manipulation

Python provides mature libraries:

- OpenCV
- Pillow
- NumPy

These libraries are widely used and actively maintained.

---

# Screen Capture

Phase 1 uses the `mss` library for screen capture.

Benefits:

- Cross-platform
- Lightweight
- Python-native
- Easy integration

This avoids platform-specific implementations during the MVP stage.

---

# Hardware Communication

Python offers reliable serial communication through:

- PySerial

This supports:

- ESP32
- Arduino-compatible devices
- USB serial debugging

No custom drivers are required.

---

# Rapid Development

SceneSense is an experimental product.

Python enables:

- Fast iteration
- Quick testing
- Easier debugging
- Shorter development cycles

This is especially valuable during early prototyping.

---

# Readability

Python emphasizes readability.

Example:

```python
scene = detector.detect(frame)

if scene != previous_scene:
    event_bus.publish(SceneChanged(scene))
```

The intent is immediately clear, improving maintainability.

---

# Cross-Platform Support

Python runs consistently on:

- macOS
- Windows
- Linux

This aligns directly with the project's cross-platform principle.

---

# Community Support

Python has a vast ecosystem for:

- AI
- Image processing
- Automation
- Embedded systems
- Scientific computing

Most technical issues already have established solutions.

---

# Testing

Python provides excellent testing tools:

- pytest
- unittest
- pytest-cov
- mocking utilities

This supports automated testing from the start.

---

# Configuration

Python works naturally with:

- YAML
- JSON
- TOML
- Environment variables

No additional frameworks are required.

---

# Alternatives Considered

## Java

### Advantages

- Excellent tooling
- Strong type system
- Mature desktop ecosystem
- Good concurrency

### Disadvantages

- Limited AI ecosystem
- Additional Python integration required
- Duplicate runtime complexity

**Decision:** Rejected.

Java would still require Python for AI inference, increasing maintenance.

---

## C++

### Advantages

- Very high performance
- Native APIs
- Low memory overhead

### Disadvantages

- Slower development
- Higher complexity
- Less accessible to contributors
- More difficult AI integration

**Decision:** Deferred.

Suitable for future optimization of isolated performance-critical components.

---

## Rust

### Advantages

- Memory safety
- Excellent performance
- Modern language features

### Disadvantages

- Smaller AI ecosystem
- Steeper learning curve
- Fewer vision-related libraries

**Decision:** Rejected for Phase 1.

---

## Go

### Advantages

- Simple syntax
- Strong concurrency
- Fast compilation

### Disadvantages

- Limited AI tooling
- Smaller computer vision ecosystem

**Decision:** Rejected.

---

## C#

### Advantages

- Excellent Windows support
- Strong tooling

### Disadvantages

- Less portable
- Smaller AI ecosystem compared to Python
- Additional platform considerations

**Decision:** Rejected.

---

## Hybrid (Java + Python)

### Advantages

- Strong desktop UI
- AI support

### Disadvantages

- Two runtimes
- Inter-process communication
- Increased maintenance
- More complicated deployment

**Decision:** Rejected.

Keeping a single runtime greatly simplifies the architecture.

---

# Trade-offs

## Advantages

- Rapid development
- Mature AI libraries
- Excellent readability
- Large community
- Easy testing
- Cross-platform
- Minimal complexity

---

## Disadvantages

- Slower than native languages
- Higher memory usage
- Global Interpreter Lock (GIL)
- Packaging complexity on some platforms

These limitations are acceptable because AI inference and screen capture dominate runtime costs rather than pure Python execution.

---

# Performance Considerations

Python is sufficiently fast for Phase 1.

Performance targets:

| Metric | Target |
|--------|--------:|
| Capture FPS | 5 |
| AI Inference | <200 ms |
| End-to-End Latency | <500 ms |

If future profiling identifies Python bottlenecks, isolated modules may be optimized without changing the overall architecture.

---

# Consequences

## Positive

- Faster MVP development
- Easier onboarding
- Single-language codebase
- Simplified debugging
- Reduced maintenance
- Seamless AI integration

---

## Negative

- Native performance optimizations may require additional work later.
- Packaging desktop applications requires platform-specific tooling.
- Very high frame-rate processing may benefit from native extensions.

These trade-offs are acceptable for the project's goals.

---

# Future Evolution

Python remains the primary orchestration language.

Future optimizations may introduce native components for specific workloads.

Examples:

- C++ image preprocessing
- Rust device drivers
- Metal-based GPU inference
- CUDA acceleration

These components should expose clean Python interfaces.

The overall architecture should remain Python-centric.

---

# Non-Goals

This decision does **not** imply:

- Python will be used for ESP32 firmware.
- Native code is prohibited.
- Performance optimization is unnecessary.

It simply establishes Python as the primary application language for Phase 1.

---

# Related ADRs

- ADR-0001 — Project Principles
- ADR-0003 — Semantic Scene Recognition
- ADR-0004 — Local Processing
- ADR-0005 — Event-Driven Architecture

---

# Summary

SceneSense adopts Python as the single implementation language for the desktop application because it provides the best balance of:

```text
AI Ecosystem

↓

Rapid Development

↓

Cross-Platform Support

↓

Maintainability

↓

Future Extensibility
```

While native languages may offer higher raw performance, Python's unmatched ecosystem for AI, computer vision, automation, and testing makes it the most practical choice for building the Phase 1 MVP. The architecture intentionally allows performance-critical components to be optimized later without abandoning Python as the primary orchestration layer.

---

# Appendix A – Technology Comparison

| Language | AI Ecosystem | Performance | Development Speed | Cross-Platform | Selected |
|----------|--------------|-------------|-------------------|----------------|----------|
| Python | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ |
| Java | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ |
| C++ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ❌ |
| Rust | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ❌ |
| Go | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ |
| C# | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ❌ |

---

# Appendix B – Language Responsibilities

```text
Python
│
├── Screen Capture
├── AI Inference
├── Image Processing
├── Decision Engine
├── Event Bus
├── Device Communication
├── Configuration
├── Logging
├── Testing
└── CLI

ESP32 Firmware (C++)
│
├── Serial Parsing
├── Fan Control
├── Valve Control
├── PWM Output
└── Device Status
```

This separation keeps the desktop application focused on high-level intelligence while the ESP32 firmware handles deterministic, low-level hardware control, resulting in a clean and maintainable system architecture.