# SceneSense Error Recovery

> **Version:** 1.0  
> **Status:** Phase 1 Design  
> **Module:** `core`

---

# Table of Contents

1. Purpose
2. Design Goals
3. Error Recovery Philosophy
4. Error Categories
5. Recovery Strategy
6. Recovery Flow
7. Module-Specific Recovery
8. Retry Policies
9. Circuit Breaker
10. Graceful Degradation
11. Error Reporting
12. Logging
13. Configuration
14. Testing
15. Future Improvements

---

# Purpose

The Error Recovery module defines how SceneSense detects, handles, and recovers from failures.

The objective is simple:

> **Keep the application running whenever it is safe to do so.**

A temporary failure in one module should not crash the entire application.

---

# Design Goals

The recovery system should be:

- Predictable
- Resilient
- Fault tolerant
- Self-healing
- Observable
- Easy to debug

---

# Error Recovery Philosophy

Every error follows the same lifecycle.

```text
Failure

↓

Detect

↓

Log

↓

Recover

↓

Continue

OR

Shutdown
```

Recovery is always preferred over termination when the system can safely continue.

---

# Error Categories

Errors are classified into four levels.

| Level | Description | Action |
|---------|-------------|--------|
| Recoverable | Temporary issue | Retry |
| Degraded | Partial functionality lost | Continue |
| Fatal | Core functionality unavailable | Shutdown |
| Unexpected | Unknown exception | Log and isolate |

---

# Recoverable Errors

Examples:

- Temporary serial timeout
- Frame capture timeout
- AI inference timeout
- USB reconnect
- Queue overflow

Recovery:

```text
Retry

↓

Continue
```

---

# Degraded Errors

Examples:

- Device disconnected
- Low AI confidence
- Unknown scene
- Missing scent mapping

Recovery:

```text
Disable Feature

↓

Continue Running
```

The application remains usable.

---

# Fatal Errors

Examples:

- Configuration missing
- Invalid configuration
- AI model cannot load
- Event Bus initialization failure

Recovery:

```text
Display Error

↓

Shutdown
```

---

# Unexpected Errors

Examples:

- Null reference
- Library bug
- Unhandled exception

Recovery:

```text
Catch

↓

Log

↓

Isolate

↓

Continue
```

The exception should not propagate across module boundaries.

---

# High-Level Recovery Flow

```text
Error

↓

Classify

↓

Recoverable?

↓

Retry

↓

Success?

↓

Continue

↓

Fail?

↓

Escalate
```

---

# Module Recovery

Each module defines its own recovery strategy.

| Module | Recovery |
|---------|----------|
| Capture | Restart capture |
| AI | Skip frame |
| Stabilizer | Clear buffer |
| Decision | Ignore event |
| Device | Reconnect |
| Event Bus | Isolate subscriber |
| Configuration | Use defaults (where possible) |

---

# Screen Capture Recovery

Failure:

```
Capture Failed
```

Recovery:

```text
Wait

↓

Restart Capture

↓

Continue
```

A single failed frame should never stop the pipeline.

---

# AI Recovery

Failure:

```
Inference Timeout
```

Recovery:

```text
Drop Frame

↓

Process Next Frame
```

Real-time processing is more important than processing every frame.

---

# Scene Stabilizer Recovery

Failure:

```
Corrupted Buffer
```

Recovery:

```text
Clear Buffer

↓

Continue
```

The next stable scene will rebuild the buffer.

---

# Decision Engine Recovery

Failure:

```
Unknown Scene
```

Recovery:

```text
Log Warning

↓

Ignore Scene
```

No scent is emitted.

---

# Device Recovery

Failure:

```
Serial Timeout
```

Recovery:

```text
Retry

↓

Reconnect

↓

Continue
```

The Device Controller manages all hardware failures internally.

---

# Event Bus Recovery

Failure:

```
Subscriber Exception
```

Recovery:

```text
Log

↓

Remove Subscriber (optional)

↓

Continue Dispatch
```

One faulty subscriber should not affect others.

---

# Retry Policy

Recommended retry strategy:

| Attempt | Delay |
|----------|-------|
| 1 | Immediate |
| 2 | 500 ms |
| 3 | 1 s |

Maximum retries:

```
3
```

---

# Exponential Backoff (Future)

Future retry delays:

```
1 s

↓

2 s

↓

4 s

↓

8 s
```

Useful for persistent failures.

---

# Circuit Breaker

Repeated failures trigger a temporary shutdown of the failing component.

```text
Failure

↓

Failure

↓

Failure

↓

Open Circuit

↓

Cooldown

↓

Retry
```

This prevents endless retry loops.

---

# Graceful Degradation

When recovery is impossible, disable only the affected feature.

Example:

```
ESP32 Disconnected

↓

Disable Scents

↓

Continue Scene Detection
```

The user interface remains responsive.

---

# Watchdog

Future versions may include a watchdog.

Responsibilities:

- Monitor thread health
- Restart failed workers
- Detect deadlocks

---

# Error Reporting

Each module publishes an error event.

Example:

```python
DeviceErrorEvent(
    code="SERIAL_TIMEOUT",
    message="No response from device",
    timestamp=datetime.now()
)
```

The UI and logger subscribe to these events.

---

# Logging

Every error should include:

- Timestamp
- Module
- Error type
- Message
- Stack trace (if available)
- Correlation ID
- Recovery action

Example:

```text
ERROR

Device

TimeoutError

Retrying (attempt 2 of 3)

command_id=84
```

---

# User Notifications

Errors visible to users should be clear and actionable.

Examples:

```
Device disconnected.
Attempting to reconnect...
```

```
AI model failed to load.
Please verify your installation.
```

Avoid exposing stack traces to end users.

---

# Configuration

Example:

```yaml
recovery:

  retries: 3

  retry_delay_ms: 500

  auto_reconnect: true

  enable_circuit_breaker: true
```

---

# Performance Considerations

Recovery should not introduce noticeable delays.

Guidelines:

- Skip bad frames instead of blocking.
- Limit retries.
- Avoid infinite loops.
- Recover asynchronously where possible.

---

# Testing

## Unit Tests

- Retry logic
- Error classification
- Circuit breaker
- Recovery decisions

---

## Integration Tests

- USB disconnect/reconnect
- AI timeout
- Invalid configuration
- Event Bus failures

---

## Manual Tests

Verify:

- Device unplugged
- Corrupted configuration
- Model missing
- Queue overflow
- Unexpected exceptions

---

# Metrics

Expose recovery metrics:

| Metric | Description |
|---------|-------------|
| Total Errors | Number of detected errors |
| Recoveries | Successful recoveries |
| Retries | Retry attempts |
| Failed Recoveries | Recovery failures |
| Reconnect Count | Device reconnects |
| Circuit Breaker Activations | Open circuit events |

These metrics help monitor application health.

---

# Future Improvements

## Automatic Diagnostics

Generate diagnostic reports after repeated failures.

---

## Crash Reports

Automatically save:

- Stack traces
- Logs
- Configuration
- Environment information

---

## Recovery Dashboard

Provide a UI showing:

- Active errors
- Recovery attempts
- Device status
- AI status

---

## Cloud Reporting (Optional)

Opt-in upload of anonymized crash reports for debugging future releases.

---

## Self-Healing Modules

Future modules may restart themselves without restarting the application.

---

# Best Practices

✔ Catch exceptions at module boundaries

✔ Retry only recoverable failures

✔ Fail fast on invalid configuration

✔ Never retry indefinitely

✔ Keep recovery actions deterministic

✔ Isolate module failures

✔ Log both the error and the recovery action

✔ Continue operating whenever safely possible

---

# Example Recovery Flow

```text
Device Timeout

↓

Log Error

↓

Retry

↓

ACK Received

↓

Resume Normal Operation
```

If retries fail:

```text
Device Timeout

↓

Retry x3

↓

Reconnect

↓

Success

↓

Continue
```

If reconnection also fails:

```text
Disable Device

↓

Publish DeviceDisconnectedEvent

↓

Continue Scene Detection
```

---

# Summary

The Error Recovery module ensures SceneSense remains resilient in the face of temporary failures and unexpected conditions.

```text
Detect

↓

Classify

↓

Recover

↓

Verify

↓

Continue
```

By isolating failures, applying consistent recovery strategies, and favoring graceful degradation over application crashes, SceneSense can provide a stable and responsive user experience even when hardware, AI models, or external dependencies encounter problems. This resilience is essential for a real-time immersive system that must continue operating smoothly over long gaming sessions.

---

# Appendix A – Recovery Matrix

| Failure | Detection | Recovery | Continue? |
|----------|-----------|----------|-----------|
| Frame Capture Timeout | Capture Module | Skip frame | ✅ |
| AI Inference Timeout | AI Module | Drop frame | ✅ |
| Low Confidence | AI Module | Ignore prediction | ✅ |
| Unknown Scene | Decision Engine | Ignore event | ✅ |
| Serial Timeout | Device Controller | Retry / Reconnect | ✅ |
| USB Disconnected | Device Controller | Auto reconnect | ✅ |
| Queue Overflow | Event Bus | Drop oldest low-priority event | ✅ |
| Invalid Configuration | Config Loader | Abort startup | ❌ |
| AI Model Missing | AI Engine | Abort startup | ❌ |
| Unhandled Exception | Module Boundary | Log & isolate | Usually ✅ |

---

# Appendix B – Error Handling Principles

1. **Recover locally whenever possible.**
2. **Never allow one module to crash another.**
3. **Keep recovery deterministic and bounded.**
4. **Separate user-facing messages from technical logs.**
5. **Treat configuration errors as startup failures, not runtime failures.**
6. **Prefer graceful degradation over complete shutdown.**
7. **Publish error events so other modules can react without tight coupling.**