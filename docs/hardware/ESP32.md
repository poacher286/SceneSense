# SceneSense ESP32 Firmware

> **Version:** 1.0  
> **Status:** Phase 1 Design  
> **Module:** `hardware`

---

# Table of Contents

1. Purpose
2. Why ESP32
3. Design Goals
4. Responsibilities
5. Hardware Overview
6. Firmware Architecture
7. Boot Process
8. State Machine
9. Serial Communication
10. Command Processing
11. Diffuser Control
12. Pin Assignments
13. Safety Features
14. Error Handling
15. Logging
16. Testing
17. Future Improvements

---

# Purpose

The ESP32 acts as the hardware controller for SceneSense.

Its primary responsibility is to receive commands from the desktop application and control the scent diffuser hardware.

The ESP32 **does not perform AI inference or scene recognition**. All perception and decision-making occur on the host computer.

---

# Why ESP32?

The ESP32 was selected because it offers:

- Dual-core processor
- USB Serial communication
- Wi-Fi (future)
- Bluetooth (future)
- Hardware PWM
- Large GPIO count
- Low cost
- Strong community support

These capabilities make it suitable for both Phase 1 (USB) and future wireless deployments.

---

# Design Goals

The firmware should be:

- Reliable
- Deterministic
- Low latency
- Easy to update
- Hardware-independent where possible
- Easy to test
- Extensible

---

# Responsibilities

The ESP32 is responsible for:

- Receiving commands
- Validating messages
- Controlling fans
- Activating scent cartridges
- Returning acknowledgements
- Monitoring hardware status
- Reporting errors

The ESP32 is **not** responsible for:

- Screen capture
- AI inference
- Scene stabilization
- Business logic
- Scent selection

---

# High-Level Architecture

```text
SceneSense Desktop

↓

USB Serial

↓

ESP32 Firmware

↓

Command Processor

↓

Hardware Controller

↓

Fan

Solenoid

Relay

Atomizer
```

---

# Firmware Modules

```
firmware/

main.cpp

serial.cpp

protocol.cpp

controller.cpp

fan.cpp

cartridge.cpp

heartbeat.cpp

config.h

pins.h

logger.cpp
```

Each module has a single responsibility.

---

# Boot Process

```text
Power On

↓

Initialize GPIO

↓

Initialize Serial

↓

Initialize Hardware

↓

Self Test

↓

Ready
```

The firmware should not accept commands until initialization completes.

---

# Firmware State Machine

```text
Booting

↓

Initializing

↓

Ready

↓

Executing Command

↓

Ready
```

Failure path:

```text
Error

↓

Recover

↓

Ready
```

---

# Communication

Phase 1 communication uses:

```
USB Serial
```

Default settings:

```
115200 Baud

8 Data Bits

No Parity

1 Stop Bit
```

---

# Protocol

Commands are exchanged as JSON.

Example:

```json
{
  "command": "activate",
  "cartridge": "pine",
  "intensity": 35,
  "duration": 2
}
```

---

# Acknowledgement

Successful execution:

```json
{
  "status": "ok"
}
```

Failure:

```json
{
  "status": "error",
  "reason": "invalid_cartridge"
}
```

---

# Command Flow

```text
Receive JSON

↓

Parse

↓

Validate

↓

Execute

↓

Return ACK
```

---

# Supported Commands

| Command | Description |
|----------|-------------|
| hello | Handshake |
| activate | Release scent |
| stop | Stop diffusion |
| heartbeat | Health check |
| status | Device information |
| reset | Reset controller |

---

# Handshake

Desktop:

```json
{
  "command": "hello"
}
```

ESP32:

```json
{
  "device": "SceneSense",
  "version": "1.0",
  "status": "ready"
}
```

---

# Device States

```
BOOTING

INITIALIZING

READY

BUSY

ERROR
```

Commands are accepted only in the **READY** state.

---

# Diffuser Control

The firmware translates high-level commands into hardware actions.

Example:

```text
Activate Pine

↓

Enable Cartridge Valve

↓

Start Fan

↓

Wait

↓

Stop Fan

↓

Close Valve
```

---

# Timing Example

```
Valve Open

0 ms

↓

Fan Start

100 ms

↓

Diffuse

2000 ms

↓

Valve Close

↓

Fan Stop
```

---

# Fan Control

Fan speed is controlled using PWM.

Example:

```
0%

25%

50%

75%

100%
```

Higher scent intensity corresponds to higher fan speed.

---

# Cartridge Control

Each cartridge is connected to a dedicated output.

Example:

```
GPIO 18

↓

Pine
```

```
GPIO 19

↓

Rain
```

Only one cartridge is active at a time in Phase 1.

---

# Example Pin Assignment

| GPIO | Function |
|-------|----------|
| GPIO18 | Pine Valve |
| GPIO19 | Ocean Valve |
| GPIO21 | Rain Valve |
| GPIO22 | Smoke Valve |
| GPIO23 | Fan PWM |
| GPIO2 | Status LED |

Pin assignments may change as hardware evolves.

---

# Status LED

LED states:

| Color/Pattern | Meaning |
|---------------|---------|
| Solid | Ready |
| Slow Blink | Initializing |
| Fast Blink | Error |
| Pulse | Command executing |

---

# Heartbeat

Desktop:

```text
PING
```

ESP32:

```text
PONG
```

Recommended interval:

```
5 Seconds
```

---

# Safety Features

The firmware should include:

- Maximum diffusion duration
- Watchdog timer
- Invalid command rejection
- Over-current protection (hardware)
- Automatic fan shutdown
- Safe startup state

---

# Maximum Runtime

Maximum continuous activation:

```
10 Seconds
```

Longer requests should be rejected or truncated.

---

# Command Validation

Verify:

- Valid JSON
- Known command
- Valid cartridge
- Duration limits
- Intensity limits

Invalid commands return an error response.

---

# Error Handling

Examples:

```
Invalid JSON

Unknown Command

Busy Device

Hardware Failure

Timeout
```

Each error returns a descriptive response.

---

# Logging

Useful log entries:

```
Boot Complete

Command Received

Command Executed

ACK Sent

Heartbeat

Error
```

Logs may be sent over Serial during development.

---

# Firmware Configuration

Example:

```cpp
#define BAUD_RATE 115200
#define MAX_DURATION 10
#define HEARTBEAT_TIMEOUT 5000
```

Centralize configuration in `config.h`.

---

# Performance Targets

| Metric | Target |
|----------|--------|
| Boot Time | < 2 s |
| Command Parse | < 5 ms |
| Command Execution | < 20 ms |
| ACK Response | < 50 ms |

---

# Testing

## Unit Tests

- JSON parsing
- Command validation
- State transitions
- Timing calculations

---

## Integration Tests

- USB communication
- Fan control
- Valve activation
- Multiple commands

---

## Manual Tests

Verify:

- Startup
- Handshake
- Scent activation
- Stop command
- Invalid command
- USB reconnect

---

# Firmware Updates

Future versions may support:

- OTA updates
- USB firmware flashing
- Version verification
- Rollback

---

# Future Wireless Support

Future transports:

```
USB

↓

Wi-Fi

↓

Bluetooth

↓

ESP-NOW
```

The protocol remains unchanged regardless of transport.

---

# Future Hardware Expansion

Support:

- Multiple fans
- Temperature sensor
- Humidity sensor
- Cartridge level sensors
- RGB lighting
- Haptic devices

---

# Best Practices

✔ Keep firmware simple

✔ Never block the main loop

✔ Validate every command

✔ Fail safely

✔ Respond quickly

✔ Separate protocol from hardware logic

✔ Use meaningful error messages

---

# Example End-to-End Sequence

```text
Desktop

↓

Activate Forest

↓

USB Serial

↓

ESP32

↓

Validate

↓

Open Pine Valve

↓

Start Fan

↓

Diffuse

↓

Stop Fan

↓

Close Valve

↓

ACK
```

---

# Summary

The ESP32 firmware is the hardware execution layer of SceneSense.

It receives validated scent commands from the desktop application and safely controls the physical diffuser hardware.

```text
Receive

↓

Validate

↓

Execute

↓

Respond
```

By keeping the firmware focused on hardware control and leaving all AI, scene recognition, and decision-making to the desktop application, the system remains modular, reliable, and easy to extend. Future communication methods such as Wi-Fi or Bluetooth can be introduced without changing the higher-level software architecture.