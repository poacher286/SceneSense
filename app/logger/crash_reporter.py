"""Crash report generation module for SceneSense."""

import datetime
import json
import os
import sys
import traceback
from pathlib import Path

# Import logger early to avoid circular dependencies
from app.logger.logger import Logger


class CrashReporter:
    """Generates crash reports with full context for debugging."""

    def __init__(self, logger: Logger = None):
        self.logger = logger or Logger("app.logger.crash_reporter")
        self._crash_dir = Path("logs/crash_reports")
        # Don't auto-create directory; let user know if it fails

    @staticmethod
    def _get_platform_info():
        """Get platform and Python version information."""
        import platform
        import sysconfig

        return {
            "python_version": sys.version,
            "platform": platform.platform(),
            "system": platform.system(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "sys_platform": sys.platform,
            "executable": sys.executable,
            "version_info": {
                "major": sys.version_info.major,
                "minor": sys.version_info.minor,
                "micro": sys.version_info.micro,
                "releaselevel": sys.version_info.releaselevel,
                "serial": sys.version_info.serial,
            },
        }

    def _get_config_snapshot(self):
        """Get current configuration snapshot (excluding sensitive data)."""
        from config.loader import ConfigLoader

        try:
            config = ConfigLoader().load()
            # Return only non-sensitive fields for privacy
            safe_config = {
                k: v for k, v in config.items()
                if k not in ["serial_port", "api_key", "password", "token"]
            }
            return safe_config
        except Exception as e:
            self.logger.warning(f"Failed to capture config snapshot: {e}")
            return {}

    def _get_state_snapshot(self):
        """Capture current application state snapshot."""
        state = {
            "thread_count": sum(1 for _ in sys._current_frames().keys()),
            "memory_info": getattr(sys, "getsizeof", None),
        }

        # Try to get memory usage if available
        try:
            import os
            state["memory_kb"] = os.sysconf("SC_PAGE_SIZE") * os.memusage() if hasattr(os, "memusage") else None
        except Exception:
            pass

        return state

    def report_crash(self, exception: Exception | None = None, message: str = "") -> dict | None:
        """
        Generate a crash report with full context.

        Args:
            exception: The exception that caused the crash (optional)
            message: Custom message to include (optional)

        Returns:
            Dictionary with crash report data, or None if no file was created
        """
        start_time = datetime.datetime.now(datetime.timezone.utc)

        # Gather crash information
        crash_info = {
            "timestamp": start_time.isoformat(),
            "exception_type": exception.__class__.__name__ if exception else "None",
            "exception_message": str(exception) if exception else message or "No message provided",
            "platform": self._get_platform_info(),
            "config_snapshot": self._get_config_snapshot(),
            "state_snapshot": {
                "python_version": sys.version,
                "thread_count": len(sys._current_frames()),
            },
        }

        # Add stack trace if exception provided
        if exception:
            crash_info["stack_trace"] = traceback.format_exception(type(exception), exception, exception.__traceback__)

        # Create crash file path
        filename = f"{start_time.strftime('%Y%m%d-%H%M%S')}-crash-report.json"
        filepath = self._crash_dir / filename

        # Ensure crash directory exists
        try:
            os.makedirs(self._crash_dir, exist_ok=True)
            self.logger.info(f"Crash directory ready: {self._crash_dir}")
        except PermissionError as e:
            self.logger.error(f"Cannot create crash directory: {e}")
            return None
        except OSError as e:
            self.logger.error(f"Failed to create crash directory: {e}")
            return None

        # Write crash report to file
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(crash_info, f, indent=2, default=str)
            self.logger.info(f"Crash report saved: {filepath}")
            return crash_info
        except (IOError, OSError) as e:
            self.logger.error(f"Failed to write crash report: {e}")
            # Still return the in-memory data for debugging
            return crash_info

    def report_exception(self, exception: Exception = None) -> dict | None:
        """
        Report an exception with full context automatically.

        Args:
            exception: The exception to report (default: last caught exception)

        Returns:
            Crash info dictionary or None if failed
        """
        if exception is None:
            # Get the most recent exception if not provided
            exception = self._get_most_recent_exception()

        message = getattr(exception, "args", [])
        message_str = ", ".join(str(a) for a in message) if message else str(exception) or ""

        return self.report_crash(exception=exception, message=message_str)

    def _get_most_recent_exception(self) -> Exception | None:
        """Get the most recently caught exception from traceback."""
        try:
            import traceback

            # Get last exception from sys.exc_info if in an except block
            exc_type, exc_value, exc_tb = sys.exc_info()
            if exc_type is not None:
                return exc_value
        except Exception:
            pass

        # Otherwise return None - caller will provide exception or message
        return None


# Singleton instance for global use
_crash_reporter_instance = None


def get_crash_reporter(logger: Logger | None = None) -> CrashReporter:
    """Get or create the singleton CrashReporter instance."""
    global _crash_reporter_instance
    if _crash_reporter_instance is None:
        _crash_reporter_instance = CrashReporter(logger=logger)
    return _crash_reporter_instance


def setup_crash_handler(exception_handler: Exception | None = None, logger: Logger | None = None):
    """
    Set up a crash handler that generates reports and exits gracefully.

    Args:
        exception_handler: Custom exception to handle (optional)
        logger: Logger instance to use (optional)
    """
    reporter = get_crash_reporter(logger=logger)
    crash_info = reporter.report_exception(exception=exception_handler)

    if crash_info:
        print(f"\n{'='*60}")
        print("CRASH DETECTED - Report generated")
        print(f"{'='*60}")
        print(f"Exception Type: {crash_info['exception_type']}")
        print(f"Message: {crash_info['exception_message'][:100]}...")
        print(f"Report saved to: {str(Path('logs/crash_reports') / crash_info.get('_filename', 'N/A'))}")
        print(f"{'='*60}\n")

    # Exit with error code for CI/pipeline detection
    import sys
    sys.exit(1) if exception_handler else None  # type: ignore[func-returns-value]
