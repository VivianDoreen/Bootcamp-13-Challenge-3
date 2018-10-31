from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request,make_response, abort
from app import create_app
from app.models.user_model import UserModel
import uuid
from validation import make_public_user
from app.decorators import generate_token, token_required
import datetime
app = create_app('DevelopmentEnv')
@app.route('/')
def index():
    """
    Index route
    :return: 
    """
    return "<h2>Welcome to My Diary</h2>"

@app.route('/api/v1/users', methods = ['GET'])
@token_required
def get_users(current_user):
    users_list = UserModel.get_users()
    return jsonify({'Users of ManagerStore': [make_public_user(user) for user in users_list]}), 200

@app.route('/api/v1/users/<public_id>', methods = ['GET'])
@token_required
def get_user(current_user, public_id):
    user = UserModel.get_user_by_id(public_id)
    if (user[0]['admin']) != False:
        return jsonify({"message":"You are not authorised to view this function"}), 401  
    return jsonify({'User':user}), 200

@app.route('/api/v1/users', methods = ['POST'])
@token_required
def create_user(current_user):
    if (not request.json or not 'name'in request.json
                         or not 'username' in request.json
                         or not 'password' in request.json
                         or not 'c_password' in request.json
                         or not 'email' in request.json
                         or not 'address' in request.json
                         or not 'gender' in request.json):
        abort(400)

    data = request.get_json() or {}
    if data['password'] != data['c_password']:
        return jsonify({'message':'Passwords do not match'}), 422
    hashed_password = generate_password_hash(data['password'], method='sha256')
    public_id = str(uuid.uuid4())
    name = data['name']
    username = data['username']
    email = data['email']
    address = data['address']
    gender = data['gender']
    admin = False
    register_user = UserModel.register_user(public_id, name, username, hashed_password, email, address, gender, admin)
    return register_user, 201
@app.route('/api/v1/users/<public_id>', methods = ['PUT'])
@token_required
def update_user(current_user,public_id,search_id):
    """
    This endpoint modifies a user
    :param version: 
    :param search_id: 
    :return: 
    """

    if (not request.json or not 'name'in request.json
                         or not 'username' in request.json
                         or not 'password' in request.json
                         or not 'email' in request.json
                         or not 'address' in request.json
                         or not 'gender' in request.json
                         or not 'admin' in request.json
                         ):
        abort(400)
    data = request.get_json() or {}
    name = data['name']
    username = data['username']
    password = data['password']
    email = data['email']
    address = data['address']
    gender = data['gender']
    admin = data['admin']
    print(data)
    print(search_id)
    edit_user = UserModel.modify_user(search_id,name, username,
                                      password, email, address,
                                      gender, admin
                                    )
    return jsonify({'message': edit_user}), 200

@app.route('/api/v1/login',methods=['POST'])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('could not verify auth input', 401, {'www-Authenticate':'Basic realm="Login required!"'})
    user = UserModel.check_if_is_valid_user(auth['username'])
    print(user[2])
    if not user:
        return make_response('could not verify the user', 401, {'www-Authenticate':'Basic realm="Login required!"'})
    if check_password_hash(user[4], auth['password']):
        return jsonify({
                    'status': "Login successful",
                    "token":generate_token(user[1]),
                    }),200
    return make_response('could not verify the password', 401, {'www-Authenticate':'Basic realm="Login required!"'})
