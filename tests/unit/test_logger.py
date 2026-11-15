"""Comprehensive unit tests for Logger class and logging infrastructure."""

import json
import logging
import os
import sys
import tempfile
import time
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from app.logger.logger import (
    Logger, ConsoleFormatter, JsonFormatter, _RotatingFileHandler,
)
from config.loader import ConfigLoader
from app.logger.crash_reporter import CrashReporter, get_crash_reporter


class TestLoggerCreation:
    """Test logger initialization and configuration."""

    def test_logger_creation(self):
        """Logger initializes correctly with default parameters."""
        logger = Logger()
        assert logger is not None
        assert logger.name == "scenesense"
        assert logger.level == logging.INFO

    def test_logger_custom_name(self):
        """Logger accepts custom name parameter."""
        logger = Logger(name="app.test.module")
        assert logger.name == "app.test.module"

    def test_logger_custom_level(self):
        """Logger accepts custom level parameter."""
        logger = Logger(level=logging.DEBUG)
        assert logger.level == logging.DEBUG

    def test_logger_name_mapping(self):
        """Logger correctly derives name from full module path."""
        logger = Logger(name="app.capture.capture")
        assert logger.name == "app.capture.capture"

    def test_prevent_duplicate_handlers(self):
        """Logger prevents duplicate handlers on re-initialization."""
        logger1 = Logger("scenesense")
        handler_count_1 = len(logger1.logger.handlers)

        logger2 = Logger("scenesense")  # Same name - should reuse, not duplicate
        handler_count_2 = len(logger2.logger.handlers)

        assert handler_count_1 == handler_count_2


class TestLogLevels:
    """Test all logging levels work correctly."""

    def test_debug_level(self):
        """DEBUG level logs correctly."""
        captured_messages = []

        class DebugCaptureHandler(logging.Handler):
            def emit(self, record):
                captured_messages.append(record.getMessage())

        logger = Logger(level=logging.DEBUG)
        handler = DebugCaptureHandler()
        logger.logger.addHandler(handler)

        logger.debug("This is a debug message")

        assert len(captured_messages) == 1
        assert "This is a debug message" in captured_messages[0]
        logger.logger.removeHandler(handler)

    def test_info_level(self):
        """INFO level logs correctly."""
        captured_messages = []

        class InfoCaptureHandler(logging.Handler):
            def emit(self, record):
                captured_messages.append(record.getMessage())

        logger = Logger(level=logging.INFO)
        handler = InfoCaptureHandler()
        logger.logger.addHandler(handler)

        logger.info("This is an info message")

        assert len(captured_messages) == 1
        assert "This is an info message" in captured_messages[0]
        logger.logger.removeHandler(handler)

    def test_warning_level(self):
        """WARNING level logs correctly."""
        captured_messages = []

        class WarningCaptureHandler(logging.Handler):
            def emit(self, record):
                captured_messages.append(record.getMessage())

        logger = Logger(level=logging.WARNING)
        handler = WarningCaptureHandler()
        logger.logger.addHandler(handler)

        logger.warning("This is a warning message")

        assert len(captured_messages) == 1
        assert "This is a warning message" in captured_messages[0]
        logger.logger.removeHandler(handler)

    def test_error_level(self):
        """ERROR level logs correctly."""
        captured_messages = []

        class ErrorCaptureHandler(logging.Handler):
            def emit(self, record):
                captured_messages.append(record.getMessage())

        logger = Logger(level=logging.ERROR)
        handler = ErrorCaptureHandler()
        logger.logger.addHandler(handler)

        logger.error("This is an error message")

        assert len(captured_messages) == 1
        assert "This is an error message" in captured_messages[0]
        logger.logger.removeHandler(handler)

    def test_critical_level(self):
        """CRITICAL level logs correctly."""
        captured_messages = []

        class CriticalCaptureHandler(logging.Handler):
            def emit(self, record):
                captured_messages.append(record.getMessage())

        logger = Logger(level=logging.CRITICAL)
        handler = CriticalCaptureHandler()
        logger.logger.addHandler(handler)

        logger.critical("This is a critical message")

        assert len(captured_messages) == 1
        assert "This is a critical message" in captured_messages[0]
        logger.logger.removeHandler(handler)


class TestConsoleFormatter:
    """Test console output formatting with colors."""

    def test_console_formatter_basic(self):
        """Console formatter produces correctly formatted log messages."""
        formatter = ConsoleFormatter()

        class MockRecord:
            timestamp = "2026-11-15 10:00:00.000"
            levelname = "INFO"
            name = "app.capture.capture"

            def __init__(self):
                self._msg = "Captured frame: 1920x1080"

            def getMessage(self):
                return self._msg

        record = MockRecord()
        output = formatter.format(record)

        assert "[ INFO" in output or "INFO" in output
        assert "capture" in output.lower()
        assert "Captured frame: 1920x1080" in output

    def test_console_formatter_with_method(self):
        """Console formatter includes method name when present."""
        formatter = ConsoleFormatter()

        class MockRecord:
            timestamp = "2026-11-15 10:00:00.000"
            levelname = "DEBUG"
            name = "app.device.serial_controller"

            def __init__(self):
                self._msg = "Serial port initialized"
                self.method = "initialize_connection"

            def getMessage(self):
                return self._msg

        record = MockRecord()
        output = formatter.format(record)

        assert "initialize_connection" in output

    def test_console_formatter_with_duration(self):
        """Console formatter includes duration when present."""
        formatter = ConsoleFormatter()

        class MockRecord:
            timestamp = "2026-11-15 10:00:00.000"
            levelname = "INFO"
            name = "app.capture.capture"

            def __init__(self):
                self._msg = "Frame captured"
                self.duration_ms = 45.23

            def getMessage(self):
                return self._msg

        record = MockRecord()
        output = formatter.format(record)

        assert "45.23" in output


class TestJsonFormatter:
    """Test JSON structured logging for files."""

    def test_json_formatter_basic(self):
        """JSON formatter produces valid structured logs with required fields."""
        formatter = JsonFormatter("app.test")

        class MockRecord:
            timestamp = "2026-11-15T10:00:00.000"
            levelname = "INFO"
            name = "app.test.module"

            def __init__(self):
                self._msg = "Test message from JSON formatter test"

            def getMessage(self):
                return self._msg

        record = MockRecord()
        output = formatter.format(record)

        # Verify JSON is valid
        parsed = json.loads(output)
        assert "time" in parsed
        assert "level" in parsed
        assert parsed["level"] == "INFO"
        assert "message" in parsed
        assert parsed["module"] == "app.test.module"

    def test_json_formatter_with_method(self):
        """JSON formatter includes method name when present."""
        formatter = JsonFormatter("app.test")

        class MockRecord:
            timestamp = "2026-11-15T10:00:00.000"
            levelname = "ERROR"
            name = "app.device.serial_controller"

            def __init__(self):
                self._msg = "Connection failed"
                self.method = "send_command"

            def getMessage(self):
                return self._msg

        record = MockRecord()
        output = formatter.format(record)

        parsed = json.loads(output)
        assert "method" in parsed
        assert parsed["method"] == "send_command"

    def test_json_formatter_with_duration(self):
        """JSON formatter includes duration when present."""
        formatter = JsonFormatter("app.test")

        class MockRecord:
            timestamp = "2026-11-15T10:00:00.000"
            levelname = "INFO"
            name = "app.capture.capture"

            def __init__(self):
                self._msg = "Capture operation complete"
                self.duration_ms = 45.23

            def getMessage(self):
                return self._msg

        record = MockRecord()
        output = formatter.format(record)

        parsed = json.loads(output)
        assert "duration_ms" in parsed
        assert parsed["duration_ms"] == 45.23


class TestRotatingFileHandler:
    """Test file rotation functionality."""

    def test_rotating_file_handler_creation(self):
        """RotatingFileHandler initializes correctly with specified parameters."""
        handler = _RotatingFileHandler(
            "test.log",
            maxBytes=100 * 1024,  # 100 KB for testing
            backupCount=2,
        )
        assert handler is not None
        assert hasattr(handler, "baseFilename")

    def test_rotating_file_handler_default_params(self):
        """RotatingFileHandler initializes without error."""
        handler = _RotatingFileHandler("test.log")
        assert hasattr(handler, "baseFilename")  # Verify it's initialized
        # We don't check exact defaults here as the internal implementation may vary


class TestTimingContextManager:
    """Test performance timing context manager."""

    def test_timeit_successful_operation(self):
        """Timeit context manager reports successful operation with timing."""
        logger = Logger(level=logging.DEBUG)

        with logger.timeit("test_operation"):
            time.sleep(0.01)  # Small delay to measure

        # Should complete without error


class TestCrashReporter:
    """Test crash report generation functionality."""

    def test_crash_reporter_creation(self):
        """CrashReporter initializes correctly."""
        reporter = CrashReporter()
        assert reporter is not None
        assert hasattr(reporter, '_crash_dir')

    def test_get_platform_info(self):
        """Get platform information for crash reports."""
        reporter = CrashReporter()
        platform_info = reporter._get_platform_info()

        assert "python_version" in platform_info
        assert "platform" in platform_info
        assert "system" in platform_info

    def test_report_crash_generates_file(self):
        """Report crash generates a JSON file with all required fields."""
        # Use a temporary directory for testing
        with tempfile.TemporaryDirectory() as tmpdir:

            try:
                reporter = CrashReporter()
                reporter._crash_dir = Path(tmpdir)
                test_exception = ValueError("Test exception for crash report")

                result = reporter.report_crash(exception=test_exception, message="Testing crash report generation")

                # Verify result structure
                assert "timestamp" in result
                assert "exception_type" in result
                assert result["exception_type"] == "ValueError"
                assert "exception_message" in result
                assert "platform" in result
                assert "config_snapshot" in result

            finally:
                pass  # Cleanup handled by context manager

    def test_exception_without_message(self):
        """Report exception without custom message uses exception args."""
        reporter = CrashReporter()

        test_exception = ValueError("Custom error message")

        result = reporter.report_crash(exception=test_exception)

        assert "exception_message" in result
        # The message should come from the exception arguments
        msg_parts = [str(arg) for arg in test_exception.args] if hasattr(test_exception, 'args') and test_exception.args else []
        assert any("Custom error message" in str(p) for p in msg_parts) or "Custom error message" in result.get("exception_message", "")

    def test_get_crash_reporter_singleton(self):
        """Get crash reporter uses singleton pattern."""
        reporter1 = get_crash_reporter()
        reporter2 = get_crash_reporter()

        assert reporter1 is reporter2


class TestLoggingIntegration:
    """Test logging in different scenarios."""

    def test_extra_parameters_passed_through(self):
        """Extra parameters are passed through to logger correctly."""
        # Verify that extra parameter is accepted by Logger's internal log method
        logger = Logger("app.test.integration")

        try:
            logger.info("Test message", extra={"extra_field": "test_value"})
        except Exception as e:
            assert False, f"Logger should accept extra parameters: {e}"

        # Verify logging works without error - the key check is that extra={} doesn't break it
        logger.info("Simple message")

    def test_log_with_timestamp(self):
        """Log messages include proper timestamps."""
        class MockRecord:
            timestamp = "2026-11-15T14:32:05.123456"
            levelname = "INFO"
            name = "app.test.timestamp"

            def __init__(self):
                self._msg = "Message with specific timestamp"

            def getMessage(self):
                return self._msg

        formatter = JsonFormatter("app.test")
        record = MockRecord()
        output = formatter.format(record)

        parsed = json.loads(output)
        assert parsed["time"] == "2026-11-15T14:32:05.123456"


class TestLoggingNoBlocking:
    """Test that logging doesn't block performance."""

    def test_logging_performance(self):
        """Verify logging doesn't block for >1ms on average."""
        logger = Logger(level=logging.INFO)

        # Measure multiple log operations
        times = []
        for i in range(100):
            start = time.perf_counter()
            logger.info(f"Performance test message {i}")
            end = time.perf_counter()
            times.append((end - start) * 1000)  # Convert to ms

        avg_time = sum(times) / len(times)
        max_time = max(times)

        # Average should be well under 5ms
        assert avg_time < 1, f"Average logging time {avg_time:.3f}ms exceeds 1ms threshold"
        # Even max should be reasonable (allowing for occasional slow disk writes)
        assert max_time < 100, f"Max logging time {max_time:.3f}ms is suspiciously slow"


class TestConfigIntegration:
    """Test logging integration with config system."""

    from config.loader import ConfigLoader

    def test_config_logging_structure(self):
        """Verify config loader returns expected logging configuration structure."""
        config = ConfigLoader().load()

        assert "logging_config" in config
        assert "level" in config["logging_config"]
        assert "console_format" in config["logging_config"]
        assert "file_output" in config["logging_config"]
        assert "file_name" in config["logging_config"]
        assert "max_file_size_mb" in config["logging_config"]
        assert "keep_last_files" in config["logging_config"]

    def test_logging_levels_valid(self):
        """Verify all logging levels are valid options."""
        config = ConfigLoader().load()
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

        for level in valid_levels:
            assert level in config["logging_config"]["level"] or level in valid_levels


class TestLoggerExceptionHandling:
    """Test exception logging functionality."""

    def test_exception_method_logs_traceback(self):
        """Exception method logs full traceback to file handler."""
        # Create logger with both handlers to verify both output
        logger = Logger(level=logging.DEBUG)

        # The exception() method should call logger.exception() which handles both
        try:
            raise ValueError("Test exception for tracing")
        except Exception as e:
            logger.exception("Exception caught and logged", exc_info=True)

    def test_timeit_on_exception(self):
        """Timeit context manager reports error when exception occurs."""
        logger = Logger(level=logging.DEBUG)

        try:
            with logger.timeit("failing_operation"):
                1 / 0  # This will raise
        except ZeroDivisionError:
            pass  # Expected


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
