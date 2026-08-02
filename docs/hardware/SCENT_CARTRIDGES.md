# SceneSense Scent Cartridges

> **Version:** 1.0  
> **Status:** Phase 1 Design  
> **Module:** `hardware`

---

# Table of Contents

1. Purpose
2. Vision
3. Design Goals
4. Cartridge Philosophy
5. Cartridge Architecture
6. Cartridge Types
7. Scent Categories
8. Standard Cartridge Specification
9. Scent Mapping
10. Cartridge Management
11. Safety
12. Storage
13. Maintenance
14. Testing
15. Future Improvements

---

# Purpose

The scent cartridge system is the heart of the SceneSense hardware platform.

Each cartridge stores a single scent and allows the diffuser to release it on demand. By keeping scents isolated in individual cartridges, SceneSense can accurately recreate game environments while avoiding unwanted scent mixing.

The cartridge system is designed to be modular, replaceable, and scalable.

---

# Vision

The long-term vision is to create a **library of reusable scent cartridges** that can be combined to simulate a wide variety of game worlds.

Instead of creating game-specific cartridges, SceneSense focuses on **universal environmental scents**.

For example:

| Environment | Scent |
|-------------|-------|
| Forest | Pine |
| Ocean | Sea Breeze |
| Rain | Petrichor |
| Desert | Dry Sand |
| Snow | Cold Air |
| Campfire | Wood Smoke |
| Flower Field | Floral |

A small collection of cartridges should be capable of representing hundreds of different games.

---

# Design Goals

The cartridge system should be:

- Modular
- Replaceable
- Leak-resistant
- Long-lasting
- Easy to identify
- Safe
- Expandable
- Cost-effective

---

# Cartridge Philosophy

Every cartridge contains **one scent only**.

Advantages:

- Simple mapping
- Easy replacement
- Minimal contamination
- Predictable behavior
- Independent lifespan

Complex environments are created by combining multiple cartridges over time (future phases), not by mixing scents inside a cartridge.

---

# High-Level Architecture

```text
Desktop App

↓

Scene

↓

Decision Engine

↓

Scent Mapping

↓

ESP32

↓

Selected Cartridge

↓

Diffuser

↓

Player
```

---

# Cartridge Components

Each cartridge contains:

```text
Outer Shell

↓

Absorbent Core

↓

Fragrance Oil

↓

Air Channel

↓

Seal

↓

Connector
```

---

# Cartridge Workflow

```text
Idle

↓

Valve Opens

↓

Air Flows Through Cartridge

↓

Fragrance Picked Up

↓

Air Exits

↓

Valve Closes
```

No fragrance should escape while the valve is closed.

---

# Cartridge Capacity

Suggested prototype capacity:

```
10–20 mL
```

This is sufficient for thousands of short diffusion events.

Future consumer versions may offer multiple capacities.

---

# Cartridge Materials

Recommended materials:

| Component | Material |
|-----------|----------|
| Housing | ABS / PETG |
| Internal Wick | Cotton / Cellulose |
| Seal | Silicone |
| Connector | Food-grade Plastic |

Materials should resist degradation from fragrance oils.

---

# Cartridge Types

Phase 1 supports only **single-scent cartridges**.

Future types may include:

- High-capacity cartridges
- Blend cartridges
- Smart cartridges
- Disposable cartridges
- Refillable cartridges

---

# Core Environmental Collection

Recommended starter set:

| Cartridge | Purpose |
|-----------|---------|
| Pine | Forest |
| Petrichor | Rain |
| Sea Breeze | Ocean |
| Wood Smoke | Fire / Camp |
| Floral | Gardens |
| Fresh Grass | Fields |
| Cold Air | Snow / Mountains |
| Neutral | Air Purge |

These eight cartridges cover a large percentage of outdoor environments.

---

# Event-Based Collection

Future event scents:

| Event | Scent |
|-------|-------|
| Explosion | Burnt Powder |
| Gunfire | Mild Gunpowder |
| Fireplace | Burning Wood |
| Bakery | Fresh Bread |
| Coffee Shop | Coffee |
| Camp | Campfire |
| Jungle | Wet Vegetation |
| Library | Old Books |

These scents are triggered by gameplay events rather than scene recognition.

---

# Emotional / Ambient Collection

Optional future cartridges:

- Vanilla
- Lavender
- Citrus
- Mint
- Fresh Linen
- Leather
- Cedar
- Sandalwood

These could enhance menus, story sequences, or relaxation games.

---

# Cartridge Identification

Phase 1:

- Printed labels
- Color coding

Example:

| Color | Cartridge |
|--------|-----------|
| Green | Pine |
| Blue | Ocean |
| Brown | Smoke |
| Yellow | Desert |

Future versions may support RFID or NFC identification.

---

# Standard Cartridge Specification

Example dimensions:

| Property | Value |
|----------|-------|
| Diameter | 25 mm |
| Height | 60 mm |
| Capacity | 15 mL |
| Weight | < 40 g |

Keeping a standard form factor simplifies future hardware upgrades.

---

# Cartridge Rack

Example layout:

```text
+-------------------------------+
| Pine   Rain   Ocean   Smoke   |
| Floral Grass Cold   Neutral   |
+-------------------------------+
```

The rack should allow tool-free replacement.

---

# Scent Mapping

Software maps scenes to cartridges.

Example:

```text
Forest

↓

Pine Cartridge
```

```text
Rain

↓

Petrichor Cartridge
```

The firmware activates the appropriate valve.

---

# Intensity

Intensity is controlled by airflow, not cartridge concentration.

Example:

| Level | Fan Speed |
|--------|-----------|
| Low | 25% |
| Medium | 50% |
| High | 75% |
| Maximum | 100% |

All cartridges contain fragrance at a consistent concentration.

---

# Cartridge Lifespan

Expected prototype lifespan:

```
2,000–5,000 activations
```

Actual lifespan depends on:

- Diffusion duration
- Airflow
- Fragrance type
- Ambient temperature

---

# Replacement

Replace cartridges when:

- Fragrance weakens
- Oil is depleted
- Expiration date is reached
- Contamination occurs

Replacement should take less than one minute.

---

# Storage

Store cartridges:

- Upright
- Sealed
- Away from sunlight
- At room temperature
- Away from children and pets

Proper storage extends fragrance life.

---

# Shelf Life

Expected shelf life:

```
12–24 months
```

Unopened cartridges generally last longer than opened ones.

---

# Cross-Contamination Prevention

To reduce scent mixing:

- Dedicated valve per cartridge
- Tight seals
- Air purge after activation
- One active cartridge at a time (Phase 1)

Future versions may include automated cleaning cycles.

---

# Safety

Cartridges should:

- Be leak-resistant
- Use non-toxic fragrance oils
- Prevent accidental opening
- Resist heat
- Include clear labeling

Only fragrances intended for air diffusion should be used.

---

# Maintenance

Routine checks:

- Inspect seals
- Clean cartridge ports
- Check airflow
- Replace worn cartridges

Do not refill damaged cartridges.

---

# Testing

## Functional Tests

Verify:

- Correct cartridge activation
- No leakage
- Correct airflow
- Easy insertion/removal

---

## Durability Tests

Measure:

- Seal wear
- Housing strength
- Connector reliability
- Repeated insertion cycles

Target:

```
1,000+

Insertion cycles
```

---

## Diffusion Tests

Measure:

- Scent consistency
- Airflow
- Residual scent
- Activation repeatability

---

# Future Improvements

## Smart Cartridges

RFID/NFC tags can store:

- Cartridge ID
- Scent name
- Remaining capacity
- Expiration date
- Batch number

The diffuser automatically detects installed cartridges.

---

## Capacity Monitoring

Future sensors may estimate remaining fragrance based on:

- Activation count
- Airflow
- Weight
- Optical sensing

---

## Automatic Purge

After each activation:

```text
Close Valve

↓

Fresh Air

↓

Clear Air Path
```

This reduces scent carryover.

---

## Scent Blending

Future versions may activate multiple cartridges simultaneously.

Example:

```text
70% Pine

30% Petrichor
```

To recreate a rainy forest.

---

## Marketplace

Long-term vision:

Users can purchase themed cartridge packs.

Examples:

- Fantasy Pack
- Space Pack
- Survival Pack
- Horror Pack
- Tropical Pack
- Winter Pack

This creates an expandable ecosystem around SceneSense.

---

# Best Practices

✔ Use one scent per cartridge

✔ Label cartridges clearly

✔ Keep cartridges sealed

✔ Replace before fully depleted

✔ Avoid cross-contamination

✔ Store correctly

✔ Design for easy replacement

✔ Use standardized dimensions

---

# Example Activation Flow

```text
Scene = Forest

↓

Decision Engine

↓

Pine Selected

↓

ESP32

↓

Open Pine Valve

↓

Fan Starts

↓

Air Passes Through Pine Cartridge

↓

Player Smells Pine

↓

Valve Closes
```

---

# Summary

The scent cartridge system provides the physical scent library that powers SceneSense.

```text
Scene

↓

Scent Selection

↓

Cartridge

↓

Airflow

↓

Immersion
```

By isolating scents into standardized, replaceable cartridges, the system remains modular, maintainable, and highly scalable. As SceneSense evolves, the cartridge ecosystem can expand from a handful of environmental scents to a rich collection of themed fragrance packs, smart cartridges, and dynamic scent blending capabilities.

---

# Appendix A – Recommended Phase 1 Starter Pack

| Cartridge | Primary Use |
|-----------|-------------|
| Pine | Forests, jungles |
| Petrichor | Rain, storms |
| Sea Breeze | Beaches, oceans |
| Wood Smoke | Campfires, explosions |
| Fresh Grass | Meadows, sports fields |
| Floral | Gardens, fantasy worlds |
| Cold Air | Snow, mountains |
| Neutral Air | Purge / reset airflow |

This set provides broad coverage for many genres while keeping hardware complexity manageable.

---

# Appendix B – Roadmap

| Phase | Features |
|--------|----------|
| **Phase 1** | Single-scent cartridges, manual replacement |
| **Phase 2** | Automatic purge, improved rack design |
| **Phase 3** | Multi-scent blending, smart cartridge detection |
| **Phase 4** | Capacity monitoring, consumer cartridge marketplace |

Following this roadmap allows SceneSense to validate the core cartridge concept early while building toward a sophisticated and extensible scent delivery ecosystem.