from config.loader import ConfigLoader
from app.events.event_bus import EventBus
from app.logger.logger import Logger
from app.ai.ai_engine import AIEngine
from app.capture.capture import ScreenCapture
from app.device.serial_controller import SerialController


class Bootstrap:

    def __init__(self):
        self.logger = None
        self.config = None
        self.event_bus = None

        self.ai = None
        self.capture = None
        self.device = None

    def start(self):

        print("=" * 60)
        print("SceneSense Starting...")
        print("=" * 60)

        self.initialize_logger()

        self.load_configuration()

        self.initialize_event_bus()

        self.initialize_ai()

        self.initialize_capture()

        self.initialize_device()

        print("\nSceneSense is ready.\n")

    def initialize_logger(self):

        self.logger = Logger()

        self.logger.info("Logger initialized")

    def load_configuration(self):

        self.config = ConfigLoader().load()

        self.logger.info("Configuration loaded")

    def initialize_event_bus(self):

        self.event_bus = EventBus()

        self.logger.info("Event Bus initialized")

    def initialize_ai(self):

        self.ai = AIEngine(self.event_bus)

        self.logger.info("AI Engine initialized")

    def initialize_capture(self):

        self.capture = ScreenCapture(self.event_bus)

        self.logger.info("Screen Capture initialized")

    def initialize_device(self):

        self.device = SerialController()

        self.logger.info("Device Controller initialized")