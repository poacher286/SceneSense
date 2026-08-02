# SceneSense Communication Protocol

> **Version:** 1.0  
> **Status:** Phase 1 Design  
> **Module:** `hardware`

---

# Table of Contents

1. Purpose
2. Design Goals
3. Protocol Overview
4. Architecture
5. Communication Flow
6. Transport Layer
7. Message Format
8. Command Types
9. Response Types
10. Device State
11. Error Handling
12. Reliability
13. Versioning
14. Security
15. Future Improvements

---

# Purpose

The SceneSense Communication Protocol defines how the desktop application communicates with the ESP32 firmware.

The protocol is designed to be:

- Simple
- Human-readable
- Versioned
- Reliable
- Extensible

The protocol abstracts the underlying transport mechanism so that the same messages can be used over USB, Wi-Fi, or Bluetooth in future versions.

---

# Design Goals

The protocol should:

- Be easy to debug
- Minimize latency
- Support acknowledgements
- Detect invalid messages
- Be forward compatible
- Remain transport independent

---

# High-Level Architecture

```text
+----------------------+
| SceneSense Desktop   |
+----------------------+
           │
           ▼
+----------------------+
| Protocol Layer       |
+----------------------+
           │
           ▼
+----------------------+
| USB / Wi-Fi / BLE    |
+----------------------+
           │
           ▼
+----------------------+
| ESP32 Firmware       |
+----------------------+
           │
           ▼
+----------------------+
| Diffuser Hardware    |
+----------------------+
```

The desktop application and firmware communicate **only** through protocol messages.

---

# Phase 1 Transport

Phase 1 uses:

```
USB Serial
```

Configuration:

| Property | Value |
|----------|-------|
| Baud Rate | 115200 |
| Data Bits | 8 |
| Stop Bits | 1 |
| Parity | None |

---

# Message Format

Messages are exchanged as JSON objects.

General structure:

```json
{
  "id": "cmd-001",
  "type": "activate",
  "payload": {},
  "timestamp": "2026-08-01T15:30:00Z"
}
```

Each message includes:

- Unique ID
- Message type
- Payload
- Timestamp

---

# Message Lifecycle

```text
Create Message

↓

Serialize JSON

↓

Send

↓

Receive

↓

Validate

↓

Process

↓

Respond
```

---

# Command Types

Supported Phase 1 commands:

| Command | Description |
|----------|-------------|
| hello | Device handshake |
| activate | Trigger scent |
| stop | Stop active scent |
| heartbeat | Device health check |
| status | Request device status |
| reset | Reset firmware |

---

# Handshake

Desktop:

```json
{
  "id": "1",
  "type": "hello",
  "payload": {
    "client": "SceneSense",
    "version": "1.0.0"
  }
}
```

ESP32:

```json
{
  "id": "1",
  "type": "hello_response",
  "payload": {
    "device": "ESP32",
    "firmware": "1.0.0",
    "status": "ready"
  }
}
```

The application should not send other commands until the handshake succeeds.

---

# Activate Command

Example:

```json
{
  "id": "42",
  "type": "activate",
  "payload": {
    "cartridge": "pine",
    "intensity": 35,
    "duration": 2
  }
}
```

Payload fields:

| Field | Description |
|--------|-------------|
| cartridge | Cartridge name |
| intensity | 0–100 (%) |
| duration | Seconds |

---

# Stop Command

```json
{
  "id": "43",
  "type": "stop"
}
```

Immediately stops:

- Fan
- Valve
- Diffusion

---

# Status Command

Desktop:

```json
{
  "id": "44",
  "type": "status"
}
```

ESP32:

```json
{
  "id": "44",
  "type": "status_response",
  "payload": {
    "state": "ready",
    "uptime": 1842,
    "firmware": "1.0.0"
  }
}
```

---

# Heartbeat

Desktop:

```json
{
  "id": "50",
  "type": "heartbeat"
}
```

ESP32:

```json
{
  "id": "50",
  "type": "heartbeat_response"
}
```

Recommended interval:

```
Every 5 Seconds
```

---

# Acknowledgements

Every command receives an acknowledgement.

Success:

```json
{
  "id": "42",
  "type": "ack"
}
```

Failure:

```json
{
  "id": "42",
  "type": "nack",
  "payload": {
    "error": "invalid_cartridge"
  }
}
```

---

# Error Codes

Standard error codes:

| Code | Meaning |
|------|---------|
| invalid_json | JSON parsing failed |
| invalid_command | Unknown command |
| invalid_payload | Missing or invalid field |
| invalid_cartridge | Unknown cartridge |
| invalid_duration | Duration out of range |
| invalid_intensity | Intensity out of range |
| busy | Device is busy |
| timeout | Command timed out |
| internal_error | Unexpected firmware error |

These codes should remain stable across firmware versions.

---

# Device States

Supported states:

```text
BOOTING

INITIALIZING

READY

BUSY

ERROR
```

Commands are accepted only in the `READY` state.

---

# Reliability

The protocol guarantees:

- One response per command
- Command validation
- Ordered processing
- Deterministic responses

Commands are processed sequentially.

---

# Timeouts

Recommended timeout:

```
1 Second
```

If no response is received:

```text
Retry

↓

Reconnect

↓

Report Error
```

Maximum retries:

```
3
```

---

# Sequence Diagram

```text
Desktop

↓

Activate

↓

ESP32

↓

Validate

↓

Execute

↓

ACK

↓

Desktop
```

---

# Versioning

Every handshake includes protocol information.

Example:

```json
{
  "protocol": "1.0"
}
```

Future firmware can reject unsupported protocol versions.

---

# Validation Rules

The firmware validates:

- JSON syntax
- Required fields
- Message type
- Payload schema
- Value ranges

Invalid messages are rejected immediately.

---

# Logging

Both sides should log:

- Sent messages
- Received messages
- Validation failures
- ACK/NACK
- Timeouts

Message IDs should appear in every log entry.

---

# Performance Targets

| Metric | Target |
|----------|--------|
| Parse JSON | < 5 ms |
| Validate | < 2 ms |
| Execute | < 20 ms |
| ACK Response | < 50 ms |

---

# Configuration

Example:

```yaml
protocol:

  version: 1.0

  timeout_ms: 1000

  retries: 3

  heartbeat_seconds: 5
```

---

# Security Considerations

Phase 1 assumes a trusted local USB connection.

Future wireless transports should consider:

- Authentication
- Encryption (TLS where applicable)
- Replay protection
- Device pairing

---

# Testing

## Unit Tests

- JSON parsing
- Payload validation
- Error generation
- Version checks

---

## Integration Tests

- Handshake
- Command execution
- Timeout handling
- Invalid payloads
- ACK/NACK responses

---

## Manual Tests

Verify:

- Device connection
- Multiple commands
- Long-duration operation
- Disconnect/reconnect
- Invalid commands

---

# Future Improvements

## Binary Protocol

Replace JSON with a compact binary format for lower latency and reduced bandwidth.

---

## Message Compression

Compress large payloads (future telemetry or diagnostics).

---

## Batch Commands

Allow multiple commands in a single packet.

Example:

```json
{
  "type": "batch",
  "commands": [
    { "type": "activate", "payload": { "cartridge": "pine", "duration": 2, "intensity": 40 } },
    { "type": "activate", "payload": { "cartridge": "rain", "duration": 1, "intensity": 20 } }
  ]
}
```

---

## Device Discovery

Future Wi-Fi protocol:

```text
Desktop

↓

Network Scan

↓

SceneSense Devices

↓

Connect
```

---

## Telemetry

The firmware may periodically publish:

- Temperature
- Fan speed
- Valve status
- Cartridge status
- Uptime

---

## Firmware Updates

Support firmware upload using the same protocol.

Example:

```text
Upload

↓

Verify

↓

Flash

↓

Restart
```

---

# Best Practices

✔ Use unique message IDs

✔ Validate every payload

✔ Always return ACK or NACK

✔ Keep messages small

✔ Maintain backward compatibility

✔ Separate protocol from transport

✔ Log every transaction

✔ Version the protocol

---

# Example End-to-End Exchange

### 1. Handshake

Desktop:

```json
{
  "id": "1",
  "type": "hello"
}
```

ESP32:

```json
{
  "id": "1",
  "type": "hello_response",
  "payload": {
    "status": "ready"
  }
}
```

---

### 2. Activate Pine

Desktop:

```json
{
  "id": "2",
  "type": "activate",
  "payload": {
    "cartridge": "pine",
    "intensity": 40,
    "duration": 2
  }
}
```

ESP32:

```json
{
  "id": "2",
  "type": "ack"
}
```

---

### 3. Heartbeat

Desktop:

```json
{
  "id": "3",
  "type": "heartbeat"
}
```

ESP32:

```json
{
  "id": "3",
  "type": "heartbeat_response"
}
```

---

# Summary

The SceneSense Communication Protocol provides a clean, reliable, and extensible contract between the desktop application and the ESP32 firmware.

```text
Create

↓

Serialize

↓

Transmit

↓

Validate

↓

Execute

↓

Respond
```

By separating protocol definition from the underlying transport, SceneSense gains flexibility to evolve from a USB-connected prototype to future wireless and multi-device architectures without changing the higher-level software components. A simple JSON-based protocol also makes development, debugging, and future expansion significantly easier during the early phases of the project.

---

# Appendix A – Complete Message Reference

| Message Type | Direction | Description |
|--------------|-----------|-------------|
| `hello` | Desktop → ESP32 | Begin handshake |
| `hello_response` | ESP32 → Desktop | Handshake response |
| `activate` | Desktop → ESP32 | Trigger a scent |
| `stop` | Desktop → ESP32 | Stop active diffusion |
| `status` | Desktop → ESP32 | Request device status |
| `status_response` | ESP32 → Desktop | Current device information |
| `heartbeat` | Desktop → ESP32 | Health check |
| `heartbeat_response` | ESP32 → Desktop | Heartbeat acknowledgement |
| `ack` | ESP32 → Desktop | Successful command execution |
| `nack` | ESP32 → Desktop | Command rejected |

---

# Appendix B – Protocol Evolution

| Protocol Version | Features |
|------------------|----------|
| **1.0** | USB Serial, JSON messages, ACK/NACK, heartbeat |
| **2.0** | Wi-Fi transport, telemetry, device discovery |
| **3.0** | Binary protocol, firmware updates, multiple diffusers |
| **4.0** | Secure communication, authentication, encrypted transport |

This evolution strategy ensures that early prototypes remain simple while providing a clear path toward a robust, production-ready communication layer.