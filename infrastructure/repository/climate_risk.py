from typing import List
from datetime import datetime
from pymongo.database import Database

from domain.model import ClimateRisk, ClimateRiskPeriod
from domain.repository import IClimateRiskRepository


class ClimateRiskRepository(IClimateRiskRepository):
    def __init__(self, db: Database):
        self._collection = db['climate_risk']

    def _as_entity(self, doc: dict):
        doc['periods'] = [ClimateRiskPeriod(**it) for it in doc.pop('periods')]
        return ClimateRisk(**doc)

    def find_by_id(self, id: str) -> ClimateRisk:
        doc = self._collection.find_one({'_id': id})
        return self._as_entity(doc) if doc else None

    def search(
        self,
        year: int = None,
        city_id: str = None,
        ordinance: int = None,
        crop: str = None,
        cycle: str = None,
        soil: str = None
    ) -> List[ClimateRisk]:
        filter = {}

        if year:
            filter['date_time'] = {
                '$gte': datetime(year, 1, 1),
                '$lte': datetime(year + 1, 1, 1)
            }

        if city_id:
            filter['city_id'] = city_id

        if ordinance:
            filter['ordinance'] = ordinance

        if crop:
            filter['crop'] = crop

        if cycle:
            filter['cycle'] = cycle

        if soil:
            filter['soil'] = soil

        results = self._collection.find(filter)
        return [self._as_entity(doc) for doc in results]

    def add(self, risk: ClimateRisk) -> ClimateRisk:
        result = self._collection.insert_one(risk.asdict())
        risk._id = result.inserted_id
        return risk
