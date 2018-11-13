#flask_api provides an implementation of browsable APIs
import os
from flask import Flask
from config import application_config
from database import DatabaseConnection
# from database import create_tables, connect_db

app = Flask(__name__)
from app.views import users
# print(users.env)
database_connection = DatabaseConnection()
database_connection.create_tables()
# print(database_connection.db)
# print(database_connection.co)
# print(database_connection.get_ev)
# print(application_config['DevelopmentEnv'].DATABASE)
# print(application_config['TestingEnv'].DATABASE)
