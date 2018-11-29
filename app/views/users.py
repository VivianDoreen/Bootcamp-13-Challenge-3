from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request,make_response, abort
from validation.utils_users import validate_input, validate_input_login
from config import application_config
from app import app
from app.models.user_model import UserModel
import uuid
from app.decorators import generate_token, token_required
import error_handler
import datetime
import os

app.config.from_object('config.DevelopmentEnvironment')

@app.route('/')
def index():
    """
    Index route
    :return: 
    """
    return "<h2>Welcome to ManagerStore</h2>"

@app.route('/api/v1/users', methods = ['GET'])
@token_required
def get_users(current_user):
    users_list = UserModel.get_users()
    if users_list == "No Users":
        return jsonify({'users': users_list}), 404
    return jsonify({'users': users_list}), 200

@app.route('/api/v1/users/<int:search_id>', methods = ['GET'])
@token_required
def get_user(current_user, search_id):
    user = UserModel.get_user_by_id(current_user)
    if user['role'] != "admin":
        return jsonify({"message":"You are not authorised to view this function"}), 401  
    user = UserModel.get_user_by_id(search_id)
    if user == "No such user, check id":
        return jsonify({'user':user}), 404
    return jsonify({'user':user}), 200

@app.route('/api/v1/auth/signup', methods = ['POST'])
@token_required
def create_user(current_user):
    if (not request.json or not 'name'in request.json
                         or not 'email' in request.json
                         or not 'password' in request.json
                         or not 'confirm_password' in request.json
                         or not 'role' in request.json
                         ):
        return jsonify({'message':'Wrong params for json'}), 400

    data = request.get_json() or {}
    validate = validate_input(data)
    if validate != True:
        return jsonify({"message":validate_input(data)}),422

    if data['password'] != data['confirm_password']:
        return jsonify({'message':'Passwords do not match'}), 422
    password =generate_password_hash(data['password'])
    register_user = UserModel.register_user(data['name'], data['email'], password, data['role'])
    if register_user == "Email already exists":
            return jsonify({"message":register_user}), 403
    return jsonify({"message":register_user}), 201
@app.route('/api/v1/users/<search_id>', methods = ['PUT'])
@token_required
def update_user(current_user, search_id):
    """
    This endpoint modifies a user
    :param version: 
    :param search_id: 
    :return: 
    """
    data = request.get_json() or {}
    validate = validate_input(data)
    if validate != True:
        return jsonify({"message":validate_input(data)}),422
    edit_user = UserModel.modify_user(search_id,data['name'], data['email'],
                                      data['password'], data['role']
                                     )
    if edit_user == "No such user, check id":
        return jsonify({'message': edit_user}), 404
    if edit_user == "email already exists":
        return jsonify({'message': edit_user}), 403
    return jsonify({'message': edit_user}), 201
@app.route('/api/v1/users/<int:search_id>', methods = ['DELETE'])
@token_required
def delete_user(current_user, search_id):
    user = UserModel.delete_user(search_id)
    if user == "No such user, check id":
        return jsonify({'user': user}), 404
    return jsonify({'user': user}), 200

@app.route('/api/v1/auth/login',methods=['POST'])
def login():
    if (not request.json or not 'email' in request.json
                         or not 'password' in request.json):
        return jsonify({"message":"wrong params"})
    data = request.get_json() or {}
    validate = validate_input_login(data)
    if validate != True:
        return jsonify({"Error":validate_input_login(data)}),422
    user = UserModel.check_if_is_valid_user(data['email'])

    if user == "user not found":
        return jsonify({'message':'could not verify the user'}), 401

    if not check_password_hash(user[3], data['password']):
        return jsonify({"message":"Wrong password"}), 404

    return jsonify({
                'id':user[0],
                'name':user[1],
                'role':user[4],
                'email':user[2],
                'message': "Login successful",
                'x-access-token':generate_token(user[0])
                }),200
