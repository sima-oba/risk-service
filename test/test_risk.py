import pytest
from uuid import uuid4
from datetime import datetime

from application import rest, kafka
from infrastructure import database
from . import TestConfig as config


API_PREFIX = rest.server.API_PREFIX


def mock_kafka():
    kafkaresult = kafka.start_consumer(config)
    return kafkaresult


def now():
    return datetime.utcnow().replace(second=0, microsecond=0)


@pytest.fixture
def clientinstance():
    app = rest.server.create_server(config)
    return app.test_client()


@pytest.fixture(autouse=True)
def db():
    db = database.get_database(config.MONGODB_SETTINGS)

    for collection in db.collection_names(False):
        db.drop_collection(collection)

    return db


def test_gunicorn_app():
    serverresult = rest.create_server(config)
    assert rest.GunicornApplication is not None
    assert serverresult is not None


def test_kafka_consumer(mocker):
    mocker.patch('application.kafka.start_consumer', return_value=1)
    assert mock_kafka() == 1


def test_city_route(clientinstance, db):
    client = clientinstance
    url = API_PREFIX + '/cities'
    collection = db['cities']

    expected = [
        {
            '_id': str(uuid4()),
            'created_at': None,
            'updated_at': None,
            'geoid': '1600303',
            'name': 'Macapá',
            'state': 'AP'
        }
    ]

    collection.insert_many(expected)
    response = client.get(url)
    assert response.status_code == 200
    assert response.get_json() == expected


def test_fire_route(clientinstance, db):
    url = API_PREFIX + '/fire_risk'
    collection = db['fire_risk']

    data = {
        '_id': str(uuid4()),
        'created_at': None,
        'updated_at': None,
        'imported_id': 123,
        'city_id': 123,
        'date_time': now(),
        'biome': 'Cerrado',
        'days_without_rain': 123,
        'rain_fallout': 'poucas',
        'risk': 'elevado',
        'satellite': 'xyz',
        'geometry': {
            'type': 'Point',
            'coordinates': [0, 0]
        }
    }

    collection.insert_one(data)
    data['date_time'] = data['date_time'].isoformat()

    expected = {
        'type': 'FeatureCollection',
        'features': [
            {
                'id': 0,
                'type': 'Feature',
                'geometry': data.pop('geometry'),
                'properties': data
            }
        ]
    }

    response = clientinstance.get(url)
    assert response.status_code == 200
    assert response.get_json() == expected


def test_climate_route(clientinstance, db):
    client = clientinstance
    url = API_PREFIX + '/climate_risk'
    collection = db['climate_risk']

    expected = {
        '_id': str(uuid4()),
        'created_at': None,
        'updated_at': None,
        'city_id': str(uuid4()),
        'date_time': now(),
        'harvest': 'milho',
        'ordinance': '123',
        'crop': 'soja',
        'cycle': '2',
        'soil': 'barroso',
        'periods': [{
            'period': 0,
            'risk_percent': 0
        }]
    }

    collection.insert_one(expected)
    expected['date_time'] = expected['date_time'].isoformat()

    response = client.get(url)
    assert response.status_code == 200
    assert response.get_json() == [expected]
