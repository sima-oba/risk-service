from typing import List
from abc import ABC, abstractmethod

from domain.model import ClimateRisk


class IClimateRiskRepository(ABC):
    @abstractmethod
    def find_by_id(self, id: str) -> ClimateRisk:
        pass

    def search(
        self,
        year: int = None,
        city_id: str = None,
        ordinance: int = None,
        crop: str = None,
        cycle: str = None,
        soil: str = None
    ) -> List[ClimateRisk]:
        pass

    def add(self, risk: ClimateRisk) -> ClimateRisk:
        pass
