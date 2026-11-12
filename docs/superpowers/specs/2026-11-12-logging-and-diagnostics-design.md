# Spec: Add Logging & Diagnostics Infrastructure

**Date:** 2026-11-12  
**Author:** SceneSense Development Team  
**Related Issue:** Phase 1 debugging and performance profiling requirements

---

## Project Overview

Add comprehensive logging and diagnostics infrastructure to SceneSense that enables developers to debug issues, profile performance, and diagnose crashes during the Proof-of-Concept phase. This includes structured logging, console formatting, file rotation, performance timing hooks, and crash report generation.

---

## Requirements

### Functional Requirements

#### FR1: Console Logging with Levels
**Given:** any module in SceneSense  
**When:** a log message is generated  
**Then:** output to console with appropriate level formatting:
- `DEBUG`: Detailed debugging information (e.g., internal state, low-level operations)
- `INFO`: Normal operational messages (e.g., frame captured, scene detected)
- `WARNING`: Potential issues (e.g., slow inference, frame drop warning)
- `ERROR`: Failures requiring attention (e.g., API failure, connection lost)
- `CRITICAL`: System-level issues (e.g., data corruption, unrecoverable state)

#### FR2: File Logging with Rotation
**Given:** logging is enabled  
**When:** application runs for extended period  
**Then:** logs are written to rotating file:
- Log directory: `logs/scenesense/`
- Max file size: 10 MB per file
- Keep last 5 files (rotate when limit reached)
- Format: JSON structured logging

#### FR3: Performance Timing Hooks
**Given:** operations with configurable timing  
**When:** operation completes  
**Then:** report timing metrics:
- Capture time per frame
- AI inference latency
- Event bus publish duration
- Console output: `Capture Time : 45.23 ms` (INFO level)

#### FR4: Error Stack Trace Logging
**Given:** an exception occurs  
**When:** exception is caught at any level  
**Then:** log full stack trace to file and console:
- File: same rotation as above
- Console: condensed message with option for full traceback
- Crash report: `logs/crash_reports/<timestamp>-crash-report.json`

#### FR5: Module Integration
**Given:** existing modules (capture, ai, device, events)  
**When:** logging infrastructure is initialized  
**Then:** each module produces structured logs:
- Include module name in log messages
- Format: `[timestamp] [level] [module.submodule] message`
- Console colors by level

#### FR6: Configurable Logging Level
**Given:** application startup  
**When:** user specifies log level via config file or CLI flag  
**Then:** adjust output verbosity accordingly:
- Default level: `INFO` (balanced output)
- Override options: `DEBUG`, `WARNING`, `ERROR`
- Config locations: embedded defaults in `config/loader.py` + optional config file `.scenesense/config.json` or `config/scenesense.yml`

### Non-Functional Requirements

#### NFR1: Console Output Performance
- Log writing overhead must be < 5ms per message
- Must not block main thread or capture/AI threads
- Use buffered I/O for file logging

#### NFR2: File Rotation Integrity
- Rotation must be atomic (no data loss on rotation)
- Corrupted log files should be skipped with warning
- Maintain log continuity across application restarts

#### NFR3: Memory Constraints
- Log buffer size: max 1 MB in memory
- No memory leaks during extended logging sessions
- Performance profiling must not increase memory usage > 5%

#### NFR4: Logging Initialization Timing
- Logger must initialize before any module uses it
- Initialization time: < 100ms
- Must not block application startup

#### NFR5: Crash Report Completeness
- Capture full exception context (state, recent operations)
- Include Python version, platform info
- Attach relevant module state snapshots if safe

---

## Design Decisions

### D1: Logging Architecture Pattern

**Option A:** Single global Logger class  
✓ Simple interface  
✓ Easy to instantiate once  
✗ Harder to test, harder to replace

**Option B:** Abstract Logger protocol with implementations (console, file)  
✓ Highly extensible  
✓ Allows testing with mock logger  
✓ Overkill for Phase 1

**Decision:** Use **hybrid pattern**:
- Single `Logger` class instantiated in `Bootstrap`
- Supports both console and file output simultaneously
- Internal abstraction allows future protocol implementation if needed

### D2: Console Formatter Choice

**Option A:** Plain text with prefix (no colors)  
✗ Harder to distinguish levels visually

**Option B:** Color-coded levels using ANSI escape codes  
✓ Industry standard  
✓ Clear visual distinction  

**Decision:** Use **ANSI colorized console output** via `colorama` library for cross-platform Windows/Linux support.

### D3: File Logging Format

**Option A:** Plain text with timestamps  
✗ Harder to parse programmatically

**Option B:** JSON structured format  
✓ Easy to parse with tools like Logstash, Loki  
✓ Enables future log aggregation  

**Decision:** Use **JSON format** for file output.

### D4: Performance Timing Strategy

**Option A:** Automatic timing to all public methods  
✗ Overhead everywhere, harder to disable later

**Option B:** Explicit marking (manual decorators on critical paths)  
✓ Minimal overhead when not needed  
✓ Clear visibility into what's being profiled  

**Decision:** Use **explicit manual decorators** on critical operations:
- `capture.capture_once()` - always time
- `ai_engine.infer_scene()` - always time  
- Other modules: optional timing via logger decorator if needed later

### D5: Module Naming Convention

**Option A:** Flat module names (`app.logger`)  
✗ No indication of which app module logged it

**Option B:** Full path from module (e.g., `app.capture.capture`)  
✓ Clear source identification  
✓ Matches CLAUDE.md guidance  

**Decision:** Use **full module path** in log messages.

### D6: Crash Report Contents

**Option A:** Only exception traceback  
✗ Too little context for debugging

**Option B:** Exception + moderate state info + platform info  
✓ Sufficient debugging information  
✓ Respects privacy (excludes frames/images)  

**Decision:** Include **traceback + moderate state snapshot** with config values and recent operations, excluding frame/image buffers.

---

## Open Questions (TBD)

1. **Q1:** Should we use Python's built-in `logging` module or external library like `loguru`?
   - *Impact:* Dependency management and simplicity
   - *Decision:* Use **Python's built-in `logging` module** (stdlib, no extra dependencies); can switch to loguru later if needed

2. **Q2:** What information should crash reports include about application state?
   - *Impact:* Debugging effectiveness vs. privacy/security
   - *Decision:* Include **moderate detail**: traceback + config values + recent operations, excluding frames/images

3. **Q3:** Should timing decorators be automatically added to all public methods or only critical paths?
   - *Impact:* Performance overhead vs. comprehensive profiling
   - *Decision:* Use **explicit manual decorators** on critical paths (capture, AI inference) initially; extend later if needed

---

## Success Criteria

### Unit Tests Required

- [ ] `test_logger_creation` - Logger initializes correctly
- [ ] `test_log_levels_console` - Console output shows correct level formatting and colors
- [ ] `test_log_rotation` - File rotation occurs at 10 MB threshold
- [ ] `test_performance_timing` - Timing decorators capture accurate durations
- [ ] `test_error_stack_trace` - Exceptions log full traceback with context
- [ ] `test_crash_report_generation` - Crash reports created with required fields
- [ ] `test_logging_no_blocking` - Logging does not block main thread (>95% of ops <1ms)

### Integration Tests Required

- [ ] All modules produce correctly formatted logs when integrated
- [ ] Console output appears in terminal with appropriate colors
- [ ] File rotation works without data loss
- [ ] Application startup completes within expected time (<2 seconds)

### Performance Metrics

- Console log overhead < 5ms per message (95th percentile)
- File log overhead < 10ms per message
- No memory increase > 5% after 1 hour of logging
- Startup time with logger initialized < 1 second

---

## Files to Create/Modify

| File | Action | Reason |
|------|--------|--------|
| `app/logger/__init__.py` | New | Package init, exports Logger class |
| `app/logger/logger.py` | New | Core logging implementation (levels, formatters, rotation) |
| `config/loader.py` | Modify | Add `logging_config` field to default config |
| `app/capture/capture.py` | Modify | Add timing hook to `capture_once()` method |
| `app/ai/ai_engine.py` | Modify | Add timing to inference operations |
| `app/device/serial_controller.py` | Modify | Add connection status logging |
| `app/events/event_bus.py` | Modify | Add event throughput metrics/logging |
| `app/bootstrap/bootstrap.py` | Modify | Initialize logger at startup, wire into modules |
| `tests/unit/test_logger.py` | New | Unit tests for Logger class and rotation |
| `tests/integration/test_logging_integration.py` | New | Integration tests across all modules |
| `logs/` | Create (dir) | Log directory for rotating files |
| `.gitignore` | Modify | Add `logs/` to gitignore |

---

## Logging Format Specifications

### Console Output Format

```
{COLOR:timestamp}{RESET} {COLOR[level]{LEVEL}{RESET}] {module}.{method} {message}{NEWLINE}

Example:
[2026-11-12 14:32:05] [INFO] [app.capture.capture] Captured frame: 1920x1080
```

### File Output Format (JSON)

```json
{
  "time": "2026-11-12T14:32:05.123456",
  "level": "INFO",
  "module": "app.capture.capture",
  "method": "capture_once",
  "message": "Captured frame: 1920x1080",
  "duration_ms": 45.23
}
```

### Error/Exception Format (JSON)

```json
{
  "time": "2026-11-12T14:32:05.123456",
  "level": "ERROR",
  "module": "app.device.serial_controller",
  "exception_type": "SerialTimeoutException",
  "message": "Failed to receive ACK within timeout",
  "stack_trace": "...",
  "state_snapshot": {
    "port": "/dev/ttyUSB0",
    "last_command": "CMD_PING",
    "retry_count": 2
  }
}
```

---

## Implementation Notes

### Phase 1 (Current POC)
- Use Python's built-in `logging` module + `colorama` for console colors
- Console + file output simultaneously via `RotatingFileHandler` (stdlib)
- Manual timing decorators on critical methods only
- Add optional config file support for log level settings

### Phase 2 (Future Enhancement)
- Optionally integrate with `loguru` or similar for advanced features
- Add structured log aggregation support (Loki, Elastic)
- Extend timing to all public methods if profiling reveals bottlenecks

---

## Related Documents

- [Device Status Monitor Spec](../specs/2026-11-12-add-device-status-monitor-design.md) - Uses similar logging patterns
- `CLAUDE.md` - Logging guidelines and error handling conventions
- [`docs/vision/NON_GOALS.md`](../vision/NON_GOALS.md) - Local-first design principles (no cloud logging)

---

## Acceptance Checklist

Before merging implementation:

- [ ] All unit tests pass (`pytest tests/unit/test_logger.py`)
- [ ] Console output is colorized and readable
- [ ] File rotation works correctly at 10 MB limit
- [ ] Timing metrics capture accurately
- [ ] Crash reports generated with full context
- [ ] No memory leaks detected over extended session
- [ ] All modules produce formatted logs when using Logger

---

## Approval Status

**Status:** Pending review

Next steps after approval:
1. Implement `app/logger/logger.py`
2. Update config to include logging options
3. Wire logger into Bootstrap initialization
4. Add timing hooks to capture and AI modules
5. Write unit tests
6. Run integration tests
