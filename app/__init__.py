#flask_api provides an implementation of browsable APIs
import os
from flask import Flask
from config import application_config
from database import DatabaseConnection

app = Flask(__name__)


def create_app(config_name):
    APP_ROOT = os.path.dirname(app.instance_path)
    app.config.from_object(application_config[config_name])
    app.config.from_pyfile(APP_ROOT+'/config.py')
    return app