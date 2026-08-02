# SceneSense Device Controller

> **Version:** 1.0  
> **Status:** Phase 1 Design  
> **Module:** `device`

---

# Table of Contents

1. Purpose
2. Design Goals
3. Responsibilities
4. High-Level Architecture
5. Device Lifecycle
6. Device Discovery
7. Connection Management
8. Command Processing
9. State Management
10. Event Handling
11. Reliability
12. Error Handling
13. Configuration
14. Performance
15. Testing
16. Future Improvements

---

# Purpose

The Device Controller is responsible for managing all communication between the SceneSense application and external hardware.

It serves as the **bridge between software and the physical scent diffuser**.

The Device Controller hides all hardware-specific implementation details from the rest of the application.

```
Decision Engine

↓

ScentRequestedEvent

↓

Device Controller

↓

ESP32

↓

Diffuser
```

No other module communicates directly with the hardware.

---

# Design Goals

The Device Controller should be:

- Hardware-agnostic
- Reliable
- Thread-safe
- Asynchronous
- Self-healing
- Easy to replace

---

# Responsibilities

The Device Controller is responsible for:

- Discovering compatible devices
- Managing serial connections
- Sending commands
- Receiving responses
- Retrying failed commands
- Publishing device events
- Monitoring device health

The Device Controller is **not** responsible for:

- AI inference
- Business rules
- Scene recognition
- Screen capture

---

# High-Level Architecture

```text
ScentRequestedEvent

↓

Device Controller

↓

Command Queue

↓

Serial Driver

↓

ESP32

↓

Diffuser
```

---

# Module Structure

```
device/

controller.py

connection_manager.py

serial_driver.py

command_queue.py

health_monitor.py

device_state.py
```

Each component has a single responsibility.

---

# Device Lifecycle

```text
Application Start

↓

Scan Ports

↓

Connect

↓

Handshake

↓

Ready

↓

Process Commands

↓

Disconnect

↓

Reconnect
```

The controller should recover automatically whenever possible.

---

# Device Discovery

During startup:

```
Scan Serial Ports

↓

Send HELLO

↓

Receive WELCOME

↓

Select Device
```

Only compatible devices should be accepted.

---

# Connection States

The controller maintains one of the following states.

```text
Disconnected

Connecting

Connected

Ready

Busy

Error

Reconnecting
```

The current state is exposed to the UI.

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

Unexpected failures transition through:

```
Ready

↓

Error

↓

Reconnect

↓

Ready
```

---

# Connection Manager

Responsibilities:

- Open serial port
- Close serial port
- Detect disconnects
- Reconnect automatically
- Verify protocol version

Suggested interface:

```python
class ConnectionManager:

    def connect(self):
        pass

    def disconnect(self):
        pass

    def reconnect(self):
        pass
```

---

# Command Queue

Commands are queued before transmission.

```
Queue

↓

Serialize

↓

Send

↓

ACK

↓

Remove
```

Commands are processed sequentially.

---

# Queue Strategy

Recommended queue:

```
FIFO
```

Example:

```
Pine

Rain

Ocean

Smoke
```

↓

```
Send Pine

↓

ACK

↓

Send Rain
```

This guarantees ordering.

---

# Command Object

Example:

```python
@dataclass(frozen=True)
class DeviceCommand:
    id: str
    type: str
    payload: dict
    timestamp: datetime
```

Commands remain immutable.

---

# Command Processing

Pipeline:

```text
Receive Event

↓

Create Command

↓

Queue

↓

Serialize

↓

Send

↓

ACK

↓

Complete
```

---

# Event Handling

Input events:

```
ScentRequestedEvent
```

Output events:

```
DeviceConnectedEvent

DeviceDisconnectedEvent

DeviceErrorEvent

CommandCompletedEvent
```

Other modules subscribe to these events as needed.

---

# Health Monitoring

The controller periodically verifies device health.

Example:

```
PING

↓

PONG
```

Heartbeat interval:

```
5 Seconds
```

If no response is received:

```
Reconnect
```

---

# Reliability

Every command requires acknowledgement.

```
Send

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

Retry

↓

Retry

↓

Device Error
```

Maximum retries:

```
3
```

---

# Automatic Reconnect

If the USB cable disconnects:

```
Disconnected

↓

Retry

↓

Port Found

↓

Handshake

↓

Ready
```

The user should rarely need to restart the application.

---

# Error Handling

Possible failures:

- Port unavailable
- Device unplugged
- Invalid response
- Timeout
- Busy device

Recovery:

```
Log

↓

Retry

↓

Reconnect

↓

Continue
```

Failures should remain isolated to the Device Controller.

---

# Configuration

Example:

```yaml
device:

  auto_connect: true

  heartbeat_seconds: 5

  retries: 3

  timeout_ms: 1000
```

Behavior should be configurable without code changes.

---

# Logging

Useful log entries:

```
Device Found

Handshake Success

Command Sent

ACK Received

Retry

Heartbeat Failed

Reconnect Started

Reconnect Successful
```

Logging should include command IDs for traceability.

---

# Performance

Expected command latency:

```
< 100 ms
```

The Device Controller should process commands significantly faster than scent diffusion occurs.

---

# Metrics

Expose runtime metrics:

| Metric | Description |
|---------|-------------|
| Device State | Current connection state |
| Commands Sent | Total commands |
| Commands Failed | Failed transmissions |
| Retries | Retry count |
| Heartbeat Success | Successful PING/PONG cycles |
| Average Response Time | Round-trip latency |
| Reconnect Count | Automatic reconnects |

These metrics assist debugging and reliability analysis.

---

# Testing

## Unit Tests

- Queue operations
- State transitions
- Retry logic
- Connection management
- Heartbeat handling

---

## Integration Tests

- Decision Engine → Device Controller
- Device Controller → ESP32
- Disconnect → Reconnect
- Invalid response handling

---

## Manual Tests

Verify:

- Startup connection
- USB unplug/replug
- Multiple commands
- Timeout recovery
- Busy device handling
- Long-running stability

---

# Future Improvements

## Multiple Devices

Support:

```
ESP32 #1

↓

Environment Diffuser
```

```
ESP32 #2

↓

Event Diffuser
```

The controller manages multiple independent connections.

---

## Device Registry

Future versions may maintain a registry of supported hardware.

Example:

```
ESP32

Arduino Nano

Raspberry Pi Pico

Future Devices
```

Each device implements the same interface.

---

## Wireless Support

Replace USB Serial with:

- Wi-Fi
- Bluetooth
- ESP-NOW
- Ethernet

Higher-level modules remain unchanged.

---

## Firmware Updates

The controller may eventually:

```
Detect Update

↓

Upload Firmware

↓

Verify

↓

Restart Device
```

---

## Device Diagnostics

Possible diagnostic commands:

```
Temperature

Fan Status

Relay Status

Voltage

Cartridge Levels
```

These values can be displayed in the dashboard.

---

## Plugin Architecture

Future hardware plugins:

```
Diffuser

Lighting

Fans

Haptics

Air Pumps
```

Each plugin implements a common device interface.

---

# Design Principles

The Device Controller should:

- Hide hardware complexity
- Be transport-independent
- Isolate failures
- Guarantee command ordering
- Support automatic recovery
- Publish events instead of exposing hardware details

Hardware-specific logic should never leak into business logic.

---

# Sequence Diagram

```text
ScentRequestedEvent

↓

Device Controller

↓

Command Queue

↓

Serialize

↓

Serial Driver

↓

ESP32

↓

ACK

↓

CommandCompletedEvent
```

---

# End-to-End Example

```text
Stable Scene

Forest

↓

Decision Engine

↓

ScentRequestedEvent

↓

Device Controller

↓

Queue Command

↓

Serialize JSON

↓

USB Serial

↓

ESP32

↓

Activate Pine Cartridge

↓

ACK

↓

CommandCompletedEvent
```

---

# Summary

The Device Controller is the hardware abstraction layer of SceneSense.

It provides reliable communication with the scent diffuser while shielding the rest of the application from hardware-specific details.

```text
Receive Event

↓

Create Command

↓

Queue

↓

Transmit

↓

Verify

↓

Complete
```

By centralizing all hardware communication within a single module, SceneSense remains modular, maintainable, and adaptable to future hardware platforms. Whether the project evolves to support multiple diffusers, wireless communication, or entirely new immersive devices, the Device Controller can evolve independently without requiring changes to the AI, Decision Engine, or user interface.