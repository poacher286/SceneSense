from app.ai.ai_engine import AIEngine
from app.capture.capture import ScreenCapture
from app.device.serial_controller import SerialController
from app.events.event_bus import EventBus, get_event_bus
from app.logger.crash_reporter import CrashReporter, get_crash_reporter
from app.logger.logger import Logger
from config.loader import ConfigLoader


class Bootstrap:
    def __init__(self):
        self.logger = None
        self.config = None
        self.event_bus = None

        self.ai = None
        self.capture = None
        self.device = None
        self.crash_reporter = None

    def start(self):

        print("=" * 60)
        print("SceneSense Starting...")
        print("=" * 60)

        self.load_configuration()  # Load config first so log level can be read from it

        self.initialize_logger()  # Now initialize logger with config-level or CLI arg

        self.initialize_event_bus()
        self.initialize_crash_reporter()  # Initialize crash reporter after logger

        self.initialize_ai()

        self.initialize_capture()

        self.run_capture_diagnostics()

        self.initialize_device()

        print("\nSceneSense is ready.\n")

    def initialize_logger(self, log_level: str | None = None):

        # Map config level string to logging module constant
        import logging

        level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }

        # Determine log level: CLI arg > config file > default config value > default INFO
        if log_level:
            effective_level = log_level
        elif self.config and "logging_config" in self.config:
            effective_level = self.config["logging_config"].get("level", "INFO")
        else:
            effective_level = "INFO"

        level_num = level_map.get(effective_level.upper(), logging.INFO)

        # Create Logger with the determined level
        self.logger = Logger(level=level_num)

        # Ensure log directory exists for file output
        try:
            import os

            log_dir = self.config.get("logging_config", {}).get(
                "file_output", "logs/scenesense"
            )
            os.makedirs(log_dir, exist_ok=True)
            # Update logger's file handler path after directory creation
            if self.logger.logger.handlers:
                for handler in self.logger.logger.handlers:
                    if hasattr(handler, "baseFilename"):
                        try:
                            from pathlib import Path

                            new_path = Path(log_dir) / os.path.basename(
                                handler.baseFilename
                            )
                            handler.baseFilename = str(new_path)
                        except (OSError, ValueError):
                            # Keep existing path if can't update it
                            pass  # Log handled by outer except block
        except OSError as e:
            self.logger.debug(
                f"Failed to create or configure log directory {log_dir}: {e}"
            )
        except PermissionError as e:
            self.logger.warning(f"Permission denied for log directory {log_dir}: {e}")

        self.logger.info("Logger initialized with level: %s", effective_level)

    def load_configuration(self):

        self.config = ConfigLoader().load()

        self.logger.info("Configuration loaded")

    def initialize_event_bus(self):

        self.event_bus = EventBus(logger=self.logger)

        # Subscribe to ScentTriggered events for metrics
        from app.events.events import ScentTriggered  # type: ignore
        try:
            self.event_bus.subscribe(ScentTriggered.__name__, lambda data: None)
            self.logger.debug(f"Subscribed to {ScentTriggered.__name__} events")
        except Exception as e:
            self.logger.warning(f"Failed to subscribe to ScentTriggered events: {e}")

        self.logger.info("Event Bus initialized with %d subscribers", len(self.event_bus.metrics))

    def initialize_crash_reporter(self):
        """Initialize crash reporter for unhandled exceptions."""

        try:
            from app.events.events import FrameCaptured, SceneDetected, SceneChanged  # type: ignore
            event_types = [FrameCaptured, SceneDetected, SceneChanged]

            # Wire crash reporter into modules
            self.crash_reporter = get_crash_reporter(logger=self.logger)

            # Ensure crash directory exists (created lazily when needed)
            import os
            try:
                os.makedirs("logs/crash_reports", exist_ok=True)
                self.logger.debug(f"Crash reports directory ready: logs/crash_reports")
            except PermissionError as e:
                self.logger.warning(f"Cannot create crash reports directory: {e}")

            self.logger.info("Crash Reporter initialized")

        except Exception as e:
            self.logger.error(f"Failed to initialize crash reporter: {e}")

    def initialize_ai(self):

        self.ai = AIEngine(self.event_bus, logger=self.logger)

        self.logger.info("AI Engine initialized")

    def initialize_capture(self):

        self.capture = ScreenCapture(logger=self.logger)

        self.logger.info("Screen Capture initialized")

    def initialize_device(self):

        self.device = SerialController(logger=self.logger)

        self.logger.info("Device Controller initialized")

    def run_capture_diagnostics(self):

        self.logger.info("Running screen capture diagnostics...")

        self.capture.print_monitor_info()

        # Time the capture operation using logger's timing context
        try:
            with self.logger.timeit("capture_once_diagnostics"):
                frame = self.capture.capture_once(save_debug_image=False)

            self.logger.info(f"Captured frame: {frame.width}x{frame.height}", method="capture_once")
        except Exception as e:
            # Report crash if capture fails
            try:
                self.crash_reporter.report_exception(e)
            except Exception as crash_error:
                self.logger.error(f"Crash report generation failed: {crash_error}")

            raise

        self.logger.info("Screen capture diagnostics completed.")
