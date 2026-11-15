import logging
from datetime import UTC, datetime

from app.logger import Logger
from app.logger.crash_reporter import get_crash_reporter


# Initialize logger with module path
device_logger = Logger("app.device.serial_controller")


class SerialController:
    def __init__(self, logger=None):
        self.logger = logger or device_logger
        self.crash_reporter = get_crash_reporter(logger=self.logger)
        device_logger.info("Serial Controller initialized with crash reporter")
