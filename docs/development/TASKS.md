# SceneSense Development Tasks

> **Version:** 1.0  
> **Status:** Living Document  
> **Module:** `development`

---

# Table of Contents

1. Purpose
2. Task Management Philosophy
3. Project Status
4. Milestones
5. Phase 1 Tasks
6. Phase 2 Tasks
7. Phase 3 Tasks
8. Phase 4 Tasks
9. Technical Debt
10. Nice-to-Have Features
11. Future Ideas
12. Completed Tasks
13. Development Workflow

---

# Purpose

This document serves as the master engineering task list for SceneSense.

It tracks:

- Current work
- Upcoming features
- Long-term roadmap
- Technical debt
- Research items
- Stretch goals

Unlike the roadmap, this document focuses on actionable engineering tasks.

---

# Task Status

| Status | Meaning |
|---------|----------|
| 🔴 Not Started | Work has not begun |
| 🟡 In Progress | Currently being developed |
| 🟢 Complete | Finished |
| ⚪ Future | Planned for a later phase |
| ⚠️ Blocked | Waiting on another task |

---

# Priority Levels

| Priority | Meaning |
|----------|----------|
| P0 | Critical |
| P1 | High |
| P2 | Medium |
| P3 | Low |

---

# Current Project Status

```text
Project Name

SceneSense

Current Phase

Phase 1

Overall Progress

Planning & Documentation

Software

Not Started

Hardware

Prototype Design

AI

Research Complete

Documentation

In Progress
```

---

# Project Milestones

| Milestone | Target |
|-----------|--------|
| Documentation Complete | ✅ |
| Initial Application Skeleton | 🔴 |
| Screen Capture Working | 🔴 |
| AI Scene Recognition | 🔴 |
| ESP32 Communication | 🔴 |
| First Working Diffuser | ⚪ |
| Public Alpha | ⚪ |
| Open Source Release | ⚪ |

---

# Phase 1 — Foundation

## Goal

Build a desktop application capable of understanding the screen and triggering scents through an ESP32.

---

# 1. Repository Setup

Priority:

```
P0
```

Status:

```
🔴
```

Tasks:

- Create repository
- Configure Git
- Create folder structure
- Configure Python environment
- Configure linting
- Configure formatting
- Configure testing
- Configure CI (future)

---

# 2. Configuration System

Priority:

P0

Status:

🔴

Tasks:

- YAML configuration
- Configuration loader
- Validation
- Default configuration
- Environment overrides

---

# 3. Logging Framework

Priority:

P0

Status:

🔴

Tasks:

- Console logger
- File logger
- Debug mode
- Performance logging

---

# 4. Screen Capture

Priority:

P0

Status:

🔴

Tasks:

- MSS integration
- Monitor selection
- Capture loop
- Resize pipeline
- FPS limiter
- Frame queue
- Performance metrics

Deliverable:

```
Capture frames at 5 FPS.
```

---

# 5. AI Engine

Priority:

P0

Status:

🔴

Tasks:

- Load CLIP
- Tokenize labels
- Image preprocessing
- Scene classification
- Confidence scoring

Deliverable:

```
Recognize environments.
```

---

# 6. Scene Stabilizer

Priority:

P0

Status:

🔴

Tasks:

- Sliding window
- Majority voting
- Confidence filtering
- Cooldown timer

Deliverable:

Stable scene transitions.

---

# 7. Decision Engine

Priority:

P0

Status:

🔴

Tasks:

- Rule engine
- Duplicate prevention
- Trigger generation
- Cooldown support

Deliverable:

Generate scent events.

---

# 8. Event Bus

Priority:

P1

Status:

🔴

Tasks:

- Event queue
- Publish/subscribe
- Thread safety
- Logging

---

# 9. Device Controller

Priority:

P1

Status:

🔴

Tasks:

- Serial connection
- Command encoding
- Retry logic
- ACK handling

---

# 10. ESP32 Firmware

Priority:

P1

Status:

🔴

Tasks:

- Serial parser
- Fan control
- Cartridge activation
- Timer management
- Status reporting

---

# 11. Configuration UI (Minimal)

Priority:

P2

Status:

⚪

Tasks:

- Select serial port
- Select monitor
- FPS settings
- Enable simulation mode

---

# 12. Testing

Priority:

P1

Status:

🔴

Tasks:

- Unit tests
- Integration tests
- Hardware simulation
- Performance tests

---

# Phase 1 Success Criteria

- Screen captured successfully
- AI recognizes environments
- Stable scene detection
- ESP32 receives commands
- Diffuser activates correctly
- End-to-end latency <500 ms

---

# Phase 2 — Smarter Recognition

## Goal

Improve immersion and system intelligence.

Tasks:

- Native screen capture APIs
- GPU inference
- Dynamic capture FPS
- Weather detection
- Time-of-day detection
- Better confidence models
- Scene blending
- Scent intensity scaling
- User profiles
- Custom scent mappings

---

# Phase 3 — Gameplay Awareness

## Goal

Recognize gameplay events in addition to environments.

Tasks:

- Explosion detection
- Fire detection
- Vehicle detection
- Ocean detection
- Weapon detection
- Snow detection
- Rain detection
- Character state recognition
- Motion analysis
- Event prediction

---

# Phase 4 — Hardware Evolution

## Goal

Develop production-ready hardware.

Tasks:

- Custom PCB
- Multiple diffuser heads
- Silent fan system
- Wireless communication
- Replaceable cartridges
- Battery-powered unit
- Automatic calibration
- LED status indicators

---

# Phase 5 — Console & TV Support

## Goal

Support gaming beyond PCs.

Tasks:

- HDMI capture integration
- PlayStation compatibility
- Xbox compatibility
- Nintendo Switch compatibility
- Smart TV compatibility
- Streaming device support

---

# Technical Debt

Known future improvements:

- Improve dependency injection
- Replace polling with events
- Optimize image preprocessing
- Reduce memory allocations
- Improve configuration validation
- Better exception hierarchy
- Native platform APIs
- GPU acceleration

---

# Research Tasks

- Evaluate Florence-2
- Evaluate SigLIP
- Compare CLIP variants
- Benchmark ONNX Runtime
- Test OpenVINO
- Evaluate Metal acceleration
- Investigate scent blending algorithms

---

# Nice-to-Have Features

- Dark mode UI
- Live diagnostics dashboard
- FPS graph
- AI confidence visualization
- Device firmware updater
- Auto-update mechanism
- Plugin system
- REST API
- Web dashboard

---

# Stretch Goals

- Voice control
- VR headset support
- Haptic integration
- Ambient lighting integration
- Smart home automation
- Multi-room scent systems
- Adaptive AI personalization

---

# Documentation Tasks

Remaining documentation work:

- Architecture diagrams
- Sequence diagrams
- UML diagrams
- API reference
- Firmware reference
- Plugin development guide
- User manual
- Hardware assembly guide

---

# Release Checklist

Before Phase 1 release:

- [ ] Application launches
- [ ] Screen capture functional
- [ ] AI model loads
- [ ] Scene recognition working
- [ ] ESP32 communication verified
- [ ] Diffuser prototype operational
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] Documentation complete

---

# Completed Tasks

## Vision

🟢 Product vision defined

🟢 Goals documented

🟢 Non-goals documented

🟢 Roadmap created

---

## Architecture

🟢 Software architecture documented

🟢 Module architecture documented

🟢 AI pipeline documented

🟢 Event bus documented

🟢 Decision engine documented

---

## Implementation

🟢 Phase 1 design documented

🟢 Screen capture design

🟢 AI engine design

🟢 Serial protocol

🟢 Testing strategy

🟢 Deployment strategy

---

## Hardware

🟢 ESP32 design

🟢 Diffuser design

🟢 Cartridge design

🟢 Hardware protocol

---

## Research

🟢 AI model research

🟢 Screen capture research

🟢 Latency analysis

🟢 Performance research

🟢 Technology references

---

# Development Workflow

```text
Choose Task

↓

Create Branch

↓

Implement

↓

Run Tests

↓

Code Review

↓

Merge

↓

Update Documentation

↓

Close Task
```

---

# Best Practices

✔ Work on one feature at a time

✔ Keep pull requests small

✔ Update documentation alongside code

✔ Write tests before marking tasks complete

✔ Measure performance after major changes

✔ Refactor when necessary, not prematurely

✔ Keep technical debt visible

---

# Summary

The SceneSense task list transforms the long-term vision into manageable engineering work.

```text
Vision

↓

Roadmap

↓

Milestones

↓

Tasks

↓

Implementation

↓

Testing

↓

Release
```

By organizing work into clearly defined phases with priorities, success criteria, and measurable deliverables, SceneSense can evolve from a documented concept into a robust, production-ready platform for immersive scent-enhanced gaming.

---

# Appendix A – Phase Overview

| Phase | Focus | Status |
|--------|-------|--------|
| Phase 1 | Desktop MVP | 🔴 Planning |
| Phase 2 | Smarter AI | ⚪ Planned |
| Phase 3 | Gameplay Events | ⚪ Planned |
| Phase 4 | Production Hardware | ⚪ Planned |
| Phase 5 | Console & TV Support | ⚪ Planned |

---

# Appendix B – MVP Definition

The Phase 1 MVP is considered complete when all of the following are true:

- Screen capture runs continuously
- Semantic AI correctly identifies major environments
- Scene stabilization prevents rapid scent switching
- Decision engine emits correct scent events
- ESP32 reliably receives commands
- Diffuser activates the correct cartridge
- Average end-to-end latency remains below 500 ms
- Documentation and automated tests are complete

This milestone establishes the technical foundation upon which all future SceneSense features and hardware generations will be built.