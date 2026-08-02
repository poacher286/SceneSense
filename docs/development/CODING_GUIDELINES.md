# SceneSense Coding Guidelines

> **Version:** 1.0  
> **Status:** Development Guide  
> **Module:** `development`

---

# Table of Contents

1. Purpose
2. Guiding Principles
3. Project Structure
4. Python Standards
5. Naming Conventions
6. Code Organization
7. Type Hints
8. Documentation
9. Logging
10. Error Handling
11. Configuration
12. Thread Safety
13. Performance
14. Testing
15. Git Standards
16. Code Review Checklist
17. Best Practices

---

# Purpose

This document defines the coding standards used throughout the SceneSense project.

The goals are to:

- Keep the codebase consistent
- Improve readability
- Reduce bugs
- Simplify reviews
- Enable long-term maintenance
- Make onboarding easier for new contributors

Every contribution should follow these guidelines unless there is a compelling technical reason not to.

---

# Guiding Principles

SceneSense code should be:

- Simple
- Readable
- Predictable
- Modular
- Testable
- Performant
- Platform-independent

Prefer code that is easy to understand over clever or highly optimized implementations.

---

# General Philosophy

Write code for the next developer.

Ask yourself:

> "Can someone understand this six months from now without asking me?"

If the answer is no, simplify the implementation.

---

# Python Version

Supported version:

```
Python 3.11+
```

Avoid using deprecated language features.

---

# Style Guide

SceneSense follows:

- **PEP 8** for formatting
- **PEP 257** for docstrings
- **PEP 484** for type hints

Formatting is enforced automatically using **Black**.

Linting is performed using **Ruff**.

---

# File Organization

Each file should have a single responsibility.

Example:

```text
capture.py

Handles screen capture only.
```

Avoid files that combine unrelated functionality.

---

# Package Structure

```text
app/

capture/

ai/

decision/

events/

device/

config/

utils/
```

Each package should expose a clear public interface.

---

# Module Size

Recommended:

- 200–400 lines per file

Maximum:

```
500 Lines
```

Large modules should be split into smaller components.

---

# Naming Conventions

## Files

Use:

```text
snake_case.py
```

Example:

```
scene_detector.py

event_bus.py

device_controller.py
```

---

## Classes

Use:

```python
SceneDetector
```

PascalCase for all classes.

---

## Functions

Use:

```python
detect_scene()
```

snake_case.

Function names should describe actions.

---

## Variables

Use descriptive names.

Good:

```python
current_scene
capture_interval
fan_speed
```

Avoid:

```python
a
x
tmp
foo
```

Except for very small local scopes.

---

## Constants

Use:

```python
MAX_QUEUE_SIZE = 2
DEFAULT_FPS = 5
```

UPPER_SNAKE_CASE.

---

# Imports

Preferred order:

```python
# Standard Library

import time

import threading

# Third-party

import cv2

import numpy as np

# Project

from app.ai import SceneDetector
```

Avoid wildcard imports.

Never use:

```python
from module import *
```

---

# Type Hints

Every public function should include type hints.

Example:

```python
def detect_scene(frame: np.ndarray) -> str:
    ...
```

Benefits:

- Better IDE support
- Easier refactoring
- Fewer runtime mistakes

---

# Docstrings

Public classes and functions should include docstrings.

Example:

```python
def capture_frame() -> np.ndarray:
    """
    Capture a single frame from the active display.

    Returns:
        RGB image as a NumPy array.
    """
```

Keep documentation concise and accurate.

---

# Function Design

Functions should:

- Perform one task
- Be easy to test
- Avoid hidden side effects

Aim for:

```
<40 lines
```

If a function becomes difficult to understand, split it.

---

# Class Design

Classes should represent a single responsibility.

Example:

Good:

```text
SceneDetector

ScreenCapture

DeviceController
```

Avoid "God Objects" that manage unrelated responsibilities.

---

# Configuration

Never hard-code configuration values.

Instead:

```yaml
capture:

  fps: 5
```

Read values through the configuration system.

---

# Magic Numbers

Avoid:

```python
sleep(0.173)
```

Instead:

```python
FRAME_INTERVAL = 0.2
```

Named constants improve readability.

---

# Logging

Use structured logging.

Recommended levels:

```text
DEBUG

INFO

WARNING

ERROR

CRITICAL
```

Example:

```python
logger.info("Scene changed to '%s'", scene)
```

Avoid using `print()` for application logic.

---

# Error Handling

Handle expected failures gracefully.

Good:

```python
try:
    connect_device()
except SerialException:
    logger.error("Unable to connect to ESP32")
```

Avoid broad exception handling:

```python
except Exception:
    pass
```

Never silently ignore errors.

---

# Exceptions

Raise meaningful exceptions.

Example:

```python
raise InvalidSceneError(scene_name)
```

Custom exception types are preferred for domain-specific failures.

---

# Thread Safety

Shared state must be protected.

Use:

- `queue.Queue`
- `threading.Lock`
- Immutable data where possible

Avoid unsynchronized global variables.

---

# Global Variables

Minimize global state.

Prefer dependency injection and explicit object ownership.

---

# Performance Guidelines

Avoid:

- Repeated allocations
- Busy waiting
- Blocking the main thread
- Unnecessary image copies

Reuse buffers where practical.

---

# AI Module Guidelines

The AI layer should:

- Load models once
- Keep inference stateless
- Return structured results
- Remain independent of hardware

AI modules should not communicate directly with the ESP32.

---

# Screen Capture Guidelines

Capture modules should:

- Produce raw frames
- Avoid AI logic
- Avoid business rules
- Focus only on image acquisition

---

# Decision Engine Guidelines

The decision engine should:

- Be deterministic
- Avoid hardware dependencies
- Be fully testable
- Contain no UI code

---

# Device Controller Guidelines

Responsible for:

- Protocol encoding
- Serial communication
- Retries
- Acknowledgement handling

It should not make gameplay decisions.

---

# Event Bus Guidelines

Events should be:

- Immutable
- Timestamped
- Lightweight

Avoid placing large image buffers inside events.

---

# Dependency Rules

Preferred dependency direction:

```text
Capture

↓

AI

↓

Decision

↓

Device
```

Lower layers must never depend on higher layers.

Example:

The capture module should never import the decision engine.

---

# Testing Requirements

Every new feature should include:

- Unit tests
- Integration tests (where applicable)

Bug fixes should include regression tests whenever possible.

---

# Comments

Write comments that explain **why**, not **what**.

Poor:

```python
# Increment index
i += 1
```

Better:

```python
# Skip duplicate frames to reduce latency.
```

---

# Code Duplication

Avoid copy-paste implementations.

Extract shared logic into reusable utilities.

---

# Security

Never:

- Commit API keys
- Commit passwords
- Commit personal data

Use environment variables or configuration files excluded from version control.

---

# Git Commit Messages

Recommended format:

```text
feat: add scene stabilizer

fix: handle serial timeout

docs: update AI research

test: add decision engine tests

refactor: simplify capture pipeline
```

---

# Pull Requests

Before opening a pull request:

- Run tests
- Run formatter
- Run linter
- Update documentation
- Review your own changes

---

# Code Review Checklist

Reviewers should verify:

- Readability
- Correctness
- Test coverage
- Performance impact
- Thread safety
- Logging
- Error handling
- Documentation

---

# Anti-Patterns

Avoid:

- Large classes
- Circular imports
- Hidden side effects
- Hard-coded values
- Duplicate logic
- Deep nesting
- Excessive inheritance

Favor composition over inheritance.

---

# Example Project Flow

```text
Capture

↓

AI

↓

Decision

↓

Event Bus

↓

Device Controller

↓

ESP32
```

Each layer has a clearly defined responsibility.

---

# Best Practices

✔ Keep functions short

✔ Prefer composition

✔ Write meaningful names

✔ Use type hints

✔ Document public APIs

✔ Keep modules independent

✔ Avoid premature optimization

✔ Test everything

✔ Log important events

✔ Keep code deterministic

---

# Summary

The SceneSense codebase is designed to remain clean, modular, and maintainable as it grows.

```text
Readable

↓

Modular

↓

Testable

↓

Reliable

↓

Maintainable
```

By following consistent naming conventions, enforcing clear module boundaries, using type hints, writing meaningful tests, and documenting public interfaces, contributors can build features with confidence while preserving the long-term health of the project.

---

# Appendix A – Development Toolchain

| Tool | Purpose |
|------|---------|
| Python 3.11+ | Programming language |
| Black | Code formatting |
| Ruff | Linting |
| MyPy | Static type checking |
| PyTest | Testing |
| Git | Version control |
| VS Code | Recommended IDE |

---

# Appendix B – Quick Checklist

Before committing code:

- [ ] Code follows PEP 8
- [ ] Formatted with Black
- [ ] Passes Ruff checks
- [ ] Includes type hints
- [ ] Public APIs documented
- [ ] Tests added or updated
- [ ] No hard-coded configuration
- [ ] No unnecessary logging
- [ ] No debug code left behind
- [ ] Documentation updated if behavior changed

Following these guidelines ensures that SceneSense remains approachable for new contributors, resilient as the codebase grows, and maintainable over the long term.