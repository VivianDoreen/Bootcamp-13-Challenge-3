# from app.views.users import app
from flask import Flask
from app.views.users import app
import os
# print(app.config.from_object(os.environ['APP_SETTINGS']))


if __name__ == '__main__':
    app.run( port=8080)