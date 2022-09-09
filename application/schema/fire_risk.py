from marshmallow import Schema, fields, EXCLUDE, post_load


class _FireRisktProperties(Schema):
    class Meta:
        unknown = EXCLUDE
    imported_id = fields.String(data_key='id', required=True)
    date_time = fields.DateTime(data_key='data_hora_gmt', required=True)
    biome = fields.String(data_key='bioma', missing=None)
    latitude = fields.String(required=True)
    longitude = fields.String(required=True)
    geoid = fields.String(data_key='municipio_id', required=True)
    rain_fallout = fields.String(data_key='precipitacao', missing=None)
    risk = fields.String(data_key='risco_fogo', missing=None)
    satellite = fields.String(data_key='satelite', missing='unknown')
    days_without_rain = fields.String(
        data_key='numero_dias_sem_chuva', missing=None
    )

    @post_load
    def format(self, data: dict, **kwargs):
        data['latitude'] = float(data['latitude'])
        data['longitude'] = float(data['longitude'])
        data['geoid'] = data['geoid']
        return data


class _FireRiskFeature(Schema):
    class Meta:
        unknown = EXCLUDE
    properties = fields.Nested(_FireRisktProperties, required=True)


class FireRiskSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    features = fields.List(fields.Nested(_FireRiskFeature), required=True)

    @post_load
    def format(self, data: dict, **kwargs):
        return [feat['properties'] for feat in data['features']]
