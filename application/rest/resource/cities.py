from flask import jsonify, Blueprint
from domain.service import CityService


def get_blueprint(service: CityService) -> Blueprint:
    bp = Blueprint('Cities', __name__, url_prefix='/cities')

    @bp.get('/')
    def get_all_cities():
        return jsonify(service.get_all())

    return bp
