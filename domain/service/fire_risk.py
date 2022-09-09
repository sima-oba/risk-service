from typing import List
from datetime import datetime, timedelta

from domain.model import FireRisk, City, Point
from domain.repository import IFireRiskRepository, ICityRepository
from domain.exception import EntityNotFound


class FireRiskService:
    def __init__(
        self, fire_repo: IFireRiskRepository, city_repo: ICityRepository
    ):
        self._fire_repo = fire_repo
        self._city_repo = city_repo

    def _new_week_interval(self):
        start = datetime.utcnow() - timedelta(days=2)
        end = start + timedelta(days=7)

        return start, end

    def current_week_by_city(self, city_id: str) -> List[FireRisk]:
        city = self._city_repo.find_by_id(city_id)

        if city is None:
            raise EntityNotFound(City.__name__, f'_id {city_id}')

        start, end = self._new_week_interval()
        return self._fire_repo.find_by_city(city._id, start, end)

    def current_week_nearby(
        self,
        lat: float,
        lng: float,
        radius: float
    ) -> List[FireRisk]:
        start, end = self._new_week_interval()
        return self._fire_repo.find_nearby(lat, lng, radius, start, end)

    def current_week(self) -> List[FireRisk]:
        start, end = self._new_week_interval()
        return self._fire_repo.find_all(start, end)

    def add_fire_risk(self, data: dict) -> FireRisk:
        geoid = data.pop('geoid')
        lat_lng = (data.pop('longitude'), data.pop('latitude'))
        data['geometry'] = Point(coordinates=lat_lng)
        data['city_id'] = geoid

        return self._fire_repo.add(FireRisk.new(data))
