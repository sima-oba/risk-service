from typing import Tuple
from dataclasses import dataclass


@dataclass
class Point:
    coordinates: Tuple[float, float]
    type: str = 'Point'
