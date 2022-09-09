from flask import Flask
from flask_restx import Api
from application.rest.resource.doc import (
    cityblueprint,
    fire_riskblueprint,
    climate_riskblueprint
)


def register(app: Flask, url_prefix: str, services):
    api = Api(
        app,
        version='0.0.1',
        title='Risk Service',
        description='Risk Service Documentation',
        doc=url_prefix + '/doc'
    )

    cityblueprint(api, url_prefix, services[0])
    fire_riskblueprint(api, url_prefix, services[1])
    climate_riskblueprint(api, url_prefix, services[2])
