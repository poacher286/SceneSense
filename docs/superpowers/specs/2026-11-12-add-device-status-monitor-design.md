# Spec: Add Device Status Monitor

**Date:** 2026-11-12  
**Author:** Generated with Claude Code

## Project Overview

Add a device status monitor to the SceneSense application that tracks the health and connectivity of external devices (ESP32 diffuser, serial controllers) and reports their status through events.

---

## Requirements

### Functional Requirements

#### FR1: Monitor Device Health
**Given:** a connected device  
**When:** the heartbeat interval expires  
**Then:** send a ping command to the device  
**And:** record response time in metrics

#### FR2: Report Device State via Events
**Given:** a device state change (connected/disconnected/timeout)  
**When:** the change is detected  
**Then:** publish `DeviceStateChanged` event with:
- `device_id`: unique identifier
- `status`: "online", "offline", or "degraded"
- `last_seen`: timestamp
- `error_message`: if applicable

#### FR3: Handle Connection Recovery
**Given:** a device went offline  
**When:** reconnection succeeds  
**Then:** automatically attempt reconnection up to MAX_RETRY times (configurable, default 3)  
**And:** log each retry attempt

#### FR4: Display Device Status in UI
**Given:** the application is running  
**When:** viewing the dashboard  
**Then:** show device status indicators for all monitored devices  
**And:** update status every HEARTBEAT_INTERVAL (default 5 seconds)

### Non-Functional Requirements

#### NFR1: Performance
- Status check overhead must be < 10ms per device
- Must not block main thread or capture/AI threads

#### NFR2: Error Handling
- Network timeouts treated as "offline" status after TIMEOUT_THRESHOLD (default 3s)
- Invalid responses treated as "degraded" status with error logged

#### NFR3: Logging
- Log WARN for offline transitions
- Log ERROR for repeated failures (> MAX_RETRY attempts)
- Log DEBUG for successful heartbeats

---

## Design Decisions

### D1: Monitor Implementation Pattern

**Option A:** Polling via dedicated thread  
✓ Simple to implement  
✓ Predictable timing behavior  
✗ Constant CPU usage even when idle

**Option B:** Event-driven monitoring (via EventBus)  
✓ Low overhead, only checks when needed  
✓ Scales with number of devices  
✗ Requires careful event ordering  

**Decision:** Use **Option B** (event-driven) for efficiency and scalability.

### D2: Heartbeat Protocol

**Current device protocol:** Send simple command → Wait for ACK response  
**Proposed enhancement:** Add "heartbeat" variant with lower timeout threshold  
**Rationale:** Differentiate between real disconnections and slow responses

---

## Open Questions (TBD)

1. **Q1:** Should device monitoring be configurable per-device (e.g., only monitor critical devices)?
   - *Impact:* Affects configuration schema
   - *Decision pending:* Default to monitoring all connected devices

2. **Q2:** What metrics should be exposed (latency, uptime, error counts)?
   - *Impact:* UI dashboard design
   - *Decision pending:* Start with 3 core metrics, allow extension

---

## Success Criteria

### Unit Tests Required
- [ ] Test heartbeat command sends and receives ACK
- [ ] Test timeout triggers offline status event
- [ ] Test reconnection retry logic (max attempts respected)
- [ ] Test invalid response handling (degraded status)

### Integration Tests Required
- [ ] DeviceStatusMonitor integrates with EventBus correctly
- [ ] Status updates appear in dashboard UI
- [ ] Event flow: FrameCaptured → AI → Decision → ScentTriggered → CommandSent → DeviceStateUpdated

### Performance Metrics
- Average status check time < 10ms (95th percentile)
- No memory leak over 24-hour monitoring period
- CPU usage < 1% when idle

---

## Files to Create/Modify

| File | Action | Reason |
|------|--------|--------|
| `app/device/status_monitor.py` | New | Core monitor implementation |
| `app/events/device_status_events.py` | New | Define status event dataclasses |
| `app/bootstrap/bootstrap.py` | Modify | Initialize status monitor in bootstrap |
| `tests/unit/device/test_status_monitor.py` | New | Unit tests for monitor |
| `tests/integration/test_device_health.py` | New | Integration tests |

---

## Related Documents

- [Device Controller](../implementation/DEVICE_CONTROLLER.md) - Base serial controller to extend
- [Serial Protocol](../implementation/SERIAL_PROTOCOL.md) - Command format reference
- [Event Bus](../architecture/EVENT_BUS.md) - Event publishing/subscribing patterns
