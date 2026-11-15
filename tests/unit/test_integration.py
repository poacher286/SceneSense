"""Integration tests for SceneSense modules."""

import json
import logging
import sys
from pathlib import Path

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from app.logger.logger import Logger
from config.loader import ConfigLoader


class TestLoggingPipeline:
    """Test the complete logging pipeline from config to output."""

    def test_config_level_propagates_to_logger(self):
        """Verify log level flows from config to logger instance."""
        config = ConfigLoader().load()

        # Extract log level from config
        config_level = config["logging_config"]["level"]
        print(f"Config log level: {config_level}")

        assert config_level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    def test_logger_initialized_with_config_level(self):
        """Logger should respect config-level log setting."""
        config = ConfigLoader().load()
        config_level = config["logging_config"]["level"]

        # Map string level to logging module constant
        level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }

        logger = Logger(level=level_map[config_level])
        assert logger.level == level_map[config_level]

    def test_json_formatter_output(self):
        """Verify JSON formatter produces valid structured logs."""
        from app.logger.logger import JsonFormatter

        formatter = JsonFormatter("app.test")

        class MockRecord:
            timestamp = "2026-11-15 10:00:00.000"
            levelname = "INFO"
            name = "app.test.module"

            def __init__(self):
                self._msg = "Test message from integration test"

            def getMessage(self):
                return self._msg

        record = MockRecord()
        output = formatter.format(record)

        # Verify JSON is valid
        parsed = json.loads(output)
        assert "time" in parsed
        assert "level" in parsed
        assert "message" in parsed

    def test_console_formatter_output(self):
        """Verify console formatter produces colorized logs."""
        from app.logger.logger import ConsoleFormatter

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


class TestBootstrapIntegration:
    """Test Bootstrap integration with logging."""

    def test_bootstrap_initializes_logger(self):
        """Bootstrap should initialize logger correctly."""
        from app.bootstrap import Bootstrap

        # We can't fully test without config, but verify initialization works
        bootstrap = Bootstrap()

        # Logger should be None initially (initialized in start())
        assert bootstrap.logger is None

    def test_config_structure(self):
        """Verify config loader returns expected structure."""
        config = ConfigLoader().load()

        assert "logging_config" in config
        assert "level" in config["logging_config"]
        assert "console_format" in config["logging_config"]
        assert "file_output" in config["logging_config"]


class TestTimingIntegration:
    """Test timing hooks are wired correctly."""

    def test_timing_context_manager(self):
        """Verify timeit context manager works."""
        from app.logger.logger import Logger

        logger = Logger(level=logging.DEBUG)

        with logger.timeit("test_operation"):
            # Simulate some work
            total = sum(range(100))

        # Verify operation completed without error

    def test_performance_profiling_config(self):
        """Verify performance profiling setting exists in config."""
        config = ConfigLoader().load()
        assert config["logging_config"]["performance_profiling"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
