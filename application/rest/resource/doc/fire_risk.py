from flask import jsonify, request
from flask_restx import fields, Resource
from marshmallow import ValidationError
from domain.service.fire_risk import FireRiskService


def fire_riskblueprint(api, url_prefix, service: FireRiskService):

    ns = api.namespace(
        name='Fire_Risk',
        path=url_prefix,
        description='Fire_Risk route'
    )

    friskmodel = api.model('Fire_Risk', {
        'type': 'FeatureCollection',
        'features': [{
            "id": fields.String(description='Feature ID'),
            'type': 'Feature',
            "geometry": fields.Nested(
                {'type': 'Point', 'coordinates': [0, 0]},
                description='Risk Coordinates'
            ),
            "properties": {
                "_id": fields.String(description='ID'),
                "created_at": fields.DateTime(description='The creation date'),
                "updated_at": fields.DateTime(description='The update date'),
                "imported_id": fields.String(description='Imported ID'),
                "city_id": fields.String(description='City ID'),
                "date_time": fields.DateTime(
                    description='The date when occurred'),
                "biome": fields.String(description='Biome'),
                "days_without_rain": fields.Integer(
                    description='Number of Days without rain'),
                "rain_fallout": fields.String(description='Rain Fallout'),
                "risk": fields.String(description='Risk'),
                "satellite": fields.String(description='Satellite'),
                "geometry": fields.Nested(
                    {'type': 'Point', 'coordinates': [0, 0]},
                    description='Risk Coordinates'
                ),
            }
        }]
    })

    autherrormodel = api.model(
        'Error Unauthorized',
        {"message": fields.String()}
    )

    @ns.route('/fire_risk')
    class Fire_risk(Resource):
        @ns.doc('get_all')
        @ns.response(401, 'Unauthorized', model=autherrormodel)
        @ns.marshal_with(friskmodel, mask='*')
        def get(self):
            return jsonify(service.current_week())

    @ns.route('/cities/<string:city_id>/fire_risk')
    class Fire_risk_id(Resource):
        @ns.doc('get_fire_risk', params={'city_id': 'City id'})
        @ns.response(401, 'Unauthorized', model=autherrormodel)
        @ns.marshal_with(friskmodel, mask='*')
        def get(self, city_id):
            if city_id is None:
                city_id = request.args.get('city_id')

            if city_id is None:
                raise ValidationError({'city_id': 'Missing query param'})

            results = service.current_week_by_city(city_id)
            return jsonify(results)
