# SceneSense Testing Strategy

> **Version:** 1.0  
> **Status:** Phase 1 Design  
> **Module:** `testing`

---

# Table of Contents

1. Purpose
2. Testing Philosophy
3. Testing Pyramid
4. Test Levels
5. Test Environment
6. Unit Testing
7. Integration Testing
8. End-to-End Testing
9. Performance Testing
10. Hardware Testing
11. Manual Testing
12. Regression Testing
13. Test Data
14. CI/CD Integration
15. Future Improvements

---

# Purpose

Testing ensures that every component of SceneSense works correctly, independently, and together.

Since SceneSense is a **real-time event-driven system**, testing must validate:

- Correctness
- Performance
- Reliability
- Hardware communication
- AI accuracy
- Recovery from failures

The goal is to detect defects early and maintain confidence as the project evolves.

---

# Testing Philosophy

SceneSense follows four principles:

- Test every module independently.
- Test interactions between modules.
- Automate repetitive tests.
- Keep hardware-independent tests separate from hardware-dependent tests.

Every new feature should include corresponding automated tests.

---

# Testing Pyramid

```text
                 End-to-End
              ───────────────
             Integration Tests
          ──────────────────────
              Unit Tests
```

Approximate distribution:

| Test Type | Target Coverage |
|------------|-----------------|
| Unit Tests | 70% |
| Integration Tests | 20% |
| End-to-End Tests | 10% |

Unit tests should form the majority of the test suite.

---

# Project Test Structure

```
tests/

unit/

integration/

e2e/

performance/

hardware/

fixtures/

test_data/

conftest.py
```

---

# Testing Environment

Recommended setup:

| Component | Tool |
|-----------|------|
| Framework | pytest |
| Mocking | unittest.mock |
| Coverage | pytest-cov |
| Benchmarking | pytest-benchmark |
| Linting | ruff |
| Static Typing | mypy |

---

# Unit Testing

Each module should be tested in complete isolation.

Modules:

```
Capture

AI

Stabilizer

Decision

Mapping

Event Bus

Device

Configuration
```

Dependencies should be mocked.

---

## Example Unit Test

```python
def test_duplicate_scene_is_ignored():
    engine = DecisionEngine(...)

    result = engine.process("Forest")
    result = engine.process("Forest")

    assert result is None
```

---

# Integration Testing

Integration tests verify communication between modules.

Examples:

```
Capture

↓

AI
```

```
AI

↓

Stabilizer
```

```
Decision

↓

Device
```

These tests use real implementations whenever practical.

---

# End-to-End Testing

An end-to-end test validates the complete application pipeline.

```text
Screen

↓

Capture

↓

AI

↓

Stabilizer

↓

Decision

↓

Mapping

↓

Device

↓

ESP32
```

The objective is to verify that a visual scene results in the expected scent command.

---

# Performance Testing

Performance tests measure latency and throughput.

Metrics:

- Capture FPS
- AI inference time
- Decision latency
- Event queue latency
- Serial response time
- End-to-end latency

Example targets:

| Metric | Target |
|----------|--------|
| Capture | 5 FPS |
| AI Inference | < 200 ms |
| Decision Engine | < 1 ms |
| Event Dispatch | < 5 ms |
| Device Response | < 100 ms |
| End-to-End | < 500 ms |

---

# Hardware Testing

Hardware tests require an ESP32 and diffuser prototype.

Verify:

- Device discovery
- Handshake
- Serial communication
- ACK responses
- Retry behavior
- Automatic reconnect

These tests should be excluded from normal CI runs.

---

# AI Testing

The AI Engine should be tested with a curated image dataset.

Example scenes:

```
Forest

Ocean

Rain

Snow

Fire

Desert

City
```

Each image should have an expected label.

Measure:

- Accuracy
- Confidence
- Inference time

---

# Scene Stabilizer Testing

Test scenarios:

```
Forest
Forest
Forest
Forest
Forest
```

↓

Stable Forest

---

```
Forest
Ocean
Forest
Ocean
Forest
```

↓

No Stable Scene

---

```
Rain
Rain
Rain
Forest
Rain
```

↓

Stable Rain

---

# Decision Engine Testing

Verify:

- Duplicate suppression
- Cooldown enforcement
- Transition detection
- Unknown scene handling
- Event generation

Example:

```
Forest

↓

Forest
```

Expected:

```
No scent request
```

---

# Event Bus Testing

Verify:

- Event publication
- Multiple subscribers
- Subscriber isolation
- Queue ordering
- Thread safety

---

# Device Controller Testing

Test:

- Successful connection
- Timeout
- Retry
- Disconnect
- Reconnect
- Invalid response

Mock serial communication whenever possible.

---

# Configuration Testing

Verify:

- Missing files
- Invalid YAML
- Invalid values
- Environment overrides
- Default values

Startup should fail only for unrecoverable configuration errors.

---

# Error Recovery Testing

Inject failures into every module.

Examples:

```
Serial Timeout

↓

Reconnect
```

```
Capture Failure

↓

Restart Capture
```

```
Unknown Scene

↓

Ignore
```

Recovery behavior should be deterministic.

---

# Manual Testing

Manual verification checklist:

| Test | Expected Result |
|--------|-----------------|
| Start application | Launch successfully |
| Connect ESP32 | Device detected |
| Disconnect ESP32 | Auto reconnect |
| Display forest image | Pine command sent |
| Display ocean image | Sea Breeze command sent |
| Invalid configuration | Startup error |
| Unknown scene | No scent |

---

# Regression Testing

Every bug should result in a new automated test.

Regression tests prevent previously fixed issues from returning.

---

# Test Data

Store reusable assets under:

```
tests/

test_data/

forest.jpg

ocean.jpg

rain.jpg

snow.jpg
```

Expected outputs should be documented.

---

# Mock Objects

Use mocks for:

- Screen capture
- AI inference
- Serial port
- Event bus
- Time functions

Mocking keeps unit tests fast and deterministic.

---

# Continuous Integration

CI pipeline:

```text
Checkout

↓

Install Dependencies

↓

Lint

↓

Static Analysis

↓

Unit Tests

↓

Integration Tests

↓

Coverage

↓

Build
```

Hardware tests should run separately.

---

# Coverage Goals

Recommended targets:

| Module | Coverage |
|----------|----------|
| Decision | 95% |
| Mapping | 95% |
| Event Bus | 90% |
| Configuration | 90% |
| Device Controller | 85% |
| AI | 75% |
| Capture | 80% |

Overall project target:

```
90%
```

---

# Metrics

Track:

| Metric | Description |
|---------|-------------|
| Tests Passed | Total successful tests |
| Tests Failed | Total failures |
| Code Coverage | Percentage covered |
| Test Duration | Total execution time |
| Performance Benchmarks | Latency metrics |

---

# Future Improvements

## Automated Hardware Lab

A dedicated hardware setup for unattended ESP32 testing.

---

## Visual Regression Testing

Compare AI predictions against expected outputs for known images.

---

## Stress Testing

Run the application continuously for extended periods (e.g., 24–72 hours) to detect memory leaks or stability issues.

---

## Load Testing

Simulate:

- High frame rates
- Frequent scene transitions
- Rapid scent requests

Verify system stability under load.

---

## Chaos Testing

Introduce random failures:

- Disconnect USB
- Kill AI worker
- Corrupt configuration
- Delay events

Ensure graceful recovery.

---

## User Acceptance Testing

Invite users to evaluate:

- Scent timing
- Accuracy
- Comfort
- Overall immersion

Collect qualitative feedback.

---

# Best Practices

✔ Keep unit tests isolated

✔ Avoid external dependencies

✔ Mock hardware

✔ Use deterministic inputs

✔ Test failure scenarios

✔ Measure performance

✔ Automate whenever possible

✔ Add regression tests for every bug

---

# Example End-to-End Test

```text
Load Forest Image

↓

Capture Frame

↓

AI Predicts Forest

↓

Stabilizer Accepts

↓

Decision Engine Selects Pine

↓

Scent Mapping Resolves Pine

↓

Device Controller Sends Command

↓

Mock ESP32 Returns ACK

↓

Test Passes
```

---

# Summary

Testing is a core part of SceneSense's architecture, not an afterthought.

```text
Unit

↓

Integration

↓

End-to-End

↓

Hardware

↓

Release
```

By combining comprehensive automated tests with targeted hardware validation, SceneSense can evolve confidently while maintaining reliability, performance, and a high-quality immersive experience. A disciplined testing strategy will enable rapid iteration as new AI models, scent profiles, and hardware capabilities are introduced.

---

# Appendix A – Recommended Python Testing Libraries

| Purpose | Library |
|----------|---------|
| Test Framework | `pytest` |
| Mocking | `unittest.mock` |
| Coverage | `pytest-cov` |
| Benchmarking | `pytest-benchmark` |
| Async Testing | `pytest-asyncio` |
| Property-Based Testing | `hypothesis` |

---

# Appendix B – Test Execution Commands

```bash
# Run all tests
pytest

# Run unit tests only
pytest tests/unit

# Run integration tests
pytest tests/integration

# Run end-to-end tests
pytest tests/e2e

# Run performance benchmarks
pytest tests/performance

# Generate coverage report
pytest --cov=src --cov-report=html

# Open HTML coverage report
open htmlcov/index.html
```

These commands provide a consistent workflow for local development and CI/CD pipelines.