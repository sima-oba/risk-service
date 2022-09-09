from dataclasses import dataclass
from datetime import datetime

from .model import Model
from .point import Point


@dataclass
class FireRisk(Model):
    imported_id: str
    city_id: str
    date_time: datetime
    biome: str
    days_without_rain: int
    rain_fallout: str
    risk: str
    satellite: str
    geometry: Point
