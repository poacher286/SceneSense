# SceneSense Deployment

> **Version:** 1.0  
> **Status:** Phase 1 Design  
> **Module:** `deployment`

---

# Table of Contents

1. Purpose
2. Deployment Goals
3. Supported Platforms
4. System Requirements
5. Deployment Architecture
6. Installation Flow
7. Project Build
8. Application Packaging
9. Python Environment
10. Configuration
11. Device Setup
12. Verification
13. Updating
14. Distribution
15. Future Improvements

---

# Purpose

This document describes how SceneSense is built, packaged, installed, and deployed.

The goal of deployment is to make installation as simple as possible while ensuring consistent behavior across supported operating systems.

Phase 1 focuses on desktop deployment for development and early testing.

---

# Deployment Goals

The deployment process should be:

- Simple
- Repeatable
- Versioned
- Cross-platform
- Reliable
- Easy to update

A new user should be able to install and run SceneSense in just a few steps.

---

# Supported Platforms

Phase 1 officially supports:

| Platform | Status |
|----------|--------|
| macOS (Apple Silicon) | ✅ Supported |
| macOS (Intel) | ✅ Supported |
| Windows 11 | ✅ Planned |
| Ubuntu 22.04+ | ✅ Planned |

Development is performed primarily on macOS.

---

# System Requirements

Minimum requirements:

| Component | Requirement |
|-----------|-------------|
| Python | 3.11+ |
| RAM | 8 GB |
| CPU | 4 Cores |
| Disk Space | 2 GB |
| USB | USB 2.0+ |
| Internet | Required only for initial model download |

Recommended:

| Component | Requirement |
|-----------|-------------|
| RAM | 16 GB |
| CPU | Apple M-Series / Intel i7 / Ryzen 7 |
| GPU | Optional (for faster inference) |

---

# Deployment Architecture

```text
+-----------------------------+
|      SceneSense Desktop     |
+-----------------------------+
             │
             ▼
+-----------------------------+
|   Configuration Files       |
+-----------------------------+
             │
             ▼
+-----------------------------+
|      AI Model Files         |
+-----------------------------+
             │
             ▼
+-----------------------------+
|     USB Serial Driver       |
+-----------------------------+
             │
             ▼
+-----------------------------+
|           ESP32             |
+-----------------------------+
             │
             ▼
+-----------------------------+
|      Scent Diffuser         |
+-----------------------------+
```

---

# Installation Flow

```text
Clone Repository

↓

Create Virtual Environment

↓

Install Dependencies

↓

Download AI Model

↓

Connect ESP32

↓

Run SceneSense
```

---

# Repository Layout

```
SceneSense/

src/

config/

docs/

tests/

scripts/

requirements.txt

README.md
```

The deployment package includes source code, configuration, and documentation.

---

# Python Environment

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

Upgrade pip:

```bash
pip install --upgrade pip
```

---

# Installing Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

Recommended core dependencies:

- PySide6
- OpenCV
- Pillow
- mss
- pyserial
- transformers
- torch
- pyyaml
- pydantic
- structlog
- psutil

---

# AI Model Download

The first launch downloads the selected AI model automatically if it is not already cached.

Example cache location:

```text
~/.cache/huggingface/
```

The application should verify the model before starting inference.

---

# Configuration

Default configuration files are located in:

```
config/

application.yaml

capture.yaml

ai.yaml

decision.yaml

scents.yaml

device.yaml

logging.yaml
```

Users may modify these files without rebuilding the application.

---

# Device Setup

1. Connect the ESP32 using USB.
2. Ensure the device firmware is installed.
3. Launch SceneSense.
4. The Device Controller scans available ports.
5. A successful handshake places the device in the **Ready** state.

Connection sequence:

```text
USB Connected

↓

Port Detected

↓

HELLO

↓

WELCOME

↓

READY
```

---

# Running the Application

Development mode:

```bash
python -m src.scenesense.main
```

or

```bash
python src/scenesense/main.py
```

The application starts with configuration validation before initializing modules.

---

# Verification Checklist

Before use, verify:

- ✅ Configuration loaded
- ✅ AI model initialized
- ✅ Screen capture active
- ✅ Event Bus running
- ✅ ESP32 connected
- ✅ Device status = READY

A startup summary should be displayed in the console.

---

# Packaging

For end users, package SceneSense into a standalone executable.

Recommended tool:

**PyInstaller**

Example:

```bash
pyinstaller \
  --name SceneSense \
  --windowed \
  --onedir \
  src/scenesense/main.py
```

Generated output:

```
dist/

SceneSense.app      (macOS)

SceneSense.exe      (Windows)
```

---

# Build Artifacts

Recommended output:

```
dist/

SceneSense/

config/

models/

logs/

README.md
```

Keep configuration separate from application binaries.

---

# Logging Directory

Logs are stored in:

```
logs/

application.log

ai.log

device.log

errors.log
```

The deployment process should create this directory automatically if it does not exist.

---

# Updating

Application updates follow this process:

```text
Download New Release

↓

Replace Executable

↓

Preserve Configuration

↓

Preserve Logs

↓

Launch
```

User configuration should not be overwritten.

---

# Backup Strategy

Preserve:

- Configuration files
- User scent mappings
- Logs
- Profiles (future)

Avoid storing generated data inside the source directory.

---

# Distribution

Possible distribution methods:

| Method | Phase |
|----------|-------|
| GitHub Repository | Phase 1 |
| GitHub Releases | Phase 2 |
| Homebrew (macOS) | Future |
| Windows Installer (MSI) | Future |
| Linux AppImage | Future |

---

# CI/CD Build Pipeline

```text
Commit

↓

GitHub Actions

↓

Run Tests

↓

Static Analysis

↓

Build Package

↓

Create Release Artifact
```

Future releases can be automatically attached to GitHub Releases.

---

# Security Considerations

- Validate configuration before startup.
- Verify AI model integrity.
- Never execute untrusted configuration.
- Restrict serial communication to recognized devices.
- Sign release binaries when distributing publicly.

---

# Troubleshooting

## Application Does Not Start

Check:

- Python version
- Missing dependencies
- Invalid configuration
- Corrupted AI model

---

## ESP32 Not Detected

Verify:

- USB cable
- Correct firmware
- Serial permissions
- Device drivers (Windows)

---

## AI Model Not Loading

Verify:

- Internet connection (first download)
- Cache directory
- Disk space

---

## High CPU Usage

Reduce:

- Capture FPS
- Capture resolution
- Logging level

---

# Deployment Testing

Before every release, verify:

- Fresh installation
- Upgrade installation
- Configuration migration
- Device detection
- AI initialization
- Packaging
- Startup on supported operating systems

---

# Future Improvements

## Automatic Updater

Check for new versions automatically.

---

## Installer Wizard

Provide a graphical installer that:

- Installs dependencies
- Downloads AI models
- Detects ESP32
- Creates desktop shortcuts

---

## Docker Development Environment

Provide a containerized environment for contributors.

---

## Portable Mode

Support running SceneSense directly from a USB drive without installation.

---

## Plugin Distribution

Future plugins may be installed independently from the core application.

---

# Best Practices

✔ Use virtual environments

✔ Keep configuration external

✔ Version releases

✔ Preserve user data

✔ Package dependencies

✔ Test on clean systems

✔ Automate builds

✔ Document installation steps

---

# Example Deployment Flow

```text
Clone Repository

↓

Create Virtual Environment

↓

Install Dependencies

↓

Download AI Model

↓

Connect ESP32

↓

Launch SceneSense

↓

Handshake Successful

↓

Ready
```

---

# Summary

The deployment process for SceneSense is designed to be simple, repeatable, and cross-platform.

```text
Build

↓

Package

↓

Install

↓

Configure

↓

Run
```

By separating configuration, application binaries, AI models, and hardware communication, SceneSense remains easy to install, maintain, and upgrade. As the project evolves, the deployment process can expand to include automated installers, update mechanisms, and platform-specific distribution channels without changing the core application architecture.

---

# Appendix A – Recommended Build Tools

| Purpose | Tool |
|----------|------|
| Dependency Management | `pip` |
| Virtual Environments | `venv` |
| Packaging | `PyInstaller` |
| Build Automation | `Make` or `Invoke` |
| CI/CD | GitHub Actions |
| Versioning | Git Tags + Semantic Versioning |

---

# Appendix B – Release Checklist

Before publishing a release:

- [ ] All unit tests pass
- [ ] Integration tests pass
- [ ] End-to-end tests pass
- [ ] Hardware communication verified
- [ ] AI model loads correctly
- [ ] Configuration validated
- [ ] Packaging completed
- [ ] Documentation updated
- [ ] Version number incremented
- [ ] Git tag created
- [ ] Release artifact generated
- [ ] Release notes prepared

Following this checklist helps ensure that every SceneSense release is reliable, reproducible, and ready for users.