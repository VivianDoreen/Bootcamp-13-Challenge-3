#flask_api provides an implementation of browsable APIs
import os
from flask import Flask
from config import application_config
#My app
from database import DatabaseConnection
app = Flask(__name__)
database_connection = DatabaseConnection()
database_connection.create_tables()
from app.views import users
from app.views import products
from app.views import sales