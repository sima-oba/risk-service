from os import environ, path, mkdir
from dotenv import load_dotenv

import logging
import logging.config


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    LOG_DIR = environ.get('LOG_DIR', './logs')
    INTROSPECTION_URI = environ.get('INTROSPECTION_URI')
    KAFKA_SERVER = environ.get('KAFKA_SERVER')
    MONGODB_SETTINGS = {
        'db': environ.get('MONGO_DB'),
        'host': environ.get('MONGO_HOST'),
        'port': int(environ.get('MONGO_PORT')),
        'username': environ.get('MONGO_USER'),
        'password': environ.get('MONGO_PASSWORD'),
        'authentication_source': 'admin',
    }

    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_ENV = environ.get('FLASK_ENV')


# Set up log
if not path.exists(Config.LOG_DIR):
    mkdir(Config.LOG_DIR)

if not path.isdir(Config.LOG_DIR):
    raise ValueError(f'{Config.LOG_DIR} is not a directory')

logging.config.fileConfig('./logging.ini')
