from dataclasses import dataclass
import numpy as np


@dataclass(slots=True)
class Frame:
    """
    Represents one captured desktop frame.
    """

    image: np.ndarray
    width: int
    height: int
    timestamp: float