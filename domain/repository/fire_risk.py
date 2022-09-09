from typing import List
from abc import ABC, abstractmethod
from datetime import datetime

from domain.model import FireRisk


class IFireRiskRepository(ABC):
    @abstractmethod
    def find_by_city(
        self, city_id: str, start: datetime, end: datetime
    ) -> List[FireRisk]:
        pass

    def find_nearby(
        self,
        lat: float,
        lng: float,
        radius: float,
        start: datetime,
        end: datetime
    ) -> List[FireRisk]:
        pass

    def find_all(self, start: datetime, end: datetime) -> List[FireRisk]:
        pass

    def add(self, risk: FireRisk) -> FireRisk:
        pass
