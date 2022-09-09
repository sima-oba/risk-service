from application.schema import FireRiskSchema
from domain.service import FireRiskService
from .base import BaseConsumer
from ..error import error_handler


class FireRiskConsumer(BaseConsumer):
    def __init__(self, service: FireRiskService):
        super().__init__()
        self._service = service
        self._schema = FireRiskSchema()

    @error_handler
    def process(self, message: any):
        data = self._schema.loads(message.value())

        for it in data:
            fire_risk = self._service.add_fire_risk(it)
            print(f'{message.key()}: processed fire_risk {fire_risk._id}')
