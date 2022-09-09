from pymongo.database import Database

from .city import CityRepository
from .fire_risk import FireRiskRepository
from .climate_risk import ClimateRiskRepository


__all__ = [
    'get_database',
    'CityRepository',
    'FireRiskRepository',
    'ClimateRiskRepository'
]


def init_database(db: Database):
    CityRepository(db).init_cities()
