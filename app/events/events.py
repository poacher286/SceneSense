from dataclasses import dataclass

from app.capture.frame import Frame


@dataclass(slots=True)
class FrameCaptured:
    frame: Frame