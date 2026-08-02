# SceneSense Performance

> **Version:** 1.0  
> **Status:** Phase 1 Design  
> **Module:** `performance`

---

# Table of Contents

1. Purpose
2. Performance Goals
3. Performance Philosophy
4. System Performance Targets
5. Performance Architecture
6. Latency Budget
7. Module Performance
8. Memory Management
9. CPU Optimization
10. Threading Model
11. Performance Monitoring
12. Benchmarking
13. Profiling
14. Testing
15. Future Improvements

---

# Purpose

Performance is critical to the success of SceneSense.

Unlike traditional desktop applications, SceneSense operates as a **real-time perception pipeline**, continuously analyzing the screen and triggering physical devices.

The primary objective is to:

> **Detect meaningful scene changes and activate scents with minimal perceived delay while keeping CPU and memory usage low.**

---

# Performance Goals

Phase 1 targets:

- Smooth real-time operation
- Low CPU usage
- Minimal memory footprint
- Fast AI inference
- Low latency hardware communication
- Stable long-running execution

The application should comfortably run in the background while a game is running.

---

# Performance Philosophy

Performance optimization follows three principles:

1. Measure before optimizing.
2. Optimize bottlenecks, not assumptions.
3. Favor simplicity over premature optimization.

Correctness is always prioritized over speed.

---

# High-Level Pipeline

```text
Screen

↓

Capture

↓

AI Inference

↓

Scene Stabilizer

↓

Decision Engine

↓

Scent Mapping

↓

Device Controller

↓

ESP32
```

Every stage contributes to total latency.

---

# End-to-End Latency Target

Recommended Phase 1 target:

```
Screen Change

↓

Scent Command

< 500 ms
```

This delay is short enough to feel responsive while avoiding unnecessary CPU usage.

---

# Latency Budget

| Module | Target |
|---------|--------|
| Screen Capture | < 50 ms |
| Image Resize | < 10 ms |
| AI Inference | < 200 ms |
| Scene Stabilizer | < 5 ms |
| Decision Engine | < 1 ms |
| Scent Mapping | < 1 ms |
| Event Bus | < 5 ms |
| Device Controller | < 100 ms |
| Serial Communication | < 50 ms |

Estimated total:

```
≈ 350–450 ms
```

---

# Capture Performance

Recommended settings:

| Parameter | Value |
|-----------|-------|
| FPS | 5 |
| Resolution | 512 × 512 |
| Queue Size | 3 |

Capturing more frames than the AI can process wastes CPU time.

---

# AI Performance

The AI Engine is expected to be the slowest stage.

Targets:

| Metric | Target |
|---------|--------|
| Model Load | < 5 s |
| Inference | < 200 ms |
| Confidence Calculation | < 1 ms |

Inference should run on GPU when available.

---

# Event Processing Performance

Events should introduce negligible overhead.

Target:

```
Publish Event

↓

Dispatch

↓

Subscriber

< 5 ms
```

Events should never become a bottleneck.

---

# Decision Engine Performance

Expected complexity:

```
O(1)
```

Operations include:

- Duplicate detection
- Cooldown checks
- Scene lookup
- Event creation

Target latency:

```
< 1 ms
```

---

# Scent Mapping Performance

Mapping uses an in-memory dictionary.

Target:

```
Lookup

↓

< 1 ms
```

No file access occurs after startup.

---

# Device Performance

Serial communication target:

```
Command

↓

ACK

< 100 ms
```

This excludes the physical scent diffusion time.

---

# Memory Usage

Recommended Phase 1 target:

| Component | Approximate Usage |
|-----------|-------------------|
| Capture Buffers | 20 MB |
| AI Model | 200–600 MB (depends on model) |
| Event Queue | < 5 MB |
| Configuration | < 1 MB |
| Logs | Rotating files |

Total application memory should remain manageable on modern systems.

---

# Memory Management

Best practices:

- Reuse image buffers.
- Avoid unnecessary copies.
- Release temporary tensors promptly.
- Keep queues bounded.
- Use immutable event objects.

Memory leaks must be treated as high-priority defects.

---

# CPU Utilization

Target CPU usage:

| System | Target |
|----------|--------|
| Idle | < 3% |
| Scene Detection | < 15% |
| Heavy Gameplay | < 25% |

Actual values depend on AI model and hardware.

---

# Threading Model

Recommended worker threads:

```text
Capture Thread

↓

AI Worker

↓

Decision Worker

↓

Device Worker

↓

UI Thread
```

Blocking operations should never run on the UI thread.

---

# Queue Management

Use bounded queues.

Example:

```
Queue Size

3
```

If full:

```
Drop Oldest Frame
```

Processing the newest frame is more valuable than processing every frame.

---

# Frame Dropping Strategy

Preferred policy:

```
Capture

↓

Queue Full

↓

Discard Oldest

↓

Insert Latest
```

This minimizes perceived latency.

---

# Performance Monitoring

Collect runtime metrics:

- FPS
- AI inference time
- Event queue size
- Queue latency
- Device response time
- Memory usage
- CPU usage

Metrics help identify performance regressions.

---

# Benchmarking

Benchmark each module independently.

Examples:

```
Capture

1000 Frames
```

Measure:

- Average capture time
- Worst-case capture time

Repeat for every module.

---

# Profiling

Recommended tools:

| Purpose | Tool |
|----------|------|
| CPU Profiling | cProfile |
| Line Profiling | line_profiler |
| Memory Profiling | memory_profiler |
| Visualization | SnakeViz |

Profile before optimizing.

---

# Long-Running Stability

SceneSense should operate continuously for extended periods.

Recommended stress test:

```
24 Hours

Continuous Capture

Continuous AI

Continuous Device Communication
```

Monitor:

- Memory growth
- CPU stability
- Queue behavior
- Thread health

---

# Performance Logging

Useful metrics:

```
Capture FPS

Inference Time

Decision Time

Queue Latency

Device Latency
```

Log periodic summaries instead of every frame.

---

# Configuration

Example:

```yaml
performance:

  target_fps: 5

  queue_size: 3

  enable_metrics: true

  enable_profiling: false
```

---

# Testing

## Unit Benchmarks

Measure:

- Decision latency
- Mapping lookup
- Event dispatch

---

## Integration Benchmarks

Measure:

```
Capture

↓

AI

↓

Decision
```

Latency between modules.

---

## End-to-End Benchmarks

Measure:

```
Screen Change

↓

Scent Command
```

Verify the overall latency target.

---

# Metrics Dashboard

Expose:

| Metric | Description |
|---------|-------------|
| FPS | Frames processed per second |
| Capture Time | Average capture latency |
| AI Time | Average inference latency |
| Decision Time | Rule evaluation latency |
| Queue Size | Pending events |
| Memory Usage | Current memory consumption |
| CPU Usage | Current processor utilization |
| Device Latency | Command round-trip time |

---

# Future Improvements

## GPU Acceleration

Use GPU inference when available.

---

## Dynamic FPS

Automatically adjust capture rate based on system load.

Example:

```
Idle

↓

5 FPS
```

```
High CPU

↓

3 FPS
```

---

## Adaptive Resolution

Lower capture resolution under heavy load.

---

## Parallel Inference

Future AI models may process multiple frames concurrently.

---

## Hardware Acceleration

Support:

- Apple Neural Engine
- CUDA
- DirectML
- OpenVINO

---

## Performance Dashboard

Future UI:

```
FPS

CPU

Memory

Latency

Device Status
```

Useful during development and troubleshooting.

---

# Best Practices

✔ Measure before optimizing

✔ Reuse buffers

✔ Keep queues bounded

✔ Avoid blocking operations

✔ Drop stale frames

✔ Profile regularly

✔ Optimize only bottlenecks

✔ Monitor long-running stability

---

# Example Performance Timeline

```text
Capture Frame           40 ms

↓

Resize Image             8 ms

↓

AI Inference           180 ms

↓

Scene Stabilizer         3 ms

↓

Decision Engine          1 ms

↓

Scent Mapping            1 ms

↓

Event Bus                2 ms

↓

Device Controller       60 ms

↓

Total                 ~295 ms
```

This comfortably meets the Phase 1 target.

---

# Summary

Performance is a foundational quality attribute of SceneSense.

```text
Capture

↓

Analyze

↓

Decide

↓

Trigger
```

Every module is designed with predictable latency, bounded resource usage, and long-term stability in mind. By continuously measuring, profiling, and optimizing the true bottlenecks, SceneSense can provide a responsive and immersive experience without significantly impacting game performance.

---

# Appendix A – Recommended Python Libraries

| Purpose | Library |
|----------|---------|
| Timing | `time.perf_counter()` |
| Profiling | `cProfile` |
| Line Profiling | `line_profiler` |
| Memory Profiling | `memory_profiler` |
| Process Metrics | `psutil` |
| Benchmarking | `pytest-benchmark` |

---

# Appendix B – Key Performance Indicators (KPIs)

| KPI | Target |
|------|--------|
| End-to-End Latency | < 500 ms |
| AI Inference | < 200 ms |
| Decision Engine | < 1 ms |
| Event Dispatch | < 5 ms |
| Serial Round Trip | < 100 ms |
| Memory Usage | Stable over 24 hours |
| CPU Usage | < 25% during gameplay |
| Frame Processing | 5 FPS |

Meeting these KPIs will ensure that SceneSense delivers timely scent activation while remaining lightweight enough to coexist with modern PC games.