# SceneSense Screen Capture Module

> **Version:** 1.0  
> **Status:** Phase 1 Design  
> **Module:** `capture`

---

# Table of Contents

1. Purpose
2. Design Goals
3. Requirements
4. Architecture
5. Capture Pipeline
6. Screen Capture Backend
7. Window Selection
8. Image Processing
9. Frame Rate Control
10. Threading Model
11. Events
12. Error Handling
13. Performance
14. Configuration
15. Testing
16. Future Improvements

---

# Purpose

The Screen Capture module is the **entry point** of the SceneSense pipeline.

Its responsibility is to continuously capture frames from the user's display and publish them to the Event Bus.

The Capture module **does not perform AI inference or make decisions**. Its only responsibility is to provide high-quality frames efficiently.

```
Desktop

↓

Capture

↓

FrameCapturedEvent
```

---

# Design Goals

The Screen Capture module should be:

- Fast
- Cross-platform
- Low CPU usage
- Independent of AI
- Independent of hardware
- Easily replaceable

---

# Functional Requirements

The module must:

- Capture the primary display
- Support full-screen games
- Support windowed games
- Run continuously
- Publish frames at a configurable FPS
- Handle monitor resolution changes
- Recover from temporary capture failures

---

# Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| Capture Rate | 5 FPS (default) |
| Capture Latency | < 50 ms |
| Memory Usage | < 100 MB |
| CPU Usage | < 10% (typical desktop) |

---

# Module Architecture

```
┌────────────────────┐
│ Screen Capture     │
└─────────┬──────────┘
          │
          ▼
 Window Manager
          │
          ▼
 Frame Grabber
          │
          ▼
 Image Preprocessor
          │
          ▼
 Frame Queue
          │
          ▼
 Event Bus
```

---

# Responsibilities

The Capture module is responsible for:

- Finding the correct display
- Capturing screen frames
- Basic preprocessing
- Publishing `FrameCapturedEvent`

The Capture module is **not** responsible for:

- AI inference
- Scene recognition
- Scent mapping
- Hardware communication

---

# Recommended Library

For Phase 1, use **MSS**.

Why MSS?

- Cross-platform
- Very fast
- Pure Python
- Minimal dependencies
- Works on macOS, Windows, and Linux

Example installation:

```bash
pip install mss
```

---

# Folder Structure

```text
capture/

screen_capture.py

window_manager.py

frame_provider.py

frame_processor.py
```

---

# Capture Pipeline

```
Display

↓

Capture Frame

↓

RGB Conversion

↓

Resize

↓

Timestamp

↓

FrameCapturedEvent

↓

Event Bus
```

Every frame follows the same pipeline.

---

# Screen Capture Backend

The `screen_capture.py` component is responsible for:

- Initializing MSS
- Selecting the monitor
- Capturing frames
- Returning images

Suggested interface:

```python
class ScreenCapture:

    def capture_frame(self) -> Frame:
        pass
```

This abstraction allows alternative backends in the future.

---

# Window Management

Initially, Phase 1 captures the **entire primary display**.

Future versions may capture:

- Active window
- Specific game window
- Multiple monitors

The `window_manager.py` module will encapsulate window-related logic.

---

# Frame Object

Every captured frame should use a common structure.

```python
from dataclasses import dataclass
from datetime import datetime
import numpy as np

@dataclass(frozen=True)
class Frame:
    image: np.ndarray
    width: int
    height: int
    timestamp: datetime
```

The Frame object is immutable and passed through the Event Bus.

---

# Image Preprocessing

Before publishing, minimal preprocessing is applied.

Steps:

1. Capture BGRA image
2. Convert to RGB
3. Resize (if required)
4. Validate dimensions

Example:

```
1920×1080

↓

RGB

↓

512×512

↓

Publish
```

Heavy preprocessing belongs in the AI module.

---

# Frame Rate Control

The capture rate is configurable.

Example:

```yaml
capture:
  fps: 5
```

The capture loop should sleep between iterations to maintain the target FPS.

The module should avoid capturing frames faster than the AI can process.

---

# Threading Model

Screen capture runs in its own thread.

```
Capture Thread

↓

Frame Queue

↓

AI Thread
```

The Capture thread should never block on AI inference.

If the queue becomes full:

- Drop the oldest frame
- Keep the newest frame

This minimizes latency.

---

# Queue Strategy

Recommended queue size:

```text
Queue Size = 3
```

Example:

```
Frame 1
Frame 2
Frame 3

↓

AI is slow

↓

Frame 1 discarded

↓

Frame 4 added
```

Fresh frames are more valuable than old frames.

---

# Events

The Capture module publishes:

```python
FrameCapturedEvent(
    frame=frame,
    timestamp=...
)
```

Subscribers:

- AI Pipeline
- Recorder (future)
- Debug Viewer (future)

---

# Error Handling

Possible failures:

- Permission denied
- Display disconnected
- Capture timeout
- Invalid monitor

Recovery strategy:

```
Capture Error

↓

Log

↓

Retry

↓

Continue
```

The application should never crash because of one failed capture.

---

# Configuration

Example configuration:

```yaml
capture:
  monitor: primary
  fps: 5
  resize_width: 512
  resize_height: 512
  queue_size: 3
```

All values should be configurable.

---

# Logging

The Capture module should log:

```
Capture started

Capture stopped

Monitor changed

Capture failed

Frame dropped
```

Avoid logging every frame to prevent excessive log volume.

---

# Testing

## Unit Tests

- Frame creation
- RGB conversion
- Resize logic
- Queue behavior

---

## Integration Tests

- Capture → AI
- Capture → Event Bus

---

## Manual Tests

- Full-screen game
- Windowed game
- Multiple monitors
- Display disconnect
- Long-duration capture

---

# Performance Optimization

Potential optimizations include:

## Resize Early

Resize immediately after capture to reduce memory and AI workload.

---

## Avoid Copies

Reuse buffers where possible.

Avoid unnecessary image duplication.

---

## Frame Skipping

If AI falls behind:

- Skip intermediate frames
- Process the latest frame

Real-time responsiveness is preferred over processing every frame.

---

# Future Improvements

Future enhancements may include:

- Active window capture
- Game window detection
- Region-of-interest capture
- Multi-monitor support
- GPU-accelerated capture
- HDR support
- Variable FPS
- Adaptive capture rate

These are outside the scope of Phase 1.

---

# Design Principles

The Screen Capture module should:

- Produce immutable Frame objects
- Avoid AI-specific logic
- Minimize latency
- Recover from failures
- Publish events only
- Remain platform-independent

---

# Sequence Diagram

```text
Application

↓

Capture Thread Started

↓

Capture Frame

↓

Create Frame Object

↓

Publish FrameCapturedEvent

↓

AI Receives Event

↓

Repeat
```

---

# Metrics

The module should expose runtime metrics:

| Metric | Description |
|---------|-------------|
| Capture FPS | Current capture rate |
| Average Capture Time | Time per frame |
| Frames Dropped | Queue overflow count |
| Capture Errors | Total failures |
| Active Monitor | Current monitor |

These metrics can be displayed in the dashboard.

---

# Summary

The Screen Capture module is responsible for delivering a continuous stream of fresh, high-quality frames into the SceneSense pipeline.

```
Display

↓

Capture

↓

Preprocess

↓

Frame

↓

Event Bus

↓

AI Pipeline
```

By keeping this module lightweight, independent, and focused solely on frame acquisition, SceneSense maintains low latency and a clean separation of concerns. Future capture technologies or platform-specific optimizations can be introduced without affecting the AI or downstream processing modules.