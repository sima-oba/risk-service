from flask import jsonify, request
from application.rest.resource import (
    cities,
    fire_risk,
    climate_risk
)
from domain.service import (
    CityService,
    FireRiskService
)
from application.schema.city import CitySchema


def configure_routes_cities(app, service: CityService):
    city_bp = cities.get_blueprint(service)
    app.register_blueprint(city_bp)
    schema = CitySchema()

    @app.route('/cities', methods=['POST'])
    def post_city():
        data = schema.load(request.json, many=True)
        cities = [service.save(it) for it in data]
        return jsonify(cities)


def configure_routes_fire(app, service: FireRiskService):
    fire_bp = fire_risk.get_blueprint(service)
    app.register_blueprint(fire_bp)


def configure_routes_climate(app, service: CityService):
    climate_bp = climate_risk.get_blueprint(service)
    app.register_blueprint(climate_bp)
