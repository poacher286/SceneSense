# SceneSense Development Setup

> **Version:** 1.0  
> **Status:** Development Guide  
> **Module:** `development`

---

# Table of Contents

1. Purpose
2. Development Philosophy
3. System Requirements
4. Supported Platforms
5. Required Software
6. Installing Python
7. Installing Git
8. IDE Setup
9. Project Setup
10. Installing Dependencies
11. Running the Application
12. ESP32 Setup
13. Running Tests
14. Troubleshooting
15. Next Steps

---

# Purpose

This guide explains how to set up a complete SceneSense development environment from scratch.

After following this document, a developer should be able to:

- Clone the repository
- Install all dependencies
- Run the application
- Connect an ESP32
- Execute tests
- Begin contributing to the project

This document targets **Python-only development** for Phase 1.

---

# Development Philosophy

SceneSense follows a simple development philosophy:

- Cross-platform
- Python-first
- Local AI inference
- Modular architecture
- Minimal setup friction
- Reproducible development environments

Every developer should be able to set up the project in less than 30 minutes.

---

# Supported Platforms

| Platform | Status |
|----------|--------|
| macOS (Apple Silicon) | ✅ Primary Development Platform |
| macOS (Intel) | ✅ Supported |
| Windows 11 | ✅ Supported |
| Ubuntu 22.04+ | ✅ Supported |
| Other Linux Distributions | ⚠️ Best Effort |

Phase 1 development is primarily performed on **macOS**.

---

# Minimum System Requirements

| Component | Requirement |
|-----------|-------------|
| CPU | Quad-Core |
| RAM | 8 GB |
| Storage | 5 GB Free |
| Python | 3.11+ |
| Git | Latest |
| USB Port | Required for ESP32 |

---

# Recommended System

| Component | Recommendation |
|-----------|----------------|
| CPU | Apple M-Series / Ryzen 7 / Intel i7 |
| RAM | 16 GB |
| Storage | SSD |
| GPU | Optional |
| Display | 1080p or Higher |

---

# Required Software

Install the following tools:

| Software | Purpose |
|----------|---------|
| Python 3.11+ | Main programming language |
| Git | Version control |
| VS Code | Recommended IDE |
| PlatformIO | ESP32 firmware |
| Arduino IDE (Optional) | Firmware debugging |

---

# Python Installation

## macOS

Install using Homebrew:

```bash
brew install python
```

Verify:

```bash
python3 --version
```

Expected:

```text
Python 3.11.x
```

---

## Windows

Download from:

https://python.org

During installation:

✔ Add Python to PATH

---

## Linux

Ubuntu:

```bash
sudo apt update

sudo apt install python3 python3-pip python3-venv
```

---

# Git Installation

macOS:

```bash
brew install git
```

Verify:

```bash
git --version
```

---

# VS Code

Recommended extensions:

- Python
- Pylance
- Ruff
- Black Formatter
- GitLens
- YAML
- Markdown All in One
- Error Lens

Optional:

- Serial Monitor
- PlatformIO IDE

---

# Clone Repository

```bash
git clone https://github.com/<username>/SceneSense.git
```

Enter project:

```bash
cd SceneSense
```

---

# Project Structure

```text
SceneSense/

├── app/

├── firmware/

├── config/

├── docs/

├── tests/

├── scripts/

├── requirements.txt

└── README.md
```

---

# Create Virtual Environment

macOS/Linux:

```bash
python3 -m venv .venv
```

Windows:

```cmd
python -m venv .venv
```

---

# Activate Environment

macOS/Linux:

```bash
source .venv/bin/activate
```

Windows:

```cmd
.venv\Scripts\activate
```

Verify:

```bash
python --version
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

Verify:

```bash
pip list
```

---

# Core Python Packages

Expected packages include:

```
mss

opencv-python

numpy

torch

transformers

pyserial

pyyaml

pytest

loguru
```

---

# Configuration

Copy example configuration:

```bash
cp config/config.example.yaml config/config.yaml
```

Edit as needed:

```yaml
serial:

  port: AUTO

capture:

  fps: 5

ai:

  model: clip
```

---

# Running the Application

Development mode:

```bash
python app/main.py
```

Expected output:

```text
Initializing...

Loading AI...

Connecting ESP32...

Ready.
```

---

# Running Without Hardware

Enable simulation mode:

```yaml
device:

  simulation: true
```

Now:

```bash
python app/main.py
```

No ESP32 is required.

---

# ESP32 Setup

Connect the ESP32 via USB.

Determine serial port.

macOS:

```bash
ls /dev/cu.*
```

Example:

```text
/dev/cu.usbserial-0001
```

Update configuration:

```yaml
serial:

  port: /dev/cu.usbserial-0001
```

---

# Upload Firmware

Using PlatformIO:

```bash
cd firmware

pio run

pio run --target upload
```

---

# Verify Connection

Run:

```bash
python scripts/check_device.py
```

Expected:

```text
Device Connected

Firmware 1.0

Ready
```

---

# Running Tests

Run all tests:

```bash
pytest
```

Specific module:

```bash
pytest tests/ai
```

Coverage:

```bash
pytest --cov=app
```

---

# Linting

Check formatting:

```bash
ruff check .
```

Auto-fix:

```bash
ruff check . --fix
```

---

# Formatting

Format code:

```bash
black app tests
```

---

# Type Checking

Run:

```bash
mypy app
```

Type hints are encouraged throughout the codebase.

---

# Logging

Logs are written to:

```text
logs/
```

Example:

```text
2026-08-01.log
```

Logging levels:

- DEBUG
- INFO
- WARNING
- ERROR

---

# Development Workflow

Typical workflow:

```text
Pull Latest Code

↓

Create Branch

↓

Implement Feature

↓

Run Tests

↓

Lint

↓

Commit

↓

Push

↓

Open Pull Request
```

---

# Debug Mode

Run:

```bash
python app/main.py --debug
```

Debug mode enables:

- Verbose logging
- Performance metrics
- AI confidence output
- Serial communication logs

---

# Common Commands

Install dependencies:

```bash
pip install -r requirements.txt
```

Run application:

```bash
python app/main.py
```

Run tests:

```bash
pytest
```

Format code:

```bash
black .
```

Lint:

```bash
ruff check .
```

---

# Common Issues

## Python Not Found

Verify installation:

```bash
python3 --version
```

---

## Virtual Environment Not Activated

Prompt should display:

```text
(.venv)
```

If not:

```bash
source .venv/bin/activate
```

---

## Missing Packages

Reinstall:

```bash
pip install -r requirements.txt
```

---

## ESP32 Not Found

Verify:

- USB cable supports data
- Correct serial port
- Firmware uploaded

---

## macOS Screen Permission

Grant:

```
System Settings

↓

Privacy & Security

↓

Screen Recording

↓

Enable SceneSense
```

Restart the application afterward.

---

## AI Model Download

First launch may download pretrained models.

Internet connection is required only once.

Subsequent runs use the local cache.

---

# Recommended Folder Usage

| Folder | Purpose |
|---------|---------|
| app | Application source |
| firmware | ESP32 firmware |
| config | Configuration files |
| docs | Documentation |
| tests | Automated tests |
| logs | Runtime logs |
| scripts | Utility scripts |

---

# Development Best Practices

✔ Always use a virtual environment

✔ Keep dependencies updated

✔ Run tests before committing

✔ Format code automatically

✔ Write type hints

✔ Keep modules focused

✔ Test without hardware when possible

✔ Document new features

---

# First Successful Run

A successful startup should resemble:

```text
SceneSense v1.0

Loading Configuration...

Initializing Screen Capture...

Loading CLIP Model...

Starting Event Bus...

Connecting ESP32...

Ready.
```

At this point the application is ready to detect scenes and communicate with the diffuser.

---

# Next Steps

After completing the setup:

1. Read `CODING_GUIDELINES.md`
2. Review the project architecture.
3. Run the sample application.
4. Explore the AI pipeline.
5. Connect an ESP32 (optional).
6. Start working on your first feature.

---

# Summary

The SceneSense development environment is intentionally lightweight and cross-platform.

```text
Install Python

↓

Clone Repository

↓

Create Virtual Environment

↓

Install Dependencies

↓

Configure Project

↓

Run Application

↓

Start Developing
```

By standardizing the development process, every contributor works in a consistent environment, reducing setup issues and making collaboration easier. The combination of Python, virtual environments, automated testing, and clear tooling provides a solid foundation for building the SceneSense platform.

---

# Appendix A – Required Commands

```bash
git clone https://github.com/<username>/SceneSense.git

cd SceneSense

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

python app/main.py
```

---

# Appendix B – Development Checklist

- [ ] Install Python 3.11+
- [ ] Install Git
- [ ] Clone the repository
- [ ] Create and activate a virtual environment
- [ ] Install dependencies
- [ ] Copy `config.example.yaml` to `config.yaml`
- [ ] Run the application
- [ ] Verify AI model loads
- [ ] (Optional) Connect and verify ESP32
- [ ] Run all tests successfully

Completing this checklist confirms that the local development environment is ready for contributing to SceneSense.