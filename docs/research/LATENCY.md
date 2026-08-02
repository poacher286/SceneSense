# SceneSense Latency Research

> **Version:** 1.0  
> **Status:** Research  
> **Module:** `research`

---

# Table of Contents

1. Purpose
2. Why Latency Matters
3. Human Perception
4. End-to-End Pipeline
5. Latency Budget
6. Sources of Latency
7. Measuring Latency
8. Optimization Strategies
9. Future Improvements
10. Conclusion

---

# Purpose

Latency is one of the most important factors affecting the quality of the SceneSense experience.

Unlike visual or audio feedback, scents take time to diffuse through the air. This means the software pipeline must react as quickly as possible to minimize the delay between an in-game event and the moment the player perceives the scent.

The objective is not to achieve zero latency—this is physically impossible—but to make the response feel natural and synchronized.

---

# What is Latency?

Latency is the total time between:

```text
Scene Changes

↓

Player Smells Scent
```

This includes every stage of the SceneSense pipeline.

---

# Why Latency Matters

Imagine the following situation:

```text
Explosion Happens

↓

Player Smells Smoke

10 Seconds Later
```

The experience feels disconnected.

Now compare it with:

```text
Explosion

↓

Smoke

300–500 ms Later
```

The scent feels associated with the event.

Small delays are acceptable because scent perception itself is slower than vision or hearing.

---

# Human Perception

Approximate sensory response times:

| Sense | Typical Response |
|--------|-----------------:|
| Vision | ~13–50 ms |
| Hearing | ~10–20 ms |
| Touch | ~100 ms |
| Smell | ~300–1000+ ms |

Unlike sound or visuals, smell naturally has a slower onset.

This gives SceneSense more flexibility than real-time audio systems.

---

# End-to-End Pipeline

```text
Game Renders Frame

↓

Operating System

↓

Screen Capture

↓

Image Processing

↓

AI Inference

↓

Scene Stabilization

↓

Decision Engine

↓

Event Bus

↓

Device Controller

↓

USB Serial

↓

ESP32

↓

Fan Starts

↓

Air Passes Through Cartridge

↓

Scent Reaches Player
```

Every stage contributes to total latency.

---

# Latency Budget

Recommended Phase 1 budget:

| Component | Target |
|-----------|--------:|
| Screen Capture | <30 ms |
| Resize & Preprocessing | <10 ms |
| AI Inference | <200 ms |
| Scene Stabilizer | <5 ms |
| Decision Engine | <1 ms |
| Event Bus | <5 ms |
| Device Controller | <20 ms |
| USB Communication | <20 ms |
| ESP32 Processing | <20 ms |
| Fan Spin-Up | <100 ms |
| Air Travel | ~100–300 ms |

Estimated total:

```
300–500 ms
```

This provides a responsive user experience while remaining achievable on consumer hardware.

---

# Types of Latency

## Capture Latency

Time required to read pixels from the display.

```text
Display

↓

Capture
```

Target:

```
<30 ms
```

---

## AI Latency

Time required for the model to understand the scene.

```text
Image

↓

Semantic Label
```

This is typically the most expensive software operation.

Target:

```
<200 ms
```

---

## Decision Latency

Time needed to determine whether a scent should be triggered.

Example:

```text
Forest

↓

Already Active?

↓

No

↓

Trigger Pine
```

Target:

```
<1 ms
```

---

## Communication Latency

Time required to deliver the command to the ESP32.

```text
Desktop

↓

USB

↓

ESP32
```

Target:

```
<20 ms
```

---

## Mechanical Latency

Time required for hardware to react.

Includes:

- Valve opening
- Fan acceleration
- Air movement

Unlike software latency, this cannot be eliminated completely.

---

## Diffusion Latency

Time for scented air to reach the player.

Depends on:

- Distance
- Airflow
- Fan speed
- Room conditions

Typical estimate:

```
100–300 ms
```

---

# Latency Timeline

Example:

```text
Frame Appears             0 ms

↓

Capture                  25 ms

↓

Resize                   8 ms

↓

AI Inference           170 ms

↓

Decision                 1 ms

↓

USB                     15 ms

↓

ESP32                   10 ms

↓

Fan Starts              60 ms

↓

Air Reaches Player     120 ms

↓

Total                 ~409 ms
```

---

# Measuring Latency

Latency should be measured end-to-end.

Recommended method:

1. Display a known visual event.
2. Trigger a scent.
3. Record both using a high-speed camera.
4. Calculate elapsed time.

This captures the true user experience.

---

# Software Profiling

Measure each stage independently.

Useful metrics:

- Capture time
- Queue wait time
- AI inference time
- Decision time
- Serial latency
- ESP32 execution time

Profiling helps identify bottlenecks.

---

# Hardware Profiling

Measure:

- Fan spin-up
- Valve activation
- Air velocity
- Diffusion distance

Mechanical improvements often provide greater gains than software optimizations.

---

# Latency Sources

Common contributors include:

- Large AI models
- High-resolution capture
- Excessive logging
- Slow serial communication
- Queue backlogs
- Slow fan acceleration
- Poor airflow design

Understanding these sources guides optimization efforts.

---

# Optimization Strategies

## Lower Capture Resolution

Instead of processing:

```
3840 × 2160
```

Resize to:

```
512 × 512
```

This significantly reduces AI inference time while preserving semantic information.

---

## Lower Capture Rate

Scene recognition rarely requires 60 FPS.

Recommended:

```
5 FPS
```

This lowers CPU usage without noticeably increasing perceived latency.

---

## Frame Dropping

If processing falls behind:

```text
Queue Full

↓

Discard Oldest Frame

↓

Process Latest
```

Fresh frames are more valuable than stale ones.

---

## Parallel Processing

Use independent threads for:

- Capture
- AI
- Decision
- Device communication

This keeps the pipeline flowing smoothly.

---

## GPU Acceleration

Where available:

- Apple Metal
- CUDA
- DirectML
- OpenVINO

GPU inference can significantly reduce AI latency.

---

## Preloaded Models

Load AI models once during startup.

Avoid loading models during gameplay.

---

# Latency vs Accuracy

Higher accuracy often increases latency.

Example:

| Model | Speed | Accuracy |
|--------|-------|----------|
| MobileNet | Fast | Moderate |
| CLIP | Fast | High |
| Florence-2 | Moderate | Very High |

For Phase 1, balance is more important than maximum accuracy.

---

# Latency Monitoring

The application should continuously monitor:

- Average latency
- Maximum latency
- 95th percentile latency
- Queue size
- AI inference time

Unexpected increases may indicate performance issues.

---

# Testing

## Unit Tests

Measure:

- Decision engine
- Event bus
- Serial communication

---

## Integration Tests

Measure:

```text
Capture

↓

AI

↓

Decision
```

---

## End-to-End Tests

Measure:

```text
Screen Change

↓

Scent Output
```

This is the most meaningful metric.

---

# Risks

Potential latency issues:

- Large AI models
- Low-end hardware
- USB disconnects
- Background CPU load
- Excessive scene changes

Mitigation strategies include adaptive frame rates and bounded queues.

---

# Future Improvements

## Predictive Scene Recognition

Recognize transitions before they complete.

Example:

```text
Entering Forest

↓

Preload Pine
```

This can reduce perceived latency.

---

## Dynamic AI Models

Switch between lightweight and heavyweight models depending on available system resources.

---

## Adaptive Capture Rate

Increase FPS during rapid scene changes and reduce it during static scenes.

---

## Hardware Optimization

Future diffuser versions may include:

- Faster valves
- Higher airflow fans
- Optimized air channels

These improvements reduce mechanical latency.

---

# Best Practices

✔ Measure real latency

✔ Optimize bottlenecks first

✔ Keep queues short

✔ Prefer recent frames

✔ Preload AI models

✔ Profile continuously

✔ Separate software and hardware timing

✔ Design with human perception in mind

---

# Example Latency Budget

```text
Capture             25 ms

↓

Preprocessing        8 ms

↓

AI                180 ms

↓

Decision            1 ms

↓

USB                15 ms

↓

ESP32              10 ms

↓

Fan                60 ms

↓

Air Travel        120 ms

↓

Total            ~419 ms
```

This meets the Phase 1 target while providing a responsive and immersive experience.

---

# Summary

Latency is a system-wide property that spans software, communication, hardware, and the physical behavior of scent diffusion.

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

↓

Perceive
```

The goal of SceneSense is to keep software latency as low as possible so that the unavoidable physical delay of scent delivery becomes the dominant factor. By optimizing each stage of the pipeline and continuously measuring real-world performance, SceneSense can provide timely, believable scent cues that enhance immersion without distracting the player.

---

# Appendix A – Target Latency Table

| Stage | Target |
|--------|--------:|
| Capture | <30 ms |
| Preprocessing | <10 ms |
| AI Inference | <200 ms |
| Decision Engine | <1 ms |
| Event Bus | <5 ms |
| Device Controller | <20 ms |
| USB Communication | <20 ms |
| ESP32 Processing | <20 ms |
| Mechanical Response | <100 ms |
| Air Travel | 100–300 ms |
| **End-to-End** | **300–500 ms** |

---

# Appendix B – Latency Evolution

| Phase | Goal |
|--------|------|
| **Phase 1** | <500 ms end-to-end |
| **Phase 2** | GPU acceleration, native capture APIs |
| **Phase 3** | Predictive scene recognition and adaptive frame rates |
| **Phase 4** | Optimized diffuser hardware and wireless communication |

This roadmap allows SceneSense to progressively reduce perceived latency while maintaining a modular architecture that can adopt future AI models and hardware improvements.