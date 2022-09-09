from flask import Blueprint, jsonify

from domain.service import FireRiskService
from ...schema import utils


def get_blueprint(service: FireRiskService) -> Blueprint:
    bp = Blueprint('FireRisk', __name__, url_prefix='/fire_risk')

    @bp.get('/')
    def get_current_week_firerisk():
        fire_risk = service.current_week()
        features = utils.export_feature_collection(fire_risk)

        return jsonify(features)

    return bp
