# SceneSense Performance Research

> **Version:** 1.0  
> **Status:** Research  
> **Module:** `research`

---

# Table of Contents

1. Purpose
2. Performance Philosophy
3. System Performance Goals
4. Performance Metrics
5. Performance Pipeline
6. CPU Performance
7. GPU Acceleration
8. Memory Optimization
9. Threading Model
10. AI Performance
11. Bottleneck Analysis
12. Benchmark Strategy
13. Future Optimizations
14. Conclusion

---

# Purpose

Performance is a fundamental requirement for SceneSense.

The application continuously captures the screen, performs AI inference, and communicates with external hardware while the user is playing games. Any excessive CPU usage, memory consumption, or latency can negatively impact gameplay and reduce immersion.

The objective is to build a system that delivers real-time scene understanding while remaining lightweight enough to run alongside modern games.

---

# Performance Philosophy

SceneSense follows four core principles:

- **Responsiveness** — Deliver scent events quickly.
- **Efficiency** — Minimize CPU, GPU, and memory usage.
- **Scalability** — Support both entry-level and high-end systems.
- **Predictability** — Maintain consistent performance over long gaming sessions.

Performance improvements should never compromise stability or user privacy.

---

# Performance Goals

Phase 1 targets:

| Metric | Target |
|--------|---------|
| CPU Usage | <15% (average) |
| Memory Usage | <500 MB |
| AI Inference | <200 ms |
| Capture FPS | 5 FPS |
| End-to-End Latency | <500 ms |
| Startup Time | <3 seconds |

These values provide a good balance between responsiveness and resource usage.

---

# High-Level Performance Pipeline

```text
Screen Capture

↓

Frame Queue

↓

Resize

↓

AI Inference

↓

Scene Stabilizer

↓

Decision Engine

↓

Device Controller

↓

ESP32
```

Each stage is measured independently to identify bottlenecks.

---

# Performance Metrics

The application should continuously monitor:

- CPU utilization
- GPU utilization
- RAM usage
- AI inference time
- Capture time
- Queue length
- Average FPS
- USB communication latency
- Device response time

These metrics should be available through debug logging or a future diagnostics dashboard.

---

# CPU Performance

The CPU is responsible for:

- Screen capture
- Image preprocessing
- AI inference (Phase 1)
- Decision engine
- Communication
- Logging

To reduce contention with the running game:

- Avoid busy waiting.
- Minimize allocations.
- Reuse buffers.
- Keep background threads lightweight.

---

# Multi-Core Utilization

SceneSense is designed to take advantage of multiple CPU cores.

Recommended thread allocation:

```text
Core 1

Screen Capture
```

```text
Core 2

AI Inference
```

```text
Core 3

Decision Engine
```

```text
Core 4

Device Communication
```

The operating system ultimately schedules threads, but the application should avoid unnecessary synchronization.

---

# GPU Acceleration

Phase 1 is CPU-first for simplicity.

Future versions may use:

- Apple Metal
- CUDA
- DirectML
- OpenVINO
- ONNX Runtime GPU

GPU inference becomes increasingly valuable as larger vision-language models are adopted.

---

# Memory Management

Memory should remain stable over long sessions.

Strategies:

- Reuse image buffers
- Avoid unnecessary copies
- Release temporary objects promptly
- Cache reusable model resources

Target:

```
No continuous memory growth
```

Memory leaks are unacceptable for a long-running desktop application.

---

# Image Optimization

Instead of processing full-resolution frames:

```text
3840 × 2160

↓

Resize

↓

512 × 512
```

Benefits:

- Faster inference
- Lower memory usage
- Reduced cache pressure

Semantic scene recognition does not require native display resolution.

---

# Threading Model

Independent worker threads improve responsiveness.

Recommended architecture:

```text
Capture Thread

↓

Inference Thread

↓

Decision Thread

↓

Communication Thread
```

Each thread performs a single responsibility.

---

# Producer–Consumer Pattern

Frame processing follows a producer–consumer model.

```text
Capture Thread

↓

Frame Queue

↓

AI Worker
```

This decouples capture from inference and prevents temporary AI slowdowns from blocking screen acquisition.

---

# Queue Strategy

The frame queue should remain small.

Example:

```
Maximum Queue Size = 2
```

If full:

```text
Drop Oldest Frame

↓

Keep Latest Frame
```

Fresh frames are more valuable than processing stale data.

---

# AI Performance

Inference is typically the most expensive stage.

Performance targets:

| Model | Target |
|--------|--------:|
| CLIP | <200 ms |
| SigLIP | <200 ms |
| Florence-2 | <500 ms |

Model selection should consider both accuracy and inference speed.

---

# Model Loading

AI models should load once during startup.

```text
Application Starts

↓

Load Model

↓

Gameplay Begins
```

Reloading models during gameplay should be avoided.

---

# Caching

Safe to cache:

- Model weights
- Tokenized labels
- Configuration
- Device information

Do not cache:

- Gameplay frames
- Screenshots
- User content

This supports both performance and privacy.

---

# Logging Performance

Logging should be asynchronous where possible.

Recommended:

- INFO for lifecycle events
- DEBUG for diagnostics
- ERROR for failures

Avoid excessive logging inside high-frequency loops.

---

# I/O Performance

Disk activity should be minimal during gameplay.

Avoid:

- Saving frames
- Large log files
- Frequent configuration writes

Most processing should remain entirely in memory.

---

# Bottleneck Analysis

Likely bottlenecks:

1. AI inference
2. Screen capture
3. Memory copies
4. Serial communication
5. Mechanical diffuser response

Each should be profiled independently.

---

# Profiling

Useful profiling metrics:

- Capture duration
- Resize duration
- AI inference time
- Queue wait time
- Decision time
- Serial write time
- End-to-end latency

Profiling should be part of regular development.

---

# Benchmark Strategy

Testing should include:

- Idle desktop
- 1080p games
- 1440p games
- 4K games
- Multiple monitors
- High CPU load
- High GPU load

This ensures predictable behavior across different environments.

---

# Hardware Recommendations

### Minimum

- Quad-core CPU
- 8 GB RAM
- Integrated GPU
- USB 2.0

### Recommended

- Apple M-Series
- AMD Ryzen 5+
- Intel Core i5+
- 16 GB RAM
- USB 3.0

### High-End

- Apple M3/M4
- Ryzen 7/9
- Intel Core i7/i9
- NVIDIA RTX GPU
- 32 GB RAM

---

# Performance Testing

## Unit Tests

Measure:

- Queue operations
- Decision engine
- Configuration loading

---

## Integration Tests

Measure:

```text
Capture

↓

Inference

↓

Decision
```

---

## Stress Tests

Run continuously for:

```
8 Hours
```

Monitor:

- CPU
- RAM
- Thread count
- Queue stability
- Device communication

---

## Long-Term Stability

Target:

```
No crashes

No leaks

No degraded performance
```

After extended operation.

---

# Future Optimizations

## GPU Inference

Move AI workloads to GPU where available.

---

## Dynamic Capture Rate

Automatically adjust FPS based on:

- CPU load
- GPU load
- AI processing time

---

## Adaptive Resolution

Reduce input resolution on slower systems.

---

## Multiple AI Workers

Future architectures may process multiple frames in parallel.

---

## Native Capture APIs

Replace generic libraries with:

- ScreenCaptureKit (macOS)
- DXGI (Windows)

To reduce capture overhead.

---

## SIMD Optimizations

Leverage CPU vector instructions for preprocessing.

Examples:

- NEON (Apple Silicon)
- AVX2
- AVX-512

---

## Hardware Telemetry

Future diagnostics may expose:

- CPU temperature
- GPU utilization
- Fan speed
- USB throughput

This assists with troubleshooting and optimization.

---

# Best Practices

✔ Keep queues small

✔ Reuse memory

✔ Process only recent frames

✔ Load AI models once

✔ Separate responsibilities across threads

✔ Minimize disk I/O

✔ Profile continuously

✔ Optimize based on measured data

---

# Example Performance Timeline

```text
Capture             25 ms

↓

Resize               8 ms

↓

Inference          180 ms

↓

Decision             1 ms

↓

USB                 15 ms

↓

ESP32               10 ms

↓

Mechanical         150 ms

↓

Total             ~389 ms
```

This comfortably meets the Phase 1 target of under 500 ms.

---

# Summary

Performance is a balance between speed, efficiency, and stability.

```text
Capture

↓

Understand

↓

Decide

↓

Transmit

↓

Diffuse
```

SceneSense achieves this by processing only a small number of frames, using lightweight semantic models, minimizing memory copies, and separating work across independent threads. The architecture is intentionally designed so that future improvements—such as GPU inference, native screen capture APIs, and adaptive processing—can be introduced without requiring major changes to the overall system.

---

# Appendix A – Target Performance Table

| Metric | Goal |
|--------|------:|
| CPU Usage | <15% |
| Memory Usage | <500 MB |
| Capture FPS | 5 |
| AI Inference | <200 ms |
| End-to-End Latency | <500 ms |
| Startup Time | <3 s |
| Queue Size | ≤2 frames |

---

# Appendix B – Performance Roadmap

| Phase | Focus |
|--------|-------|
| **Phase 1** | CPU-based inference, MSS capture, fixed 5 FPS |
| **Phase 2** | Native screen capture APIs, adaptive FPS |
| **Phase 3** | GPU acceleration, dynamic resolution, advanced profiling |
| **Phase 4** | Distributed AI, multiple diffusers, predictive processing |

This roadmap enables SceneSense to begin with a simple and dependable architecture while providing a clear path toward high-performance, production-ready deployments across a wide range of hardware configurations.