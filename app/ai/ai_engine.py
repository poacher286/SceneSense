import logging
from datetime import UTC, datetime
from pathlib import Path

from app.logger import Logger
from app.logger.crash_reporter import get_crash_reporter


# Initialize logger with module path
ai_logger = Logger("app.ai.ai_engine")


class AIEngine:
    def __init__(self, event_bus, logger=None):
        self.event_bus = event_bus
        self.logger = logger or ai_logger
        self.crash_reporter = get_crash_reporter(logger=self.logger)

        ai_logger.info("AI Engine initialized with event bus")
