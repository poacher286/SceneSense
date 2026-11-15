# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development Workflow

**Run the application:**
```bash
python -m app.main
```

**Install dependencies:**
```bash
python -m pip install -r requirements.txt
```

**Run all tests:**
```bash
python -m pytest
```

**Run a specific test:**
```bash
python -m pytest tests/test_module.py::TestClass::test_method
```

**Lint code:**
```bash
python -m ruff check app tests
```

**Format code:**
```bash
python -m ruff format app tests
```

### Makefile Targets (optional)

```bash
make install    # Install dependencies
make run        # Run the application
make test       # Run all tests
make lint       # Lint code
make format     # Format code
```

## Architecture Overview

SceneSense is an AI-powered desktop application that observes game/video scenes and triggers immersion effects (currently scent diffusers) based on what it sees. It operates entirely locally for privacy.

### Core Pipeline

The application follows this data flow:

```
Game Window → Screen Capture → AI Recognition → Scene Stabilization 
→ Decision Engine → Event Bus → [Device Controller] [UI]
                              ↓
                          ESP32 Diffuser
```

### Module Structure (`app/`)

| Package | Responsibility | Key Files |
|---------|----------------|-----------|
| `bootstrap` | Initializes all modules (logger, config, event bus, AI, capture, device) | `bootstrap.py` |
| `config` | Loads configuration from YAML/JSON | `loader.py` |
| `capture` | Captures screen frames using PyAutoGUI/MSS | `capture.py`, `frame.py`, `monitor.py` |
| `ai` | Runs scene recognition models (CLIP, etc.) | `ai_engine.py` |
| `stabilizer` | Smooths AI predictions to reduce noise | *(TODO)* |
| `decision` | Detects meaningful scene transitions | *(TODO)* |
| `device` | Manages hardware communication via USB serial | `serial_controller.py` |
| `events` | Event bus for module communication | `event_bus.py`, `events.py` |
| `ui` | Desktop dashboard UI (PySide6) | *(TODO)* |
| `logger` | Logging utilities | `logger.py` |
| `common` | Shared utilities, types, exceptions | *(TODO)* |

### Event System

The event bus enables loose coupling between modules:

- **Events defined in** `app/events/events.py`
- **Published via** `EventBus.publish(event, data)`
- **Subscribed via** `event_bus.subscribe(event, callback)`

Example event flow:
```
FrameCaptured → SceneDetected → SceneChanged → ScentTriggered → CommandSent
```

### Threading Model

The application uses multiple threads for parallel processing:

- **Capture Thread**: Captures frames at configured FPS
- **AI Thread**: Runs inference in background
- **Decision Thread**: Processes scene transitions
- **UI Thread**: Keeps dashboard responsive
- **Serial Thread**: Handles USB communication

### Configuration Structure

Configuration is centralized and externalized (default in `config/loader.py`):

```python
{
    "capture_fps": 5,              # Frames per second for screen capture
    "serial_port": "/dev/tty.usbserial",  # USB port for ESP32
    "ai_model": "clip"             # AI model to use (CLIP, etc.)
}
```

### Key Design Principles

1. **Modularity**: Each subsystem has a single responsibility and is independently replaceable.
2. **Event-Driven**: Modules communicate via events, not direct method calls.
3. **Local First**: No data leaves the user's machine.
4. **AI Before Game Integration**: Understands scenes visually, not via game APIs.
5. **Output Agnostic**: AI produces context; devices react independently.

### Typical Development Flow

1. Extend an existing module (e.g., add a new device driver in `device/`)
2. Publish events for cross-module communication (`events/events.py`)
3. Subscribe to relevant events in other modules
4. Test each component independently via the event bus
5. Integrate through the bootstrap pattern

### Bootstrapping Pattern

All modules are initialized in `Bootstrap.start()`:
1. Initialize logger
2. Load configuration
3. Set up event bus
4. Initialize AI engine
5. Initialize capture module
6. Run capture diagnostics
7. Initialize device controller

This centralized initialization ensures all dependencies are wired correctly before execution.

## Common Tasks

### Adding a New Event

1. Create an event dataclass in `app/events/events.py`
2. Publish it via the event bus when needed
3. Subscribe to it in modules that should react

### Adding a New Device Driver

1. Extend `SerialController` or create a new subclass
2. Subscribe to `ScentTriggered` events
3. Convert events to device-specific commands
4. Handle connection management and retries

### Switching AI Models

1. Modify `AIEngine` in `app/ai/ai_engine.py` to load the new model
2. Update configuration (`ai_model` setting in `config/loader.py`)
3. Ensure output format matches expected scene predictions (e.g., CLIP returns textual embeddings)
4. Update scent mappings in decision engine if needed

### Adding a New Device Controller

1. Extend `SerialController` in `app/device/serial_controller.py` or create new subclass
2. Subscribe to `ScentTriggered` events via EventBus
3. Implement protocol encoding (see `docs/hardware/PROTOCOL.md`)
4. Handle connection management, timeouts, and retries
5. Register device in bootstrap initialization

### Working with Events

1. Define new event type in `app/events/events.py` using dataclass decorator
2. Publish via `event_bus.publish(EventType, data)` from any module
3. Subscribe via `event_bus.subscribe(EventType, callback)` in listening modules
4. Common event flow: `FrameCaptured → SceneDetected → SceneChanged → ScentTriggered → CommandSent`
5. Never pass large image buffers in events (use references or shared frame pool)

### Threading & Concurrency

- **Capture Thread**: Runs `ScreenCapture.capture_once()` in loop at configured FPS
- **AI Thread**: Processes frames asynchronously via event-driven approach
- **Serial Thread**: Handles USB communication with retry logic
- All threads share immutable events via EventBus; avoid shared mutable state
- Use `queue.Queue` for frame buffering if needed
- Protect shared resources with `threading.Lock`

### Testing Guidelines

- Run all tests: `python -m pytest`
- Run specific test: `python -m pytest tests/test_module.py::TestClass::test_method`
- Unit tests live in `tests/unit/` mirroring source structure
- Integration tests in `tests/integration/` for pipeline validation
- Use fixtures in `tests/fixtures/` for test data

### Common Pitfalls to Avoid

1. **Circular imports**: Keep module dependencies unidirectional (Capture → AI → Decision → Device)
2. **Hardcoded config**: Always use `ConfigLoader()` from bootstrap
3. **Blocking main thread**: AI inference and capture must run asynchronously
4. **Large events**: Never embed raw image data in events; use Frame references only
5. **Silent failures**: Log all exceptions, implement retry logic for serial comms
6. **Thread safety**: Protect shared state with locks or immutable data structures

### Project Status & Phases

- **Phase 1 (Current)**: POC with screen capture, CLIP scene recognition, basic USB comms to ESP32
- Core modules exist but implementations are stubs awaiting full logic
- Event bus enables loose coupling; future devices can subscribe without code changes
