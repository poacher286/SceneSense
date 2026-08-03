import time
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
from mss import mss

from app.capture.frame import Frame
from app.capture.monitor import MonitorManager


class ScreenCapture:

    def __init__(self):
        self.sct = mss()
        self.monitor_manager = MonitorManager()
        self.monitor = self.monitor_manager.get_primary_monitor()

    def print_monitor_info(self):
        print("\nPrimary Monitor")
        print("-" * 30)
        print(f"Left   : {self.monitor['left']}")
        print(f"Top    : {self.monitor['top']}")
        print(f"Width  : {self.monitor['width']}")
        print(f"Height : {self.monitor['height']}")
        print()

    def capture_once(self, save_debug_image: bool = False) -> Frame:
        """
        Capture a single frame from the primary monitor.

        Args:
            save_debug_image: Save the captured frame as an image.

        Returns:
            Frame object containing the captured image.
        """

        start = time.perf_counter()

        # Capture screen
        screenshot = self.sct.grab(self.monitor)

        # Convert to NumPy array
        image = np.array(screenshot)

        # Save debug image only if requested
        if save_debug_image:
            self._save_debug_image(image)

        elapsed = (time.perf_counter() - start) * 1000
        print(f"Capture Time : {elapsed:.2f} ms")

        return Frame(
            image=image,
            width=screenshot.width,
            height=screenshot.height,
            timestamp=time.time(),
        )

    def _save_debug_image(self, image: np.ndarray) -> None:
        """
        Save a captured frame for debugging.
        """

        output_dir = Path("output/captures")
        output_dir.mkdir(parents=True, exist_ok=True)

        filename = datetime.now().strftime("%Y%m%d_%H%M%S.png")

        output_file = output_dir / filename

        cv2.imwrite(
            str(output_file),
            cv2.cvtColor(image, cv2.COLOR_BGRA2BGR),
        )

        print(f"Debug image saved: {output_file}")