# SceneSense Configuration

> **Version:** 1.0  
> **Status:** Phase 1 Design  
> **Module:** `config`

---

# Table of Contents

1. Purpose
2. Design Goals
3. Configuration Architecture
4. Configuration Files
5. Configuration Loading
6. Configuration Validation
7. Runtime Access
8. Environment Variables
9. Hot Reloading
10. Default Values
11. Configuration Reference
12. Error Handling
13. Testing
14. Future Improvements

---

# Purpose

The Configuration module centralizes every configurable aspect of SceneSense.

Rather than hardcoding values throughout the application, all settings should be loaded from configuration files.

This enables:

- Easy customization
- Environment-specific configuration
- Safer deployments
- Future UI settings
- User profiles

Configuration should control behavior—not code.

---

# Design Goals

The configuration system should be:

- Human-readable
- Version controlled
- Easy to modify
- Validated at startup
- Type-safe
- Extensible
- Reloadable (future)

---

# High-Level Architecture

```text
config/

application.yaml

capture.yaml

ai.yaml

decision.yaml

scents.yaml

device.yaml

logging.yaml
```

Each module owns its own configuration file.

---

# Folder Structure

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

```
src/scenesense/config/

config_loader.py

config_manager.py

validators.py

models.py
```

---

# Configuration Loading

Startup sequence:

```text
Application Starts

↓

Read YAML Files

↓

Merge Configuration

↓

Validate

↓

Create Config Objects

↓

Inject Into Modules
```

Modules never read YAML files directly.

---

# Configuration Manager

The `ConfigurationManager` is responsible for:

- Loading files
- Validation
- Caching
- Providing typed access

Example:

```python
config.capture.fps

config.ai.model

config.device.timeout
```

No module should access raw dictionaries.

---

# Configuration Flow

```text
YAML Files

↓

Config Loader

↓

Validation

↓

Configuration Objects

↓

Application Modules
```

---

# File Overview

| File | Purpose |
|--------|----------|
| application.yaml | Global settings |
| capture.yaml | Screen capture |
| ai.yaml | AI model |
| decision.yaml | Business rules |
| scents.yaml | Scene → scent mapping |
| device.yaml | ESP32 communication |
| logging.yaml | Logging configuration |

---

# application.yaml

Contains global application settings.

Example:

```yaml
application:

  name: SceneSense

  version: 1.0.0

  debug: false

  language: en

  theme: dark
```

---

# capture.yaml

Example:

```yaml
capture:

  fps: 5

  monitor: primary

  width: 512

  height: 512

  queue_size: 3
```

---

# ai.yaml

Example:

```yaml
ai:

  model: clip

  image_size: 512

  device: auto

  confidence_threshold: 0.80

  batch_size: 1
```

---

# decision.yaml

Example:

```yaml
decision:

  cooldown_seconds: 15

  ignore_duplicates: true

  default_duration: 2

  default_intensity: 0.35
```

---

# scents.yaml

Example:

```yaml
Forest:

  scent: Pine

  intensity: 0.35

  duration: 2

Rain:

  scent: Petrichor

  intensity: 0.45

  duration: 3

Ocean:

  scent: SeaBreeze

  intensity: 0.30

  duration: 2
```

---

# device.yaml

Example:

```yaml
device:

  auto_connect: true

  baud_rate: 115200

  timeout_ms: 1000

  retries: 3

  heartbeat_seconds: 5
```

---

# logging.yaml

Example:

```yaml
logging:

  level: INFO

  console: true

  file: true

  directory: logs

  rotation: daily
```

---

# Configuration Models

Every configuration should have a strongly typed model.

Example:

```python
@dataclass(frozen=True)
class CaptureConfig:
    fps: int
    width: int
    height: int
```

Avoid using raw dictionaries throughout the codebase.

---

# Validation

Validation occurs immediately after loading.

Checks include:

- Missing files
- Missing required fields
- Invalid types
- Invalid ranges
- Duplicate values
- Unknown keys (optional)

---

## Example Validation

Valid:

```yaml
fps: 5
```

Invalid:

```yaml
fps: -2
```

↓

Validation Error

---

# Default Values

Reasonable defaults should exist.

Example:

```text
Capture FPS

↓

Missing

↓

Default = 5
```

Defaults should be documented.

---

# Runtime Access

Modules receive configuration via dependency injection.

Example:

```python
capture = CaptureService(config.capture)

ai = AIEngine(config.ai)

device = DeviceController(config.device)
```

Avoid global configuration lookups.

---

# Environment Variables

Environment variables override YAML values.

Example:

```
SCENESENSE_DEBUG=true

SCENESENSE_LOG_LEVEL=DEBUG

SCENESENSE_AI_DEVICE=gpu
```

Priority:

```text
Environment Variables

↓

YAML

↓

Default Values
```

---

# Hot Reloading (Future)

Future versions may reload configuration without restarting.

Example:

```
User Saves YAML

↓

Detect Change

↓

Validate

↓

Apply New Settings
```

Not required for Phase 1.

---

# Configuration Versioning

Example:

```yaml
config:

  version: 1
```

Allows migration logic in future releases.

---

# Error Handling

Possible failures:

- Missing file
- Invalid YAML
- Invalid value
- Unsupported option

Recovery:

```text
Log

↓

Use Default

↓

Continue
```

Critical failures should stop startup with a clear message.

---

# Logging

Configuration loading should log:

```
Configuration Loaded

Validation Passed

Using Default Value

Environment Override Applied

Configuration Error
```

---

# Performance

Configuration files are loaded once during startup.

Expected load time:

```
< 100 ms
```

Configuration access should be in-memory after initialization.

---

# Testing

## Unit Tests

- YAML parsing
- Validation
- Default values
- Environment overrides
- Typed models

---

## Integration Tests

- Full application startup
- Invalid configuration
- Missing configuration
- Multiple configuration files

---

# Metrics

Expose:

| Metric | Description |
|---------|-------------|
| Files Loaded | Total configuration files |
| Validation Errors | Configuration issues |
| Defaults Used | Default values applied |
| Environment Overrides | Override count |
| Load Time | Startup configuration duration |

---

# Future Improvements

## User Profiles

Support multiple configuration profiles.

Example:

```
Default

Gaming

Streaming

Developer
```

---

## Configuration UI

Future desktop settings page.

```
Settings

↓

Modify

↓

Save YAML
```

---

## Cloud Sync

Users may synchronize preferences.

---

## Plugin Configuration

Plugins can register additional configuration sections.

---

## Encrypted Secrets

Sensitive values (future cloud integrations) should be encrypted or stored outside YAML.

---

# Best Practices

✔ Keep one concern per file

✔ Use typed configuration objects

✔ Validate everything

✔ Fail fast for critical errors

✔ Use sensible defaults

✔ Keep YAML human-readable

✔ Document every field

---

# Example Startup Sequence

```text
Start Application

↓

Load YAML Files

↓

Merge Values

↓

Apply Environment Variables

↓

Validate

↓

Create Config Objects

↓

Inject Into Modules

↓

Application Ready
```

---

# Summary

The Configuration module provides a centralized, type-safe, and extensible mechanism for managing all SceneSense settings.

```text
YAML

↓

Load

↓

Validate

↓

Typed Objects

↓

Application
```

By isolating configuration from implementation, SceneSense becomes easier to deploy, test, maintain, and customize. This foundation will support future capabilities such as user profiles, configuration UIs, plugin settings, and cloud synchronization while keeping the core application clean and maintainable.

---

# Appendix A – Complete Configuration Example

```yaml
application:
  name: SceneSense
  version: 1.0.0
  debug: false

capture:
  fps: 5
  monitor: primary
  width: 512
  height: 512
  queue_size: 3

ai:
  model: clip
  device: auto
  image_size: 512
  confidence_threshold: 0.80

stabilizer:
  buffer_size: 5
  minimum_votes: 3
  confidence_threshold: 0.80

decision:
  cooldown_seconds: 15
  ignore_duplicates: true

device:
  auto_connect: true
  baud_rate: 115200
  timeout_ms: 1000
  retries: 3
  heartbeat_seconds: 5

logging:
  level: INFO
  console: true
  file: true
```

---

# Appendix B – Recommended Libraries

| Purpose | Library |
|----------|---------|
| YAML Parsing | PyYAML |
| Validation | Pydantic v2 |
| Environment Variables | python-dotenv |
| File Watching (Future) | watchdog |

Using **Pydantic** for configuration models is strongly recommended. It provides automatic validation, type conversion, default values, and excellent error messages, making configuration management both robust and developer-friendly.