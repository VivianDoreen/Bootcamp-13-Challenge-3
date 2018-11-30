import datetime
import jwt
from flask import Flask, request, jsonify
from functools import wraps
from app.models.user_model import UserModel

app = Flask(__name__)
app.config['SECRETE_KEY'] = "This is a secrete key"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({"message":"token is missing"}),401
        try:
            data = jwt.decode(token, app.config['SECRETE_KEY'], algorithms=['HS256'])
            current_user = data['sub']
            user = UserModel.get_user_by_id(current_user)
            if user['role'] != "admin":
                current_user = data['sub']
            if user['role'] != "store_attendant":
                current_user = data['sub']
        except:
            return jsonify({"message":"Your session has expired, please login again"}),401
        return f(current_user, *args, **kwargs)
    return decorated

def generate_token(user):
    payload = {
            "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat":datetime.datetime.utcnow(),
            "sub":user
            }
    token = jwt.encode( payload,app.config['SECRETE_KEY'], algorithm='HS256').decode("utf-8")
    return token