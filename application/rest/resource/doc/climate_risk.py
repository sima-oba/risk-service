from flask import jsonify, request
from flask_restx import fields, Resource
from application.schema.climate_risk import ClimateRiskQuery
from domain.service.climate_risk import ClimateRiskService


def climate_riskblueprint(api, url_prefix, service: ClimateRiskService):

    ns = api.namespace(
        name='Climate_risk',
        path=url_prefix,
        description='Climate_risk route'
    )

    criskmodel = api.model('Climate_Risk', {
        "_id": fields.String(description='ID'),
        "created_at": fields.DateTime(description='The creation date'),
        "updated_at": fields.DateTime(description='The update date'),
        "city_id": fields.String(description='City ID'),
        "date_time": fields.DateTime(description='The date when occurred'),
        "harvest": fields.String(description='Harvest'),
        "ordinance": fields.String(description='Ordinance'),
        "crop": fields.String(description='Crop'),
        "cycle": fields.String(description='Cycle'),
        "soil": fields.String(description='Soil'),
        "periods": [{
            "period": fields.Integer(),
            "risk_percent": fields.Integer(),
        }]
    })

    autherrormodel = api.model(
        'Error Unauthorized',
        {"message": fields.String()}
    )

    @ns.route('/climate_risk')
    class Climate_risk(Resource):
        @ns.doc('get_all')
        @ns.response(401, 'Unauthorized', model=autherrormodel)
        @ns.marshal_with(criskmodel, mask='*')
        def get(self):
            schema_query = ClimateRiskQuery()
            query = schema_query.load(request.args.to_dict())
            climate_risks = service.search(query)
            return jsonify(climate_risks)
