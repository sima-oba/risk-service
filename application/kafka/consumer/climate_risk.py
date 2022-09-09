from application.schema import ClimateRiskSchema
from domain.service import ClimateRiskService
from .base import BaseConsumer
from ..error import error_handler


class ClimateRiskConsumer(BaseConsumer):
    def __init__(self, service: ClimateRiskService):
        super().__init__()
        self._service = service
        self._schema = ClimateRiskSchema()

    @error_handler
    def process(self, message: any):
        data = self._schema.loads(message.value())
        climate_risk = self._service.add_climate_risk(data)
        print(f'{message.key()}: processed climate_risk {climate_risk._id}')
