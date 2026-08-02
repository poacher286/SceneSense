# ADR-0004: Local Processing

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
5. Why Local Processing
6. Alternatives Considered
7. Privacy Considerations
8. Performance Considerations
9. Trade-offs
10. Consequences
11. Future Evolution
12. Summary

---

# Status

**Accepted**

All real-time SceneSense processing will occur **locally on the user's device**.

This includes:

- Screen capture
- Image preprocessing
- AI inference
- Scene recognition
- Scene stabilization
- Decision engine
- Scent mapping
- ESP32 communication

The application will not require a cloud service for normal operation.

---

# Context

SceneSense continuously analyzes what the user is seeing in order to determine the appropriate scent.

That means the application temporarily processes:

- Gameplay
- Movies
- Streaming video
- Desktop applications

Because this content may be private or copyrighted, choosing where processing occurs is a fundamental architectural decision.

Two primary approaches were considered:

1. Local processing
2. Cloud processing

---

# Problem Statement

The system must satisfy several requirements:

- Protect user privacy
- Minimize latency
- Work without Internet access
- Reduce operational costs
- Scale to many users
- Keep deployment simple
- Support future hardware devices

Sending captured frames to external servers conflicts with several of these goals.

---

# Decision

SceneSense will process all captured frames on the user's computer.

The processing pipeline is:

```text
Screen

↓

Capture

↓

AI Model

↓

Scene

↓

Decision

↓

ESP32
```

At no point in the normal workflow are images transmitted to an external service.

---

# Why Local Processing?

Local execution aligns with the project's guiding principles:

- Privacy-first
- Cross-platform
- Low latency
- Offline capable
- User ownership of data

It also reduces infrastructure complexity and recurring operational costs.

---

# Privacy

Users should retain full control over their visual data.

Captured frames:

- Stay in system memory
- Are processed immediately
- Are discarded after inference

By default:

- No screenshots are saved
- No gameplay is uploaded
- No recordings are created
- No cloud account is required

This significantly reduces privacy concerns.

---

# Offline Capability

SceneSense should continue working even if the user has no Internet connection.

Examples:

- Airplane mode
- Local gaming setups
- LAN parties
- Limited connectivity
- Home network outages

After the initial AI model download, the application should operate completely offline.

---

# Low Latency

Scent generation is highly sensitive to latency.

Cloud processing introduces:

- Upload time
- Server processing
- Network congestion
- Download time

These delays accumulate quickly.

Local inference eliminates network round trips.

Target latency:

| Stage | Target |
|--------|--------:|
| Screen Capture | <50 ms |
| Image Preprocessing | <20 ms |
| AI Inference | <200 ms |
| Decision Engine | <20 ms |
| Serial Communication | <50 ms |
| Total End-to-End | <500 ms |

---

# Reliability

Cloud services depend on:

- Internet connectivity
- Server availability
- Regional outages
- API stability

Local execution removes these dependencies.

The application remains usable regardless of external service availability.

---

# Cost

Cloud inference requires:

- GPU servers
- Bandwidth
- Storage
- Monitoring
- Maintenance

As the user base grows, operating costs increase.

Local processing shifts computation to the user's existing hardware, allowing the application to scale without proportional infrastructure costs.

---

# Security

Keeping data on the user's machine reduces several risks:

- Data interception
- Server breaches
- Unauthorized access
- Long-term storage exposure

While local software must still be secure, eliminating unnecessary data transmission reduces the overall attack surface.

---

# AI Model Distribution

Pretrained models are downloaded once during installation or first launch.

Typical flow:

```text
Install

↓

Download Model

↓

Store Locally

↓

Offline Inference
```

Subsequent execution uses the cached model without requiring Internet access.

---

# Resource Utilization

Local processing uses:

- CPU
- GPU (optional)
- System memory

This is acceptable because modern desktop systems are generally capable of running lightweight vision models at the target frame rate.

Users with more powerful hardware automatically benefit from faster inference.

---

# Alternatives Considered

## Cloud AI

### Advantages

- Access to larger models
- Centralized updates
- Reduced client requirements

### Disadvantages

- Privacy concerns
- Internet dependency
- Increased latency
- Ongoing infrastructure costs
- Bandwidth usage
- Potential service outages

**Decision:** Rejected.

---

## Hybrid Processing

Example:

- Local screen capture
- Cloud AI
- Local hardware control

Advantages:

- Smaller desktop application
- Easier model updates

Disadvantages:

- Privacy issues remain
- Network latency persists
- More complex architecture

**Decision:** Rejected for the core system.

Future optional features may explore hybrid capabilities, but they are outside the scope of the MVP.

---

## Remote Desktop Processing

Example:

Run SceneSense entirely on a remote server.

Advantages:

- Centralized management

Disadvantages:

- High latency
- Limited practicality
- Poor gaming experience
- Hardware dependency

**Decision:** Rejected.

---

# Trade-offs

## Advantages

- Strong privacy guarantees
- Offline operation
- Lower latency
- No recurring cloud costs
- Simple deployment
- Better reliability
- Easier regulatory compliance

---

## Disadvantages

- AI performance depends on user hardware.
- Larger local application size due to embedded models.
- Model updates require local downloads.
- Older systems may experience slower inference.

These trade-offs are acceptable because SceneSense targets modern desktop systems.

---

# Consequences

The decision influences the overall architecture.

```text
Capture

↓

AI

↓

Decision

↓

Device

↓

Diffuser
```

No cloud communication is required for normal runtime operation.

The application remains self-contained and predictable.

---

# Operational Model

Normal operation:

```text
User Starts Application

↓

Load Configuration

↓

Load Local AI Model

↓

Capture Screen

↓

Infer Scene

↓

Generate Scent Event

↓

Control ESP32
```

The network is not part of the execution path.

---

# Telemetry

By default:

- No usage analytics
- No gameplay telemetry
- No automatic uploads
- No remote diagnostics

If optional telemetry is introduced in the future, it should require explicit user consent and never include captured image data without clear authorization.

---

# Future Evolution

Local processing remains the default architecture.

Possible optional enhancements include:

- Model download updates
- Plugin marketplace
- Firmware update service
- Anonymous crash reporting (opt-in)
- Community-contributed scent profiles

These features should not interfere with offline functionality.

---

# Non-Goals

This decision does **not** prohibit:

- Downloading AI models
- Checking for software updates
- Firmware downloads
- Optional cloud-backed services

It simply establishes that **core runtime functionality must not depend on cloud processing**.

---

# Related ADRs

- ADR-0001 — Project Principles
- ADR-0002 — Python-Only Implementation
- ADR-0003 — Semantic Scene Recognition
- ADR-0005 — Event-Driven Architecture

---

# Summary

SceneSense performs all critical computation locally.

```text
Screen

↓

Local AI

↓

Scene Recognition

↓

Decision Engine

↓

ESP32

↓

Diffuser
```

This architecture prioritizes user privacy, minimizes latency, enables offline operation, and removes dependence on cloud infrastructure. It also simplifies deployment and ensures that the application's core functionality remains available regardless of Internet connectivity or external service availability.

---

# Appendix A – Local vs. Cloud

| Characteristic | Local Processing | Cloud Processing |
|---------------|------------------|------------------|
| Privacy | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Latency | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Offline Support | ✅ | ❌ |
| Internet Required | ❌ | ✅ |
| Operating Cost | Low | High |
| Scalability | User Hardware | Server Infrastructure |
| Data Ownership | User | Service Provider |
| Reliability | High | Network Dependent |
| Selected | ✅ | ❌ |

---

# Appendix B – Runtime Architecture

```text
+-------------------------+
|      User Display       |
+------------+------------+
             |
             v
+-------------------------+
|    Screen Capture       |
+------------+------------+
             |
             v
+-------------------------+
|  Local AI Inference     |
+------------+------------+
             |
             v
+-------------------------+
|  Scene Stabilization    |
+------------+------------+
             |
             v
+-------------------------+
|   Decision Engine       |
+------------+------------+
             |
             v
+-------------------------+
|   Device Controller     |
+------------+------------+
             |
             v
+-------------------------+
|         ESP32           |
+------------+------------+
             |
             v
+-------------------------+
|     Scent Diffuser      |
+-------------------------+
```

The complete processing pipeline remains on the user's device, ensuring that SceneSense delivers a fast, private, and reliable immersive experience without relying on external cloud services.