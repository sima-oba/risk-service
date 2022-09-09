from flask import Flask, Blueprint
from flask_cors import CORS
from infrastructure import database
from domain.service import (
    CityService,
    FireRiskService,
    ClimateRiskService
)
from infrastructure.repository import (
    CityRepository,
    FireRiskRepository,
    ClimateRiskRepository
)
from .error import error_bp
from .encoder import CustomJsonEncoder
from .resource import cities, fire_risk, climate_risk
from .security import Authorization, Role


API_PREFIX = '/api/v1/risk'


def create_server(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['JSON_SORT_KEYS'] = False
    app.url_map.strict_slashes = False
    app.json_encoder = CustomJsonEncoder
    app.register_blueprint(error_bp)

    db = database.get_database(config.MONGODB_SETTINGS)
    CORS(app)
    is_auth_enabled = app.config['FLASK_ENV'] != 'development'
    auth = Authorization(config.INTROSPECTION_URI, is_auth_enabled)
    auth.grant_role_for_any_request(Role.ADMIN, Role.READ_RISK)
    auth.require_authorization_for_any_request(app)

    root_bp = Blueprint('Root', __name__, url_prefix=API_PREFIX)

    city_repo = CityRepository(db)
    city_svc = CityService(city_repo)
    city_bp = cities.get_blueprint(city_svc)
    root_bp.register_blueprint(city_bp)

    fire_risk_repo = FireRiskRepository(db)
    fire_risk_svc = FireRiskService(fire_risk_repo, city_repo)
    fire_risk_bp = fire_risk.get_blueprint(fire_risk_svc)
    root_bp.register_blueprint(fire_risk_bp)

    climate_risk_repo = ClimateRiskRepository(db)
    climate_risk_svc = ClimateRiskService(climate_risk_repo, city_repo)
    climate_risk_bp = climate_risk.get_blueprint(climate_risk_svc)
    root_bp.register_blueprint(climate_risk_bp)

    app.register_blueprint(root_bp)

    return app
