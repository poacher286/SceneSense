# ADR-0003: Semantic Scene Recognition

> **Status:** Accepted  
> **Date:** 2026-08-02  
> **Decision Makers:** SceneSense Project  
> **Module:** Architecture Decision Records (ADR)

---

# Table of Contents

1. Status
2. Context
3. Problem Statement
4. Decision
5. Why Semantic Scene Recognition
6. Alternatives Considered
7. Trade-offs
8. Consequences
9. Future Evolution
10. Summary

---

# Status

**Accepted**

SceneSense will recognize **semantic scenes** from the visible screen using computer vision and AI models.

The system will **not** depend on:

- Game APIs
- Game plugins
- Memory reading
- Engine integrations
- Reverse engineering
- OCR as the primary recognition method

The screen itself is treated as the single source of truth.

---

# Context

The goal of SceneSense is to trigger scents that match what the player is experiencing.

Examples:

| Visible Scene | Scent |
|--------------|-------|
| Forest | Pine |
| Beach | Ocean |
| Campfire | Smoke |
| Snow | Fresh Air |
| Rain | Wet Earth |
| Desert | Dry Sand |

The challenge is determining **what the player is currently seeing** in a way that works across thousands of games and media sources.

Several technical approaches were evaluated before selecting semantic scene recognition.

---

# Problem Statement

The recognition system must satisfy several requirements:

- Work with almost any game
- Require no game-specific integration
- Preserve user privacy
- Operate offline
- Respond in near real time
- Be maintainable
- Scale to future platforms such as consoles and TVs

Traditional game integrations cannot meet all of these goals simultaneously.

---

# Decision

SceneSense will use **semantic scene recognition**.

The application periodically captures the screen, passes the image to an AI vision model, and determines the dominant environment or context.

Example pipeline:

```text
Screen

↓

Image

↓

AI Model

↓

Semantic Meaning

↓

Decision Engine

↓

Scent Event
```

The AI determines **what the scene represents**, not which game is running.

---

# What Is Semantic Scene Recognition?

Semantic scene recognition answers questions such as:

- Is this a forest?
- Is this a beach?
- Is the player indoors?
- Is this a snowy mountain?
- Is this a cave?
- Is this a city street?

Rather than detecting specific objects, the model understands the overall environment.

Example:

A forest scene may contain:

- Trees
- Grass
- Shadows
- Sunlight
- Rocks
- Fog

The model recognizes these elements collectively as:

```
Forest
```

This high-level understanding is what drives scent selection.

---

# Why This Approach?

The visible screen already contains the information needed for the user experience.

Whether the game is:

- Unreal Engine
- Unity
- RE Engine
- Source Engine
- Godot
- Custom engine

...the player ultimately sees rendered pixels.

By understanding those pixels, SceneSense remains independent of the underlying technology.

---

# Universal Compatibility

Because the system analyzes rendered output, it can work with:

- PC games
- Emulators
- Videos
- Movies
- Live streams
- Future HDMI capture devices
- Console gameplay

No game-specific implementation is required.

---

# Privacy

Only the current frame is processed.

Captured frames:

- Remain in memory
- Are analyzed locally
- Are discarded immediately after inference

No gameplay images are uploaded or stored by default.

---

# AI Model Selection

Phase 1 uses a vision-language model capable of associating images with natural language descriptions.

Desired characteristics:

- General-purpose scene understanding
- Zero-shot classification
- Offline inference
- Cross-platform support

This avoids collecting and maintaining a custom training dataset.

---

# Scene Categories

The initial semantic vocabulary focuses on broad environmental contexts.

Examples include:

- Forest
- Beach
- Ocean
- Desert
- Snow
- Rain
- Mountain
- Cave
- City
- Village
- Castle
- Space
- Underwater
- Jungle
- Swamp
- Campfire
- Night
- Indoor
- Outdoor

The vocabulary can expand over time without changing the architecture.

---

# Decision Flow

```text
Capture Frame

↓

Preprocess Image

↓

Run AI Inference

↓

Rank Candidate Scenes

↓

Select Highest Confidence

↓

Stabilize

↓

Generate Event
```

---

# Why Not OCR?

OCR was evaluated as a possible solution.

Advantages:

- Simple implementation
- Detects visible text

Disadvantages:

- Most gameplay contains little or no useful text.
- Text does not reliably describe the environment.
- HUD elements vary significantly between games.
- Localization introduces language dependencies.

Example:

```
Quest Updated
```

This provides no useful scent information.

Decision:

**Rejected.**

---

# Why Not Game Plugins?

Game-specific plugins can access internal game state.

Advantages:

- Accurate event data
- Rich context

Disadvantages:

- Requires a plugin for every game.
- Difficult to maintain.
- Breaks after game updates.
- Impossible for many closed platforms.
- Incompatible with movies and streams.

Decision:

**Rejected.**

---

# Why Not Memory Reading?

Reading process memory can reveal game state.

Advantages:

- Detailed information

Disadvantages:

- Platform-specific
- Fragile
- May violate game policies
- Difficult to maintain
- Impossible on consoles
- Potential anti-cheat concerns

Decision:

**Rejected.**

---

# Why Not Image Templates?

Template matching compares images against predefined references.

Advantages:

- Simple for fixed interfaces

Disadvantages:

- Does not generalize
- Sensitive to resolution changes
- Breaks with visual updates
- Requires extensive maintenance

Decision:

**Rejected.**

---

# Why Not Object Detection Alone?

Object detection identifies individual objects.

Example:

- Tree
- Rock
- Car
- Dog

While useful, it does not always convey the overall environment.

Example:

A tree may appear in:

- Forest
- City park
- Village
- Backyard

The scent should depend on the overall scene rather than a single object.

Decision:

Object detection may complement semantic recognition in future phases but is not sufficient on its own.

---

# Benefits

## Game Independence

No knowledge of the game engine is required.

---

## Future Console Support

The same approach works for:

```text
HDMI Capture

↓

Image

↓

AI

↓

Scene
```

This directly supports the project's long-term vision of PlayStation, Xbox, Nintendo Switch, and smart TV compatibility.

---

## Scalability

Adding support for new games requires no code changes.

If the AI understands the rendered image, the game is automatically supported.

---

## Maintainability

The application evolves by improving the AI model rather than building and maintaining thousands of game integrations.

---

# Trade-offs

## Advantages

- Universal compatibility
- Offline operation
- Privacy-first
- Cross-platform
- Future-proof
- Simple architecture
- Easy to extend

---

## Disadvantages

- AI inference is computationally heavier than rule-based approaches.
- Visual ambiguity may occasionally reduce confidence.
- Similar environments may require stabilization.
- Lighting effects can influence predictions.

These limitations are mitigated through scene stabilization and confidence thresholds.

---

# Consequences

The architecture centers on semantic understanding.

Modules are organized accordingly:

```text
Screen Capture

↓

Semantic AI

↓

Scene Stabilizer

↓

Decision Engine

↓

Scent Mapping

↓

Device Controller
```

Future enhancements improve the semantic layer rather than introducing game-specific integrations.

---

# Future Evolution

Semantic recognition provides a foundation for richer understanding.

Potential additions include:

- Weather recognition
- Time-of-day recognition
- Seasonal detection
- Indoor vs. outdoor classification
- Event detection (fire, explosions, vehicles)
- Dynamic scene blending
- Emotional atmosphere estimation

These capabilities extend the same pipeline rather than replacing it.

---

# Non-Goals

This decision does **not** include:

- Reading game memory
- Detecting player health
- Tracking inventory
- Parsing HUD elements
- Predicting game mechanics
- Identifying specific game titles

Those concerns are intentionally outside the scope of semantic scene recognition.

---

# Related ADRs

- ADR-0001 — Project Principles
- ADR-0002 — Python-Only Implementation
- ADR-0004 — Local Processing
- ADR-0005 — Event-Driven Architecture

---

# Summary

SceneSense recognizes **meaning**, not game internals.

```text
Rendered Screen

↓

Semantic Understanding

↓

Stable Scene

↓

Scent Decision

↓

Immersive Experience
```

By focusing on what the player actually sees, SceneSense achieves broad compatibility, protects user privacy, and avoids the maintenance burden of game-specific integrations. This decision also establishes a clear path toward future support for consoles, HDMI capture devices, streaming content, and other visual media, all while preserving a simple and extensible architecture.

---

# Appendix A – Approach Comparison

| Approach | Universal | Offline | Privacy | Console Ready | Selected |
|----------|-----------|----------|----------|---------------|----------|
| Semantic Scene Recognition | ✅ | ✅ | ✅ | ✅ | ✅ |
| Game Plugins | ❌ | ✅ | ✅ | ❌ | ❌ |
| Memory Reading | ❌ | ✅ | ⚠️ | ❌ | ❌ |
| OCR | ⚠️ | ✅ | ✅ | ✅ | ❌ |
| Template Matching | ❌ | ✅ | ✅ | ⚠️ | ❌ |
| Object Detection Only | ⚠️ | ✅ | ✅ | ✅ | ❌ |

---

# Appendix B – Long-Term Vision

```text
PC Screen
        │
        ▼
   Semantic AI
        │
        ▼
 Environment
        │
        ▼
 Decision Engine
        │
        ▼
  Scent Output

Future Inputs
─────────────

HDMI Capture
Streaming Video
Console Output
Movies
Television
Cloud Gaming

        │
        ▼
Same Semantic Pipeline
```

This architecture ensures that SceneSense's core intelligence remains centered on understanding visual context rather than platform-specific implementation details, enabling a consistent experience across current and future entertainment systems.