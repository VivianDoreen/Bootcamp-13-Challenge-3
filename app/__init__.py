#flask_api provides an implementation of browsable APIs
import os
from flask import Flask
from flask_cors import CORS
from config import application_config
#My app
from database import DatabaseConnection
app = Flask(__name__)
CORS(app)
database_connection = DatabaseConnection()
database_connection.create_tables()
# database_connection.create_admin()
from app.views import users
from app.views import products
from app.views import sales