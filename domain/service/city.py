from typing import List

from domain.model import City
from domain.repository import ICityRepository


class CityService:
    def __init__(self, repo: ICityRepository):
        self._repo = repo

    def get_all(self) -> List[City]:
        return self._repo.find_all()

    def save(self, data: dict) -> City:
        city = self._repo.find_by_geoid(data['geoid'])

        if city is not None:
            return city

        return self._repo.add(City.new(data))
