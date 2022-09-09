from typing import List
from pymongo.database import Database
from datetime import datetime

from domain.model import FireRisk, Point
from domain.repository import IFireRiskRepository


class FireRiskRepository(IFireRiskRepository):
    def __init__(self, db: Database):
        self._collection = db['fire_risk']

    def _as_entity(self, doc: dict) -> FireRisk:
        point = Point(**doc.pop('geometry'))
        return FireRisk(**doc, geometry=point)

    def find_by_city(
        self, city_id: str, start: datetime, end: datetime
    ) -> List[FireRisk]:
        results = self._collection.find({
            'city_id': city_id,
            "date_time": {"$gte": start, "$lte": end}
        })
        return [self._as_entity(doc) for doc in results]

    def find_nearby(
        self,
        lat: float,
        lng: float,
        radius: float,
        start: datetime,
        end: datetime
    ) -> List[FireRisk]:
        results = self._collection.aggregate([
            {
                '$geoNear': {
                    'near': {
                        'type': "Point",
                        'coordinates': [lng, lat]
                    },
                    'spherical': True,
                    'maxDistance': radius
                }
            },
            {
                '$match': {
                    'date_time': {
                        "$gte": start, "$lte": end
                    }
                }
            }
        ])
        return [self._as_entity(doc) for doc in results]

    def find_all(self, start: datetime, end: datetime) -> List[FireRisk]:
        results = self._collection.find({
            'date_time': {'$gte': start, '$lte': end}
        })
        return [self._as_entity(doc) for doc in results]

    def add(self, risk: FireRisk) -> FireRisk:
        result = self._collection.insert_one(risk.asdict())
        risk._id = result.inserted_id
        return risk
