#flask_api provides an implementation of browsable APIs
import os
from flask import Flask
from config import application_config
from database import DatabaseConnection

app = Flask(__name__)
from app.views import users
database_connection = DatabaseConnection()
database_connection.create_tables()

