from domain.exception import EntityNotFound
from typing import List

from domain.model import ClimateRisk, ClimateRiskPeriod, City
from domain.repository import IClimateRiskRepository, ICityRepository


class ClimateRiskService:
    def __init__(
        self,
        risk_repo: IClimateRiskRepository,
        city_repo: ICityRepository
    ):
        self._risk_repo = risk_repo
        self._city_repo = city_repo

    def search(self, filter) -> List[ClimateRisk]:
        return self._risk_repo.search(**filter)

    def add_climate_risk(self, data: dict) -> ClimateRisk:
        city_name = data.pop('city_name')
        state = data.pop('state')
        city = self._city_repo.find_by_name(city_name, state)

        if city is None:
            raise EntityNotFound(City.__name__, (city_name, state))

        periods = [ClimateRiskPeriod(**it) for it in data.pop('periods')]
        data['periods'] = periods
        data['city'] = city._id
        risk = ClimateRisk.new(data)

        return self._risk_repo.add(risk)
