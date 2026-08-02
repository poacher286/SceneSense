# SceneSense Project Structure

> **Version:** 1.0  
> **Status:** Active  
> **Audience:** Developers

---

# Table of Contents

1. Purpose
2. Design Principles
3. Repository Overview
4. Directory Structure
5. Source Code Organization
6. Documentation Structure
7. Tests
8. Configuration
9. Assets
10. AI Models
11. Scripts
12. Firmware
13. Build & Distribution
14. Future Expansion

---

# Purpose

This document describes the directory structure of the SceneSense repository.

The primary goals are:

- Clean organization
- Clear separation of responsibilities
- Easy onboarding for contributors
- Long-term maintainability
- Scalability for future hardware and AI models

The structure is designed to support both the current MVP and future phases without major reorganization.

---

# Design Principles

The repository follows these principles:

- Feature modules are isolated.
- Documentation lives alongside development.
- Configuration is externalized.
- AI models are separated from application logic.
- Tests mirror the source tree.
- Hardware firmware is version-controlled with the application.

---

# Repository Overview

```
SceneSense/
│
├── src/
├── docs/
├── tests/
├── config/
├── models/
├── assets/
├── firmware/
├── scripts/
├── logs/
├── data/
├── .github/
├── requirements.txt
├── pyproject.toml
├── README.md
├── LICENSE
└── .gitignore
```

---

# Complete Directory Structure

```text
SceneSense/
│
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── .env.example
│
├── src/
│   └── scenesense/
│       │
│       ├── __init__.py
│       ├── main.py
│       │
│       ├── core/
│       │   ├── application.py
│       │   ├── bootstrap.py
│       │   ├── lifecycle.py
│       │   └── dependency_container.py
│       │
│       ├── capture/
│       │   ├── screen_capture.py
│       │   ├── window_manager.py
│       │   └── frame_provider.py
│       │
│       ├── ai/
│       │   ├── pipeline/
│       │   ├── inference/
│       │   ├── labels/
│       │   └── models.py
│       │
│       ├── stabilizer/
│       │   ├── prediction_buffer.py
│       │   └── scene_stabilizer.py
│       │
│       ├── decision/
│       │   ├── decision_engine.py
│       │   ├── scent_mapper.py
│       │   ├── cooldown_manager.py
│       │   └── rules.py
│       │
│       ├── events/
│       │   ├── event_bus.py
│       │   ├── event_types.py
│       │   ├── publisher.py
│       │   └── subscriber.py
│       │
│       ├── device/
│       │   ├── serial_controller.py
│       │   ├── protocol.py
│       │   ├── device_manager.py
│       │   └── esp32_client.py
│       │
│       ├── ui/
│       │   ├── dashboard.py
│       │   ├── widgets.py
│       │   └── theme.py
│       │
│       ├── config/
│       │   ├── config_loader.py
│       │   ├── settings.py
│       │   └── validator.py
│       │
│       ├── common/
│       │   ├── logger.py
│       │   ├── constants.py
│       │   ├── helpers.py
│       │   └── exceptions.py
│       │
│       └── domain/
│           ├── scene.py
│           ├── scent.py
│           ├── events.py
│           └── prediction.py
│
├── docs/
│   ├── vision/
│   ├── architecture/
│   ├── hardware/
│   ├── ai/
│   ├── api/
│   ├── development/
│   └── user-guide/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── performance/
│   ├── fixtures/
│   └── test_data/
│
├── config/
│   ├── application.yaml
│   ├── scents.yaml
│   ├── logging.yaml
│   └── models.yaml
│
├── models/
│   ├── clip/
│   ├── siglip/
│   ├── florence/
│   └── cache/
│
├── assets/
│   ├── icons/
│   ├── screenshots/
│   ├── diagrams/
│   └── scents/
│
├── firmware/
│   └── esp32/
│       ├── src/
│       ├── include/
│       ├── platformio.ini
│       └── README.md
│
├── scripts/
│   ├── setup.sh
│   ├── run.sh
│   ├── lint.sh
│   ├── format.sh
│   └── build.sh
│
├── logs/
│
├── data/
│   ├── recordings/
│   ├── traces/
│   └── cache/
│
└── .github/
    ├── workflows/
    ├── ISSUE_TEMPLATE/
    └── PULL_REQUEST_TEMPLATE.md
```

---

# Source Code Organization

The `src/scenesense` directory contains all application logic.

| Module | Responsibility |
|---------|----------------|
| `core` | Application startup, dependency injection, lifecycle |
| `capture` | Screen capture and window management |
| `ai` | AI inference and preprocessing pipeline |
| `stabilizer` | Smooth AI predictions |
| `decision` | Rules, cooldowns, scent selection |
| `events` | Event Bus and event definitions |
| `device` | ESP32 and hardware communication |
| `ui` | Desktop dashboard |
| `config` | Configuration loading and validation |
| `common` | Shared utilities |
| `domain` | Business models (Scene, Events, Predictions) |

Each module should have a single responsibility and minimal dependencies on other modules.

---

# Documentation Structure

```
docs/

vision/
    PRODUCT_VISION.md
    ROADMAP.md
    GOALS.md
    NON_GOALS.md

architecture/
    SOFTWARE_ARCHITECTURE.md
    MODULES.md
    DATA_FLOW.md
    EVENT_BUS.md

ai/
    AI_PIPELINE.md
    SCENE_MODEL.md

development/
    PROJECT_STRUCTURE.md
    CODING_GUIDELINES.md
    CONTRIBUTING.md
    TESTING.md

hardware/
    DEVICE_PROTOCOL.md
    ESP32.md
    SCENT_CARTRIDGES.md

user-guide/
    INSTALLATION.md
    QUICK_START.md
    FAQ.md
```

Every architectural decision should be documented before implementation.

---

# Tests

The test structure mirrors the source tree.

```
tests/

unit/
    capture/
    ai/
    decision/
    device/
    events/

integration/
    pipeline/
    hardware/

performance/
    ai/
    capture/

fixtures/
    images/
    configs/

test_data/
```

This organization makes it easy to locate tests corresponding to a specific module.

---

# Configuration

All configuration files live in the top-level `config/` directory.

Examples:

- `application.yaml` — global application settings
- `scents.yaml` — scene-to-scent mappings
- `logging.yaml` — logging configuration
- `models.yaml` — AI model settings

No configuration should be hardcoded into the source code.

---

# Assets

The `assets/` directory stores non-code resources.

Examples:

- Application icons
- UI screenshots
- Architecture diagrams
- Reference scent images

These assets should never contain executable logic.

---

# AI Models

The `models/` directory contains downloaded AI model files and caches.

Example:

```
models/
├── clip/
├── siglip/
├── florence/
└── cache/
```

Models are intentionally separated from source code to simplify updates and reduce repository size.

---

# Firmware

The `firmware/` directory contains the ESP32 code.

```
firmware/
└── esp32/
    ├── src/
    ├── include/
    ├── platformio.ini
    └── README.md
```

Keeping firmware in the same repository ensures application and device protocols evolve together.

---

# Scripts

Utility scripts automate common development tasks.

Examples:

| Script | Purpose |
|---------|---------|
| `setup.sh` | Install dependencies |
| `run.sh` | Launch the application |
| `lint.sh` | Run linting tools |
| `format.sh` | Apply code formatting |
| `build.sh` | Package the application |

Scripts should be platform-aware where possible.

---

# Logs

The `logs/` directory stores runtime log files.

Example:

```
logs/

application.log

device.log

ai.log
```

Logs should be excluded from version control.

---

# Data

The `data/` directory stores temporary runtime data.

Examples:

- Cached AI outputs
- Session traces
- Performance recordings

This directory should be safe to delete between runs.

---

# Build & Distribution

Python packaging is managed through:

- `pyproject.toml`
- `requirements.txt`

Future packaging options may include:

- PyInstaller
- Briefcase
- Nuitka

These tools can generate standalone executables for Windows, macOS, and Linux.

---

# Future Expansion

The structure is designed to accommodate additional capabilities without reorganization.

Possible future directories:

```
plugins/
lighting/
haptics/
audio/
cloud/
telemetry/
web/
mobile/
```

Because modules communicate through the Event Bus, new features can be added with minimal impact on existing code.

---

# Design Rules

Every new file should follow these guidelines:

- Place it in the module that owns the responsibility.
- Avoid cross-module imports when events or interfaces suffice.
- Keep modules cohesive and loosely coupled.
- Mirror the source tree in the test tree.
- Document architectural changes before implementation.

---

# Summary

The SceneSense repository is organized to support long-term growth while keeping the MVP approachable.

```
Repository

↓

Modules

↓

Events

↓

Features
```

A clear project structure makes the codebase easier to navigate, simplifies onboarding, encourages consistent development practices, and provides a solid foundation as SceneSense evolves from a prototype into a full immersive platform.