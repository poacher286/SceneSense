# SceneSense Logging

> **Version:** 1.0  
> **Status:** Phase 1 Design  
> **Module:** `logging`

---

# Table of Contents

1. Purpose
2. Design Goals
3. Logging Philosophy
4. Logging Architecture
5. Log Levels
6. Log Categories
7. Log Format
8. Log Files
9. Structured Logging
10. Performance Considerations
11. Error Logging
12. Configuration
13. Log Rotation
14. Testing
15. Future Improvements

---

# Purpose

Logging is one of the most important infrastructure components in SceneSense.

The goal of logging is to make it easy to understand:

- What happened?
- When did it happen?
- Why did it happen?
- Which module caused it?

Good logging dramatically reduces debugging time and provides insight into application behavior during development, testing, and production.

---

# Design Goals

The logging system should be:

- Consistent
- Lightweight
- Structured
- Human-readable
- Machine-parsable
- Configurable
- Thread-safe

---

# Logging Philosophy

Every significant event in the system should answer four questions:

```
What happened?

When?

Where?

Why?
```

Avoid excessive logging while ensuring enough information exists to diagnose issues.

---

# High-Level Architecture

```text
Application Modules

↓

Logger

↓

Console

↓

Log Files

↓

Future Dashboard / Analytics
```

All modules log through a centralized logging service.

---

# Log Levels

SceneSense uses standard logging levels.

| Level | Purpose |
|--------|---------|
| DEBUG | Detailed diagnostic information |
| INFO | Normal application flow |
| WARNING | Recoverable issues |
| ERROR | Failures affecting functionality |
| CRITICAL | Application cannot continue |

---

## DEBUG

Used during development.

Examples:

- Frame captured
- AI inference started
- Queue size updated
- Event dispatched

Should generally be disabled in production.

---

## INFO

Normal application events.

Examples:

```
Application Started

Configuration Loaded

Model Initialized

Device Connected

Scent Triggered
```

---

## WARNING

Unexpected but recoverable situations.

Examples:

```
Unknown Scene

Low AI Confidence

Frame Dropped

Retry Attempt
```

---

## ERROR

Failures requiring attention.

Examples:

```
Serial Timeout

Model Load Failure

Configuration Error

Capture Failed
```

---

## CRITICAL

Application cannot continue.

Examples:

```
No Configuration Found

Unsupported Python Version

Failed to Initialize Event Bus
```

Application startup should stop after critical failures.

---

# Log Categories

Each module should have its own logical logger.

Examples:

```
capture

ai

stabilizer

decision

device

events

config

ui

application
```

This makes filtering easier.

---

# Directory Structure

```text
logs/

application.log

capture.log

ai.log

decision.log

device.log

events.log

errors.log
```

Each module may log independently while sharing a common format.

---

# Log Format

Recommended format:

```text
2026-08-01 21:15:32.184

INFO

AI

Forest detected

confidence=0.93
```

Structured example:

```text
timestamp | level | module | message | metadata
```

---

# Structured Logging

Each log entry should include contextual metadata.

Example:

```json
{
  "timestamp": "2026-08-01T21:15:32.184Z",
  "level": "INFO",
  "module": "ai",
  "message": "Scene detected",
  "scene": "Forest",
  "confidence": 0.93
}
```

Structured logs simplify searching and analysis.

---

# Logging Pipeline

```text
Module

↓

Logger

↓

Formatter

↓

File Handler

↓

Console Handler
```

Additional handlers can be added later.

---

# Module Logging Examples

## Capture

```
Capture Started

Capture Stopped

Frame Dropped

Monitor Changed
```

---

## AI

```
Model Loaded

Inference Started

Inference Completed

Prediction Published

Low Confidence
```

---

## Stabilizer

```
Prediction Buffered

Stable Scene Published

Scene Transition Detected
```

---

## Decision Engine

```
Scene Accepted

Duplicate Ignored

Cooldown Active

Scent Requested
```

---

## Device

```
Device Connected

Command Sent

ACK Received

Retry

Disconnected

Reconnect Successful
```

---

## Event Bus

```
Subscriber Registered

Event Published

Queue Overflow

Dispatch Completed
```

---

# Correlation IDs

Each request flowing through the pipeline should carry a correlation ID.

Example:

```text
FrameCapturedEvent

↓

frame_id = 4128

↓

SceneDetectedEvent

↓

frame_id = 4128

↓

StableSceneDetectedEvent

↓

frame_id = 4128
```

This allows tracing a frame from capture to scent activation.

---

# Performance Logging

Useful metrics:

```
Capture FPS

Inference Time

Queue Latency

Decision Time

Device Response Time
```

Performance logs help identify bottlenecks.

---

# Exception Logging

Always log:

- Exception type
- Message
- Stack trace
- Module
- Correlation ID

Example:

```
ERROR

Device

TimeoutError

Serial write timed out

frame_id=4128
```

Never swallow exceptions silently.

---

# Sensitive Information

Do **not** log:

- User credentials
- API keys
- Secrets
- Personal information

Configuration values containing secrets should be redacted.

---

# Configuration

Example:

```yaml
logging:

  level: INFO

  console: true

  file: true

  json: false

  rotation: daily

  retention_days: 30
```

---

# Log Rotation

Recommended rotation:

```
Daily
```

Retention:

```
30 Days
```

Compressed archives:

```
application.log

↓

application.log.1.gz
```

Older logs may be automatically deleted.

---

# Performance Considerations

Logging should never significantly impact application performance.

Guidelines:

- Avoid logging every frame in production.
- Use lazy string formatting.
- Write asynchronously when possible.
- Limit DEBUG logs during continuous capture.

---

# Testing

## Unit Tests

- Formatter
- Log levels
- File creation
- Rotation
- Structured output

---

## Integration Tests

- Startup logging
- Module logging
- Exception logging
- Rotation behavior

---

## Manual Tests

Verify:

- Correct log files
- Correct timestamps
- Rotation
- Correlation IDs
- Log readability

---

# Metrics

Expose logging metrics:

| Metric | Description |
|---------|-------------|
| Total Log Entries | Number of entries written |
| Errors Logged | Total ERROR level entries |
| Warnings Logged | Total WARNING level entries |
| Log File Size | Current size |
| Rotation Count | Number of rotations |
| Average Write Time | Logging overhead |

---

# Future Improvements

## JSON Logging

Default to JSON for production.

Benefits:

- Machine-readable
- ELK compatible
- Easier analytics

---

## Remote Logging

Future cloud logging support.

```
Application

↓

Cloud Collector

↓

Dashboard
```

---

## Live Log Viewer

The desktop application may include a real-time log console for developers.

---

## Log Search

Built-in filtering:

```
Level

Module

Time Range

Correlation ID
```

---

## Telemetry

Anonymous performance metrics (optional and opt-in) could help improve future versions.

---

# Best Practices

✔ Log meaningful events

✔ Include context

✔ Use appropriate log levels

✔ Avoid duplicate messages

✔ Keep messages concise

✔ Never log sensitive information

✔ Use correlation IDs

✔ Prefer structured metadata over free text

---

# Example End-to-End Trace

```text
21:15:00 INFO  Capture   Frame captured               frame_id=4128
21:15:00 INFO  AI        Forest detected              frame_id=4128 confidence=0.93
21:15:01 INFO  Stabilizer Stable scene=Forest         frame_id=4128
21:15:01 INFO  Decision  Pine selected                frame_id=4128
21:15:01 INFO  Device    Command sent                 command_id=98
21:15:01 INFO  Device    ACK received                 command_id=98
```

A single correlation ID allows the complete journey to be reconstructed.

---

# Summary

The Logging module provides visibility into every major component of SceneSense while remaining lightweight and configurable.

```text
Application

↓

Logger

↓

Format

↓

Write

↓

Analyze
```

A well-designed logging strategy is essential for diagnosing problems, measuring performance, and supporting future features such as remote diagnostics, analytics, and telemetry. By standardizing log structure and using correlation IDs across the event pipeline, SceneSense gains a powerful foundation for both development and long-term maintenance.

---

# Appendix A – Recommended Python Libraries

| Purpose | Library |
|----------|---------|
| Core Logging | `logging` (standard library) |
| Structured Logging | `structlog` |
| Rich Console Output | `rich.logging` |
| JSON Formatter | `python-json-logger` |
| Log Rotation | `logging.handlers.RotatingFileHandler` or `TimedRotatingFileHandler` |

For Phase 1, the built-in **`logging`** module combined with **`TimedRotatingFileHandler`** is sufficient. As the project grows, `structlog` can be introduced to provide richer structured logging without requiring major architectural changes.