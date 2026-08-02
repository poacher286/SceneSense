# SceneSense Screen Capture APIs

> **Version:** 1.0  
> **Status:** Research  
> **Module:** `research`

---

# Table of Contents

1. Purpose
2. Problem Statement
3. Design Goals
4. Capture Pipeline
5. Capture Requirements
6. APIs Evaluated
7. Cross-Platform Considerations
8. Performance Comparison
9. Recommended Architecture
10. Security & Permissions
11. Future Improvements
12. Conclusion

---

# Purpose

SceneSense is built around the idea of **understanding what is visible on the user's display**.

Unlike game mods or engine plugins, SceneSense has no direct connection to a game. Instead, it continuously captures the screen, extracts semantic information using AI, and converts that understanding into scent events.

The choice of screen capture technology directly impacts:

- Latency
- CPU usage
- Memory usage
- Image quality
- Cross-platform compatibility
- Battery consumption

Selecting the correct capture API is therefore one of the most important architectural decisions.

---

# Problem Statement

Games are developed using many different technologies.

Examples include:

- Unreal Engine
- Unity
- Source Engine
- RE Engine
- Frostbite
- Decima
- Custom Engines

Each engine renders frames differently, making engine-specific integrations impractical.

Instead of integrating with individual games, SceneSense captures the final image that is already being displayed.

```text
Game

↓

Operating System

↓

Display

↓

Screen Capture

↓

AI

↓

Scene Recognition
```

This makes the system independent of any specific game.

---

# Design Goals

The capture system should:

- Work with every game
- Work with every application
- Be cross-platform
- Capture efficiently
- Avoid frame drops
- Require no game plugins
- Minimize latency
- Support multiple monitors
- Support fullscreen applications

---

# Capture Pipeline

```text
Desktop Display

↓

Capture API

↓

Raw Frame

↓

Resize

↓

Normalize

↓

AI Inference

↓

Scene Classification
```

The capture module produces raw images only. It performs no AI processing.

---

# Capture Requirements

Target requirements for Phase 1:

| Requirement | Target |
|-------------|--------|
| Resolution | 512 × 512 |
| FPS | 5 |
| Latency | < 50 ms |
| Memory Copies | Minimal |
| Multi-monitor | Supported |

Five frames per second is sufficient for semantic scene recognition while keeping CPU usage low.

---

# APIs Evaluated

Several capture technologies were evaluated for different operating systems.

---

# 1. MSS (Python)

Library:

```
mss
```

Platforms:

- macOS
- Windows
- Linux

Advantages:

- Cross-platform
- Lightweight
- Fast
- Pure Python interface
- Active maintenance

Disadvantages:

- Depends on OS-specific backends
- Limited advanced configuration

Performance:

★★★★★

Recommendation:

**Primary choice for Phase 1.**

---

# 2. Quartz Display Services (macOS)

Framework:

```
Quartz
```

Advantages:

- Native Apple API
- Excellent performance
- Stable
- Supports Retina displays

Disadvantages:

- macOS only
- More complex implementation

Suitable for future macOS-specific optimizations.

---

# 3. ScreenCaptureKit (macOS)

Introduced by Apple for modern screen capture.

Advantages:

- Extremely efficient
- GPU optimized
- Low latency
- Supports display selection
- Supports window capture

Disadvantages:

- macOS 12.3+
- Native implementation required

Future candidate for Phase 2.

---

# 4. DXGI Desktop Duplication (Windows)

Native Windows API.

Advantages:

- Very fast
- GPU accelerated
- Industry standard

Disadvantages:

- Windows only
- Native code required

Excellent future optimization.

---

# 5. Windows Graphics Capture API

Modern Windows capture framework.

Advantages:

- Better compatibility
- Lower latency
- Supports HDR

Future Windows implementation.

---

# 6. X11

Linux display server.

Advantages:

- Mature
- Well documented

Disadvantages:

- Being replaced by Wayland

Useful for legacy Linux support.

---

# 7. Wayland

Modern Linux display protocol.

Advantages:

- Improved security
- Better architecture

Disadvantages:

- Restricted screen capture
- Different implementation per compositor

Linux support requires additional research.

---

# 8. OpenCV Screen Capture

Possible using platform-specific wrappers.

Advantages:

- Familiar API

Disadvantages:

- Not optimized
- Additional copies
- Less efficient

Not recommended.

---

# 9. Game Engine Plugins

Examples:

- Unity Plugin
- Unreal Plugin

Advantages:

- Access to internal game state

Disadvantages:

- Requires per-game support
- High maintenance
- Not scalable

Rejected.

---

# API Comparison

| API | Platform | Speed | Ease of Use | Recommended |
|------|----------|-------|-------------|-------------|
| MSS | All | Excellent | Excellent | ✅ Phase 1 |
| Quartz | macOS | Excellent | Moderate | Future |
| ScreenCaptureKit | macOS | Excellent | Moderate | Future |
| DXGI | Windows | Excellent | Moderate | Future |
| Graphics Capture | Windows | Excellent | Moderate | Future |
| X11 | Linux | Good | Moderate | Legacy |
| Wayland | Linux | Good | Difficult | Future |
| OpenCV | All | Fair | Easy | No |

---

# Why MSS?

MSS provides the best balance of:

- Simplicity
- Performance
- Cross-platform compatibility
- Python integration

It allows SceneSense to focus on AI development rather than platform-specific capture code.

---

# Capture Frequency

SceneSense does not require 60 FPS capture.

Recommended rates:

| Use Case | FPS |
|----------|-----|
| Scene Recognition | 5 |
| Weather Detection | 5–10 |
| Event Detection | 10–15 |
| Future Action Detection | 15–30 |

Lower frame rates reduce CPU usage while remaining responsive for environmental changes.

---

# Resolution Strategy

Instead of capturing at full resolution:

```text
3840 × 2160

↓

Resize

↓

512 × 512
```

Benefits:

- Faster AI inference
- Lower memory usage
- Minimal loss of semantic information

Scene recognition generally does not require pixel-perfect detail.

---

# Multi-Monitor Support

Future versions should allow users to select:

- Primary monitor
- Secondary monitor
- Specific display

Capture flow:

```text
Available Displays

↓

User Selection

↓

Capture Selected Display
```

---

# Window Capture

Future support:

- Entire screen
- Specific application
- Specific game window

This reduces unnecessary processing.

---

# Fullscreen Compatibility

The capture system should support:

- Windowed mode
- Borderless fullscreen
- Exclusive fullscreen (where permitted by the OS)

Compatibility depends on operating system APIs.

---

# Memory Considerations

Avoid unnecessary copies.

Preferred pipeline:

```text
Capture Buffer

↓

Resize

↓

AI

↓

Discard
```

Frames should be processed in memory only.

---

# Latency Budget

Recommended target:

| Stage | Target |
|--------|--------|
| Capture | < 30 ms |
| Resize | < 10 ms |
| Queue | < 5 ms |

Total capture overhead:

```
< 50 ms
```

---

# Permissions

Some operating systems require explicit permission.

## macOS

Users must grant:

```
Screen Recording Permission
```

This permission allows reading pixels from the display but does **not** imply recording or storing gameplay.

---

## Windows

Most capture APIs require no additional user permissions.

---

## Linux

Behavior depends on:

- Wayland
- X11
- Desktop environment

---

# Privacy Considerations

SceneSense processes images:

- Locally
- In memory
- Without permanent storage

Frames are discarded immediately after AI inference.

No screenshots are saved by default.

---

# Error Handling

Possible failures:

- Permission denied
- Display disconnected
- Capture timeout
- Invalid display
- Unsupported API

Recovery strategy:

```text
Retry

↓

Fallback API

↓

Notify User
```

---

# Testing

## Functional Tests

Verify:

- Capture starts
- Correct display selected
- Image quality
- Resolution
- FPS

---

## Performance Tests

Measure:

- Capture latency
- CPU usage
- Memory usage
- Frame consistency

---

## Compatibility Tests

Test on:

- macOS
- Windows
- Linux

With:

- Single monitor
- Dual monitor
- High DPI displays
- Fullscreen games

---

# Future Improvements

## GPU Capture

Leverage GPU-native APIs:

- ScreenCaptureKit
- DXGI
- Metal
- DirectX

For lower latency and reduced CPU usage.

---

## Region Capture

Capture only relevant portions of the screen when appropriate.

---

## Dynamic FPS

Automatically adjust capture frequency based on:

- CPU load
- GPU load
- AI processing speed

---

## HDR Support

Future APIs should preserve HDR information where available.

---

## HDMI Capture

Support external HDMI capture devices.

This enables:

- PlayStation
- Xbox
- Nintendo Switch
- Streaming devices
- Smart TVs

Without requiring software on the gaming device.

---

# Best Practices

✔ Capture only what is needed

✔ Keep processing local

✔ Avoid unnecessary memory copies

✔ Resize before AI inference

✔ Use cross-platform APIs first

✔ Abstract platform-specific code

✔ Handle permissions gracefully

✔ Design for future hardware expansion

---

# Summary

Screen capture is the first stage of the SceneSense perception pipeline.

```text
Display

↓

Capture API

↓

Image

↓

AI

↓

Semantic Scene
```

For Phase 1, **MSS** provides the best combination of simplicity, reliability, and cross-platform support. As SceneSense evolves, platform-specific APIs such as **ScreenCaptureKit** on macOS and **DXGI Desktop Duplication** on Windows can further reduce latency and improve efficiency without changing the overall architecture.

By abstracting the capture layer behind a common interface, SceneSense remains portable across operating systems and future hardware platforms while maintaining a consistent AI pipeline.

---

# Appendix A – Recommended Capture Stack

| Platform | API |
|----------|-----|
| macOS | MSS (Phase 1), ScreenCaptureKit (Future) |
| Windows | MSS (Phase 1), DXGI Desktop Duplication (Future) |
| Linux | MSS (X11), Wayland-compatible backend (Future) |

---

# Appendix B – Capture Evolution

| Phase | Capture Technology |
|--------|--------------------|
| **Phase 1** | MSS, full-screen capture, 5 FPS |
| **Phase 2** | Native OS APIs, display selection |
| **Phase 3** | GPU-accelerated capture, adaptive FPS |
| **Phase 4** | HDMI capture devices for consoles and TVs |

This phased approach allows SceneSense to deliver a working, cross-platform prototype quickly while leaving room for substantial performance improvements as the project matures.