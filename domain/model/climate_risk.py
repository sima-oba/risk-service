from typing import List
from dataclasses import dataclass
from datetime import datetime

from .model import Model


@dataclass
class ClimateRiskPeriod:
    period: int
    risk_percent: int


@dataclass
class ClimateRisk(Model):
    city_id: str
    date_time: datetime
    harvest: str
    ordinance: str
    crop: str
    cycle: str
    soil: str
    periods: List[ClimateRiskPeriod]
