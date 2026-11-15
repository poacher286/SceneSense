"""Core logging implementation for SceneSense using Python's built-in logging module."""

import json
import logging
import logging.handlers  # Import before using handlers.RotatingFileHandler
import sys
import time
from datetime import UTC, datetime

import colorama


class Logger:
    """SceneSense logger with console and file output support."""

    # Color codes for console output
    COLORS = {
        "DEBUG": colorama.Fore.CYAN + colorama.Style.DIM,
        "INFO": colorama.Fore.GREEN,
        "WARNING": colorama.Fore.YELLOW,
        "ERROR": colorama.Fore.RED,
        "CRITICAL": colorama.Fore.MAGENTA + colorama.Style.BRIGHT,
    }
    RESET = colorama.Style.RESET_ALL

    def __init__(self, name: str = "scenesense", level: int = logging.INFO):
        """
        Initialize the logger.

        Args:
            name: Logger name (module path)
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        # Store level and name BEFORE calling _setup_handlers
        self.name = name
        self.level = level

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Prevent duplicate handlers on re-initialization
        if not self.logger.handlers:
            self._setup_handlers()

    def _setup_handlers(self):
        """Set up console and file handlers."""
        # Console handler with color formatter
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.level)
        console_formatter = ConsoleFormatter()
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # File handler for rotating logs
        try:
            file_handler = _RotatingFileHandler(
                "logs/scenesense/app.log",
                maxBytes=10 * 1024 * 1024,  # 10 MB
                backupCount=5,
                encoding="utf-8",
            )
            file_handler.setLevel(getattr(logging, self.level.upper()))
            file_formatter = JsonFormatter(self.name)
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
        except OSError as e:
            # If logs directory can't be created (permission/exists), continue with console only
            self.logger.warning(f"Cannot create log directory {log_dir}: {e}")
        except Exception as e:
            # Catch-all for unexpected errors during handler setup
            self.logger.debug(f"Unexpected error in _setup_handlers: {e}")

    def debug(self, message: str, **extra):
        """Log DEBUG level message."""
        self._log(logging.DEBUG, message, **extra)

    def info(self, message: str, **extra):
        """Log INFO level message."""
        self._log(logging.INFO, message, **extra)

    def warning(self, message: str, **extra):
        """Log WARNING level message."""
        self._log(logging.WARNING, message, **extra)

    def error(self, message: str, **extra):
        """Log ERROR level message."""
        self._log(logging.ERROR, message, **extra)

    def critical(self, message: str, **extra):
        """Log CRITICAL level message."""
        self._log(logging.CRITICAL, message, **extra)

    def _log(self, level_num: int, message: str, method: str = "", **extra):
        """Internal log method with timing and formatting."""
        # Use simple logging call for Python 3.11+ compatibility
        self.logger.log(level_num, message)

    def exception(self, message: str, **extra):
        """Log exception with full stack trace."""
        self.logger.exception(message, **extra)

    def timeit(self, operation_name: str):
        """Context manager for timing operations."""
        start = time.perf_counter()

        class TimingHandler:
            def __init__(self, name, logger_instance):
                self.name = name
                # Store references to parent's log methods
                self.info_func = logger_instance.info
                self.error_func = logger_instance.error

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                duration_ms = (time.perf_counter() - start) * 1000
                if exc_type is None:
                    self.info_func(
                        f"Operation completed: {self.name} in {duration_ms:.2f} ms",
                        method=operation_name,
                    )
                else:
                    self.error_func(
                        f"Operation failed: {self.name} after {duration_ms:.2f} ms",
                        method=operation_name,
                        exc_type=exc_type.__name__,
                    )
                return False

        return TimingHandler(self.name, self)


class ConsoleFormatter(logging.Formatter):
    """Console formatter with color support."""

    COLORS = {
        "DEBUG": colorama.Fore.CYAN + colorama.Style.DIM,
        "INFO": colorama.Fore.GREEN,
        "WARNING": colorama.Fore.YELLOW,
        "ERROR": colorama.Fore.RED,
        "CRITICAL": colorama.Fore.MAGENTA + colorama.Style.BRIGHT,
    }
    RESET = colorama.Style.RESET_ALL

    def format(self, record: logging.LogRecord) -> str:
        level_color = self.COLORS.get(record.levelname, "")
        reset = self.RESET

        timestamp = getattr(
            record, "timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        module = getattr(
            record,
            "module",
            record.name.split(".")[-1] if record.name else "scenesense",
        )

        formatted_message = f"{level_color}{timestamp}{reset} [{level_color}{record.levelname:.<8}{reset}] [{module:<30}{reset}] {record.getMessage()}"

        # Add method if present
        if hasattr(record, "method"):
            formatted_message += f" - {record.method}"

        # Add duration if present
        if hasattr(record, "duration_ms"):
            formatted_message += f" (Duration: {record.duration_ms:.2f}ms)"

        return formatted_message


class JsonFormatter(logging.Formatter):
    """JSON formatter for file output."""

    def __init__(self, default_module: str = "scenesense"):
        self.default_module = default_module

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "time": getattr(record, "timestamp", datetime.now(UTC).isoformat()),
            "level": record.levelname,
            "module": getattr(record, "module", record.name),
            "message": record.getMessage(),
        }

        if hasattr(record, "method"):
            log_data["method"] = record.method

        if hasattr(record, "duration_ms"):
            log_data["duration_ms"] = record.duration_ms

        # Safely access exc_info with default value
        exc_info_val = getattr(record, "exc_info", None)
        if exc_info_val:
            exc_type = exc_info_val[1].__class__.__name__ if exc_info_val[1] else ""
            log_data["exception_type"] = exc_type
            log_data["stack_trace"] = (
                "".join(exc_info_val[2])
                if hasattr(exc_info_val, "__iter__")
                else str(exc_info_val)
            )

        return json.dumps(log_data, default=str)


class _RotatingFileHandler(logging.handlers.RotatingFileHandler):
    """Internal rotating file handler (avoid name conflict)."""

    def __init__(self, filename: str, maxBytes=10 * 1024 * 1024, backupCount=5):
        super().__init__(filename, maxBytes, backupCount)


# Convenience functions for direct logging calls
def get_logger(name: str = "scenesense", level: int = logging.INFO) -> Logger:
    """Get or create a logger instance."""
    return Logger(name, level)
