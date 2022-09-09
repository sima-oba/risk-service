from typing import List
from pymongo.database import Database

from domain.model.city import City, CITIES
from domain.repository import ICityRepository


class CityRepository(ICityRepository):
    def __init__(self, db: Database):
        self._collection = db["cities"]

    def init_cities(self):
        for city in CITIES:
            doc = self._collection.find_one({'geoid': city['geoid']})

            if doc is None:
                doc = City.new(city).asdict()
                self._collection.insert_one(doc)

    def _with_filter(self, filter: dict) -> City:
        result = self._collection.find_one(filter)
        return City(**result) if result else None

    def find_all(self) -> List[City]:
        return [City(**it) for it in self._collection.find()]

    def find_by_id(self, id: str) -> City:
        return self._with_filter({'_id': id})

    def find_by_geoid(self, geoid: str) -> City:
        return self._with_filter({'geoid': geoid})

    def find_by_name(self, city: str, state: str) -> City:
        return self._with_filter({
            "name": {'$regex': f'^{city}', '$options': '-i'},
            "state": {'$regex': f'^{state}', '$options': '-i'}
        })

    def add(self, city: City) -> City:
        result = self._collection.insert_one(city.asdict())
        city._id = result.inserted_id
        return city
