from flask import jsonify, request, render_template
from app import create_app

app = create_app('DevelopmentEnv')

@app.route('/')
def index():
    """
    Index route
    :return: 
    """
    return "<h2>Welcome to My Diary</h2>"