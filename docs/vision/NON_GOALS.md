# SceneSense Non-Goals

> **Version:** 1.0  
> **Status:** Active  
> **Scope:** Phase 1 (Proof of Concept)

---

# Table of Contents

1. Purpose
2. Why Define Non-Goals?
3. Phase 1 Boundaries
4. Product Non-Goals
5. Technical Non-Goals
6. AI Non-Goals
7. Hardware Non-Goals
8. User Experience Non-Goals
9. Platform Non-Goals
10. Future Features (Not Now)
11. Decision Framework
12. Summary

---

# Purpose

This document defines what **SceneSense is intentionally NOT trying to solve** during Phase 1.

Every successful software project is defined not only by what it builds, but also by what it deliberately chooses **not** to build.

The purpose of this document is to prevent scope creep, reduce unnecessary complexity, and keep development focused on validating the core idea.

---

# Why Define Non-Goals?

When building a new product, it is easy to become distracted by exciting ideas.

Examples:

- Console support
- Smart home integration
- Voice assistants
- RGB synchronization
- Cloud AI
- Mobile apps

While these ideas are valuable, implementing them too early would delay validation of the core concept.

For Phase 1, simplicity wins.

---

# Phase 1 Boundaries

The only question Phase 1 must answer is:

> **Can SceneSense understand a game scene and trigger the correct scent?**

Everything else is secondary.

If a feature does not help answer this question, it should be postponed.

---

# Product Non-Goals

The following are **not** goals for Phase 1.

---

## It is NOT a Commercial Product

Phase 1 is a prototype.

It is acceptable if:

- the UI is basic
- setup requires technical knowledge
- installation is manual
- configuration is developer-oriented

The objective is proof of concept—not polish.

---

## It is NOT a Finished Desktop Application

The desktop interface only exists to help developers observe the system.

It is **not** intended to be production-ready.

A simple dashboard showing:

- Current scene
- Confidence
- Device status
- Current scent

is sufficient.

---

## It is NOT a Gaming Launcher

SceneSense will not:

- Launch games
- Manage game libraries
- Detect installed games
- Replace Steam, Epic, or GOG

It simply observes whatever is currently displayed on the screen.

---

## It is NOT a Streaming Tool

SceneSense will not:

- Record gameplay
- Stream gameplay
- Capture videos
- Save screenshots

Frames exist only in memory.

---

# Technical Non-Goals

---

## No Cloud Processing

All inference happens locally.

Phase 1 will not include:

- Cloud AI
- Remote APIs
- Online inference
- External processing services

Reasons:

- Lower latency
- Better privacy
- Offline support

---

## No Distributed Architecture

SceneSense runs as a single desktop application.

No:

- microservices
- containers
- Kubernetes
- distributed messaging

Those concepts add complexity without helping validate the idea.

---

## No Plugin System

Although the architecture should be modular, Phase 1 will not implement:

- Plugins
- Extension APIs
- Third-party modules

These belong in later releases.

---

## No Automatic Updates

Phase 1 will not include:

- Auto-update mechanisms
- Version synchronization
- Installer frameworks

---

# AI Non-Goals

---

## Not Object Detection

SceneSense is **not** trying to identify every object on the screen.

Instead of:

```
Tree
Rock
Grass
Bush
```

It should simply understand:

```
Forest
```

Semantic understanding is more valuable than object recognition.

---

## Not Perfect Accuracy

The AI does not need 100% accuracy.

It only needs to be reliable enough to create convincing scent transitions.

Occasional mistakes are acceptable during the prototype phase.

---

## Not Every Environment

Phase 1 intentionally supports only a small number of scenes.

Suggested scenes:

- Forest
- Rain
- Ocean
- Snow
- Fire

Additional environments will be added later.

---

## No Emotion Recognition

The AI will not attempt to determine:

- player emotions
- character emotions
- story progression
- narrative context

These are outside the scope of the MVP.

---

# Hardware Non-Goals

---

## No Custom Hardware Design

Initially, SceneSense should use:

- ESP32
- USB Serial
- Simple diffuser prototype

No custom PCB is required.

---

## No Wireless Communication

Phase 1 will use:

```
USB Serial
```

Only.

Bluetooth and Wi-Fi introduce unnecessary complexity.

---

## No Multi-Device Synchronization

Only one hardware device is required.

Future versions may support:

- multiple diffusers
- lighting
- fans
- haptics

Not now.

---

## No Cartridge Management

The application will not:

- detect cartridge levels
- estimate remaining scent
- monitor usage
- automate replacement

These features belong to future hardware revisions.

---

# User Experience Non-Goals

---

## No User Accounts

SceneSense will not require:

- login
- registration
- cloud profiles
- subscriptions

Everything runs locally.

---

## No Telemetry

The application will not collect:

- gameplay statistics
- usage analytics
- user behavior
- crash reporting (unless explicitly enabled)

Privacy is a design principle.

---

## No Mobile Companion App

There will be:

- no Android app
- no iPhone app
- no remote dashboard

Desktop only.

---

# Platform Non-Goals

---

## No Console Support

PlayStation

Xbox

Nintendo Switch

support is intentionally postponed.

Future versions may use HDMI capture devices, but this is outside Phase 1.

---

## No macOS/Linux Optimization

The initial implementation should prioritize functionality.

Platform-specific optimizations can be addressed later.

Cross-platform compatibility is desirable but not required for the prototype.

---

## No VR Integration

Virtual reality introduces unique challenges.

Support for VR should only be explored after the desktop version is stable.

---

# Future Features (Not Now)

The following ideas are intentionally postponed.

---

## Smart Lighting

Philips Hue

Nanoleaf

RGB strips

---

## Smart Fans

Wind simulation

Temperature effects

---

## Haptic Devices

Vests

Controllers

Wearables

---

## Fog Machines

Environmental immersion

---

## HDMI Input

Support external video sources.

---

## Movies

Automatic scent generation for films.

---

## Streaming Services

Netflix

YouTube

Disney+

---

## Accessibility Features

Scene narration

Environmental notifications

Audio assistance

---

## SDK

Game developers integrating SceneSense directly.

---

## Plugin Marketplace

Community-created integrations.

---

# Decision Framework

When evaluating a new feature, ask the following questions.

### Does it help prove the core idea?

If **No**, postpone it.

---

### Does it improve scene understanding?

If **No**, postpone it.

---

### Does it increase implementation complexity?

If **Yes**, ask whether that complexity is necessary for Phase 1.

---

### Can it wait until after the MVP?

If **Yes**, it probably should.

---

# Summary

SceneSense is **not** trying to become everything at once.

Phase 1 has a single objective:

```
Observe

↓

Understand

↓

Trigger
```

Everything else can wait.

The most valuable outcome of Phase 1 is not a polished application—it is confidence that the core concept works.

By deliberately limiting the scope, SceneSense can evolve from a focused prototype into a robust platform with a solid architectural foundation.

---

# Phase 1 Checklist

The MVP is complete when all of the following are true:

- ✅ Screen capture works
- ✅ AI recognizes scenes
- ✅ Scene transitions are stable
- ✅ Correct scent mapping occurs
- ✅ ESP32 receives commands
- ✅ Diffuser activates successfully

If all six items are complete, Phase 1 is successful.

Anything beyond that belongs to the next phase.