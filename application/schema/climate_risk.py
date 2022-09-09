from datetime import datetime
from marshmallow import Schema, fields, EXCLUDE, post_load, validate


class ClimateRiskSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    harvest = fields.String(data_key='Safra', required=True)
    city_name = fields.String(data_key='Município', required=True)
    state = fields.String(data_key='UF', required=True)
    crop = fields.String(data_key='Cultura', required=True)
    cycle = fields.String(data_key='Ciclo', required=True)
    soil = fields.String(data_key='Solo', required=True)
    ordinance = fields.String(
        data_key='Portaria',
        required=True,
        validate=validate.Regexp(
            r'^(\w+)\.(\d+)_(de_){0,1}(\d{2}-){2}(\d){4}$'
        )
    )
    periods = fields.List(fields.Integer(required=True), required=True)

    @post_load
    def format(self, data: dict, **kwargs):
        data['ordinance'] = "_".join(data['ordinance'].split("_de_"))
        ordinance, date_time = data.pop('ordinance').split('_')
        data['ordinance'] = int(ordinance.split('.')[1])
        data['date_time'] = datetime.strptime(date_time, '%d-%m-%Y')
        data['periods'] = [
            {'period': index + 1, 'risk_percent': value}
            for index, value in enumerate(data.pop('periods'))
        ]

        return data


class ClimateRiskQuery(Schema):
    year = fields.Integer()
    city_id = fields.String()
    ordinance = fields.Integer()
    crop = fields.String()
    cycle = fields.String()
    soil = fields.String()
