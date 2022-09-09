from domain.service import FireRiskService, ClimateRiskService
from infrastructure import database
from infrastructure.repository import (
    CityRepository,
    FireRiskRepository,
    ClimateRiskRepository,
)
from .consumer import (
    FireRiskConsumer,
    ClimateRiskConsumer
)


def start_consumer(config):
    db = database.get_database(config.MONGODB_SETTINGS)
    kafka_config = {
        'bootstrap.servers': config.KAFKA_SERVER,
        'group.id': 'RISK',
        'enable.auto.commit': False,
        'auto.offset.reset': 'earliest'
    }

    city_repo = CityRepository(db)

    fire_risk_repo = FireRiskRepository(db)
    fire_risk_svc = FireRiskService(fire_risk_repo, city_repo)
    fire_risk_consumer = FireRiskConsumer(fire_risk_svc)
    fire_risk_consumer.start(kafka_config, 'FIRE_RISK')

    climate_risk_repo = ClimateRiskRepository(db)
    climate_risk_svc = ClimateRiskService(climate_risk_repo, city_repo)
    climate_risk_consumer = ClimateRiskConsumer(climate_risk_svc)
    climate_risk_consumer.start(kafka_config, 'CLIMATE_RISK')

    fire_risk_consumer.wait()
    climate_risk_consumer.wait()
