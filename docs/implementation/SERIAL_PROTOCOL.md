# SceneSense Serial Communication Protocol

> **Version:** 1.0  
> **Status:** Phase 1 Design  
> **Module:** `device / serial`

---

# Table of Contents

1. Purpose
2. Design Goals
3. Overview
4. Architecture
5. Communication Flow
6. Transport Layer
7. Packet Format
8. Commands
9. Responses
10. Connection Lifecycle
11. Device Discovery
12. Reliability
13. Error Handling
14. Configuration
15. Testing
16. Future Improvements

---

# Purpose

The Serial Protocol defines how the SceneSense desktop application communicates with the ESP32 controller.

The protocol is designed to be:

- Human-readable
- Easy to debug
- Versioned
- Extensible
- Reliable
- Independent of hardware implementation

The desktop application never controls GPIO pins directly—it communicates exclusively through this protocol.

---

# Design Goals

The protocol should:

- Be simple to implement
- Minimize latency
- Support acknowledgements
- Be backward compatible
- Be extensible
- Allow debugging using a serial monitor

---

# High-Level Architecture

```text
SceneSense Desktop

↓

Device Controller

↓

Serial Protocol

↓

USB Serial

↓

ESP32 Firmware

↓

Relay / MOSFET Driver

↓

Scent Cartridge
```

---

# Communication Flow

```
Decision Engine

↓

ScentRequestedEvent

↓

Device Controller

↓

Serialize Command

↓

USB Serial

↓

ESP32

↓

Execute Command

↓

ACK
```

---

# Transport Layer

Phase 1 uses:

```
USB Serial
```

Recommended settings:

| Parameter | Value |
|----------|-------|
| Baud Rate | 115200 |
| Data Bits | 8 |
| Stop Bits | 1 |
| Parity | None |
| Flow Control | None |

These settings are supported across all major operating systems.

---

# Message Format

Each command is a single UTF-8 text line.

Example:

```text
SCENT,PINE,0.35,2000
```

Fields are comma-separated.

Each command ends with:

```
\n
```

This simplifies parsing on the ESP32.

---

# Command Structure

General format:

```text
COMMAND,PARAM1,PARAM2,...
```

Example:

```text
SCENT,PINE,0.40,2500
```

Meaning:

```
Diffuse

↓

Pine

↓

40% Intensity

↓

2500 ms
```

---

# Supported Commands

## HELLO

Desktop → Device

```text
HELLO
```

Response:

```text
WELCOME,1.0
```

Used to verify protocol compatibility.

---

## PING

Desktop:

```text
PING
```

ESP32:

```text
PONG
```

Used for heartbeat monitoring.

---

## SCENT

Desktop:

```text
SCENT,PINE,0.35,2000
```

Meaning:

```
Activate Pine

↓

35%

↓

2 Seconds
```

---

## STOP

```text
STOP
```

Stops all active scent outputs immediately.

---

## STATUS

Desktop:

```text
STATUS
```

ESP32:

```text
STATUS,READY
```

Possible states:

```
READY

BUSY

ERROR

OFFLINE
```

---

## RESET

```text
RESET
```

Resets the device state without restarting the ESP32.

---

# Device Responses

Every command should receive a response.

Examples:

```text
ACK
```

or

```text
ERROR,INVALID_COMMAND
```

The desktop waits for a response before marking the command complete.

---

# Acknowledgements

Successful execution:

```text
ACK
```

Failure:

```text
ERROR,DEVICE_BUSY
```

Timeout:

```
No response

↓

Retry
```

---

# Protocol Versioning

Handshake:

Desktop:

```text
HELLO
```

ESP32:

```text
WELCOME,1.0
```

Future versions:

```text
WELCOME,2.0
```

The desktop can reject incompatible versions gracefully.

---

# Connection Lifecycle

```text
USB Connected

↓

Open Port

↓

HELLO

↓

WELCOME

↓

READY

↓

Normal Operation
```

If the handshake fails, the device remains disconnected.

---

# Device Discovery

The Device Controller scans available serial ports.

Example:

```
COM3

COM4

/dev/cu.usbserial

/dev/ttyUSB0
```

Each candidate receives:

```text
HELLO
```

The first device responding with:

```text
WELCOME
```

is selected.

---

# State Machine

```text
Disconnected

↓

Connecting

↓

Handshake

↓

Ready

↓

Busy

↓

Ready

↓

Disconnected
```

The desktop always knows the current device state.

---

# Reliability

Retry strategy:

```
Send

↓

Wait

↓

ACK?

↓

Yes

↓

Complete
```

Otherwise:

```
Retry

↓

Maximum Retries

↓

Device Error
```

Recommended retry count:

```
3
```

---

# Timeouts

Suggested timeout:

```
1000 ms
```

If exceeded:

```
Retry
```

After three failures:

```
Disconnect Device
```

---

# Error Codes

Examples:

| Code | Description |
|------|-------------|
| INVALID_COMMAND | Unknown command |
| INVALID_SCENT | Unknown scent |
| DEVICE_BUSY | Device already active |
| INVALID_ARGUMENT | Parameter error |
| HARDWARE_ERROR | Relay failure |
| INTERNAL_ERROR | Unexpected firmware issue |

Error codes are returned in plain text.

Example:

```text
ERROR,INVALID_SCENT
```

---

# Configuration

Example:

```yaml
serial:

  baud_rate: 115200

  timeout_ms: 1000

  retries: 3

  auto_connect: true
```

---

# Logging

Useful log entries:

```
Port Opened

Handshake Success

Command Sent

ACK Received

Retry

Device Lost

Reconnect Successful
```

Raw serial logging should be optional.

---

# Performance

Serial bandwidth requirements are minimal.

Typical command:

```text
SCENT,PINE,0.35,2000
```

≈ 25 bytes

Even dozens of commands per second remain well below the bandwidth limit.

---

# Testing

## Unit Tests

- Packet formatting
- Parsing
- Validation
- Retry logic

---

## Integration Tests

- Desktop ↔ ESP32
- Handshake
- Command execution
- Timeout recovery

---

## Manual Tests

Verify:

- Device discovery
- Auto reconnect
- Invalid commands
- Power cycling
- USB reconnect

---

# Metrics

Expose runtime metrics:

| Metric | Description |
|---------|-------------|
| Connected | Device status |
| Commands Sent | Total commands |
| ACK Received | Successful responses |
| Retries | Retry count |
| Timeouts | Communication failures |
| Average Response Time | Round-trip latency |

---

# Future Improvements

## Binary Protocol

Replace text commands with compact binary packets.

Advantages:

- Smaller
- Faster
- CRC support

Phase 1 intentionally uses text for simplicity.

---

## Checksums

Future packet:

```text
SCENT,PINE,0.35,2000,CRC32
```

Protects against corrupted serial data.

---

## Multiple Devices

Support:

```
ESP32 #1

↓

Left Diffuser
```

```
ESP32 #2

↓

Right Diffuser
```

---

## Wireless Transport

Replace USB with:

- Bluetooth
- Wi-Fi
- ESP-NOW

The protocol remains unchanged.

---

## Firmware Updates

Future commands:

```text
UPDATE
```

```
BEGIN

↓

TRANSFER

↓

VERIFY

↓

COMPLETE
```

---

## Diagnostics

Possible command:

```text
DIAG
```

Response:

```text
TEMP,34

FAN,ON

CARTRIDGE,OK
```

Useful for troubleshooting hardware.

---

# Design Principles

The protocol should:

- Be human-readable
- Be deterministic
- Support version negotiation
- Require acknowledgements
- Be backward compatible
- Avoid unnecessary complexity

The desktop application should communicate only through this protocol, never relying on hardware-specific assumptions.

---

# Example Session

```text
Desktop

HELLO

↓

ESP32

WELCOME,1.0

↓

Desktop

STATUS

↓

ESP32

STATUS,READY

↓

Desktop

SCENT,PINE,0.35,2000

↓

ESP32

ACK

↓

Desktop

PING

↓

ESP32

PONG

↓

Desktop

STOP

↓

ESP32

ACK
```

---

# End-to-End Flow

```text
Stable Scene

↓

Decision Engine

↓

Scent Mapping

↓

ScentRequestedEvent

↓

Device Controller

↓

Serialize Command

↓

USB Serial

↓

ESP32

↓

Relay

↓

Diffuser
```

---

# Summary

The Serial Protocol provides a simple, reliable communication layer between the SceneSense desktop application and the ESP32 hardware.

It hides hardware details behind a clean, versioned interface while ensuring reliable command delivery through acknowledgements and retries.

```text
Create Command

↓

Serialize

↓

Send

↓

ACK

↓

Complete
```

By keeping the protocol text-based in Phase 1, development and debugging remain straightforward. As the project matures, the protocol can evolve to support binary encoding, wireless transports, multiple devices, firmware updates, and advanced diagnostics without changing the higher-level application architecture.