from marshmallow import Schema, fields, EXCLUDE, post_load


class _StateSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    abbreviation = fields.String(data_key='sigla', required=True)


class _MesoregionSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    state = fields.Nested(_StateSchema, data_key='UF', required=True)


class _MicroregionSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    mesoregion = fields.Nested(_MesoregionSchema, data_key='mesorregiao')


class CitySchema(Schema):
    class Meta:
        unknown = EXCLUDE
    geoid = fields.Integer(data_key='id', required=True)
    name = fields.String(data_key='nome', required=True)
    microregion = fields.Nested(
        _MicroregionSchema, data_key='microrregiao', required=True
    )

    @post_load
    def format(self, data: dict, **kwargs):
        microregion = data.pop('microregion')
        data['state'] = microregion['mesoregion']['state']['abbreviation']
        return data
