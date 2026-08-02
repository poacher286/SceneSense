# SceneSense Error Handling Strategy

> **Version:** 1.0  
> **Status:** Active  
> **Audience:** Developers & Contributors

---

# Table of Contents

1. Purpose
2. Design Philosophy
3. Error Handling Principles
4. Error Categories
5. Recovery Strategy
6. Module-Specific Error Handling
7. Logging Strategy
8. Retry Strategy
9. User Notifications
10. Exception Hierarchy
11. Failure Scenarios
12. Future Improvements
13. Summary

---

# Purpose

This document defines how SceneSense detects, reports, and recovers from errors.

The application is designed to run continuously while the user is gaming.

Because of this, **stability is more important than perfection**.

A single failed frame, disconnected device, or temporary AI error must **never** crash the application.

---

# Design Philosophy

SceneSense follows four principles.

## 1. Fail Gracefully

Errors should affect only the module where they occur.

Example:

```
USB Failure

↓

Device Module Stops

↓

AI Continues

↓

UI Continues
```

---

## 2. Recover Automatically

Whenever possible:

```
Error

↓

Retry

↓

Recover

↓

Continue
```

Manual intervention should be the exception.

---

## 3. Never Lose the Application

Modules may fail.

The application should not.

```
Module Failure

↓

Restart Module

↓

Continue Running
```

---

## 4. Log Everything Important

Every significant error should be logged with enough information for debugging.

---

# Error Handling Principles

Every module should:

- Catch its own exceptions
- Log failures
- Publish error events
- Continue running whenever possible
- Avoid propagating recoverable exceptions

No module should terminate the entire application.

---

# Error Categories

## Configuration Errors

Examples:

- Missing config file
- Invalid YAML
- Unknown settings
- Missing scent mapping

Severity: **High**

Recovery:

- Load defaults when possible
- Display warning
- Continue if safe

---

## Capture Errors

Examples:

- Window closed
- Permission denied
- Capture timeout

Severity: **Medium**

Recovery:

- Retry capture
- Notify UI
- Continue polling

---

## AI Errors

Examples:

- Model failed to load
- GPU unavailable
- Inference timeout
- Invalid prediction

Severity: **High**

Recovery:

- Log error
- Skip frame
- Retry inference
- Fall back to CPU (future)

---

## Decision Errors

Examples:

- Invalid scene
- Unknown mapping
- Rule evaluation failure

Severity: **Low**

Recovery:

- Ignore invalid scene
- Log warning
- Continue processing

---

## Device Errors

Examples:

- USB disconnected
- Serial timeout
- Invalid response
- ESP32 restart

Severity: **Medium**

Recovery:

- Attempt reconnect
- Notify UI
- Continue processing

---

## UI Errors

Examples:

- Widget failure
- Rendering issue

Severity: **Low**

Recovery:

- Log error
- Refresh affected component
- Keep backend running

---

# Recovery Strategy

Each module owns its recovery process.

```
Capture

↓

Retry
```

```
AI

↓

Skip Frame
```

```
Device

↓

Reconnect
```

```
Decision

↓

Ignore Event
```

No module should rely on another module to recover.

---

# Module-Specific Error Handling

## Capture Module

Possible failures:

- Invalid window
- Capture exception
- Frame unavailable

Recovery:

```
Retry after next capture interval
```

---

## AI Module

Possible failures:

- Model unavailable
- Inference failure
- Invalid tensor
- Memory error

Recovery:

```
Discard Frame

↓

Continue
```

Never reuse failed predictions.

---

## Stabilizer Module

Possible failures:

- Empty prediction buffer
- Invalid confidence

Recovery:

```
Clear Buffer

↓

Wait for New Predictions
```

---

## Decision Engine

Possible failures:

- Missing scent mapping
- Invalid rule
- Unknown scene

Recovery:

```
Log Warning

↓

Ignore Event
```

---

## Event Bus

Possible failures:

- Subscriber exception

Recovery:

```
Catch Exception

↓

Continue Delivering Event
```

One failing subscriber must not prevent other subscribers from receiving the event.

---

## Device Module

Possible failures:

- Serial port unavailable
- Timeout
- Write failure
- Device disconnected

Recovery:

```
Reconnect

↓

Retry Command
```

Maximum retry count should be configurable.

---

# Logging Strategy

Errors should include:

- Timestamp
- Module
- Severity
- Error code
- Stack trace (debug mode)
- Recovery action

Example:

```text
[2026-08-01 20:31:10]

ERROR

Module: AI

Code: AI001

Message:
Inference timeout.

Recovery:
Frame skipped.
```

---

# Retry Strategy

Not every error should be retried.

| Error | Retry |
|--------|-------|
| Frame capture failed | Yes |
| USB disconnected | Yes |
| Serial timeout | Yes |
| Invalid configuration | No |
| Unknown scene | No |
| Missing scent mapping | No |

Retrying unrecoverable errors wastes resources.

---

# User Notifications

The UI should distinguish between warnings and fatal errors.

Examples:

### Information

```
Device Connected
```

---

### Warning

```
Model confidence below threshold.
```

---

### Recoverable Error

```
ESP32 disconnected.

Attempting reconnection...
```

---

### Fatal Error

```
AI model could not be loaded.

SceneSense cannot continue.
```

Fatal errors should be rare and only occur when the application cannot perform its core function.

---

# Exception Hierarchy

A custom exception hierarchy improves clarity.

```text
SceneSenseError
│
├── ConfigurationError
├── CaptureError
├── AIError
├── StabilizerError
├── DecisionError
├── DeviceError
└── UIError
```

Modules should raise domain-specific exceptions rather than generic exceptions.

---

# Failure Scenarios

## AI Model Fails

```
Frame

↓

AI Exception

↓

Log

↓

Discard Frame

↓

Continue
```

---

## ESP32 Disconnects

```
Serial Error

↓

Reconnect

↓

Connected

↓

Continue
```

---

## Invalid Scene

```
Unknown Scene

↓

No Mapping

↓

Log Warning

↓

Ignore
```

---

## Capture Window Closed

```
Capture Failed

↓

Retry

↓

Notify User

↓

Wait for Window
```

---

## Subscriber Failure

```
SceneChanged

↓

Logger ✔

↓

Dashboard ✔

↓

Device ❌

↓

Continue
```

The Event Bus isolates subscriber failures.

---

# Error Events

Modules should publish standardized events when failures occur.

Examples:

```text
ConfigurationErrorEvent

CaptureErrorEvent

AIErrorEvent

DeviceErrorEvent

RecoverySucceededEvent
```

The UI and Logger can subscribe to these events.

---

# Future Improvements

Potential enhancements include:

- Automatic crash reports (opt-in)
- Error analytics
- Event replay
- Health monitoring dashboard
- Self-healing module restart
- Performance diagnostics
- Hardware diagnostics

These are intentionally outside the scope of Phase 1.

---

# Design Principles

Error handling should always be:

- Predictable
- Localized
- Recoverable
- Observable
- Testable

The goal is not to eliminate all failures.

The goal is to ensure failures remain isolated and the application continues delivering a good user experience.

---

# Summary

SceneSense is designed as a resilient, continuously running application.

Every module is responsible for its own failures, recovery, and logging.

```
Detect

↓

Log

↓

Recover

↓

Continue
```

By isolating errors and avoiding cascading failures, SceneSense can continue capturing scenes, recognizing environments, and triggering immersive experiences even when individual components encounter temporary problems.