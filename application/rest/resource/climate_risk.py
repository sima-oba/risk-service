from flask import request, jsonify, Blueprint
from domain.service import ClimateRiskService
from application.schema import ClimateRiskQuery


def get_blueprint(service: ClimateRiskService) -> Blueprint:
    bp = Blueprint('ClimateRisk', __name__, url_prefix='/climate_risk')
    query_schema = ClimateRiskQuery()

    @bp.get('/')
    def search_climate_risks():
        query = query_schema.load(request.args)
        climate_risks = service.search(query)

        return jsonify(climate_risks)

    return bp
