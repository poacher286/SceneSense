import logging


class Logger:

    def __init__(self):

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s",
        )

        self.logger = logging.getLogger("SceneSense")

    def info(self, message):

        self.logger.info(message)

    def error(self, message):

        self.logger.error(message)