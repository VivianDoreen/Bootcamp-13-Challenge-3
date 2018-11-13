from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request,make_response, abort
from app import app
from app.models.product_model import CategoryModel, ProductModel
import uuid
from config import application_config
from validation import make_public_user, ValidateInput
from app.decorators import generate_token, token_required
import datetime
# app = create_app('DevelopmentEnv')
env = application_config['DevelopmentEnv']

@app.route('/api/v1/categories', methods = ['GET'])
@token_required
def get_category(current_user):
    """
    This endpoint gets all categories 
    :return: 
    """
    category_list = CategoryModel.get_categories()
    return jsonify({'categories List': category_list}), 200

@app.route('/api/v1/categories/<int:search_id>', methods = ['GET'])
@token_required
def get_single_category(current_user, search_id):
    category = CategoryModel.get_category(search_id)
    return jsonify({'categories': category}), 200

@app.route('/api/v1/categories', methods = ['POST'])
@token_required
def add_category(current_user):
    """
    This endpoint adds a category 
    :return: 
    """
    if (not request.json or not 'category'in request.json ):
            abort(400)

    data = request.get_json() or {}

    validate = ValidateInput.validate_category()
    if not validate(data):
        return make_response("Check your input values."
            "\n Name*"
            " \n\t\t\t\t- Required"
            "\n\t\t\t\t- Must be a string, "
            "\n\t\t\t\t- Minlength: 2 characters"
            "\n\t\t\t\t- Must begin with a character"
            ), 422

    create_category = CategoryModel(data['category'], current_user)
    return_create_category  = create_category.create_category()
    return jsonify({"message":return_create_category}), 201

@app.route('/api/v1/products', methods = ['GET'])
@token_required
def get_products(current_user):
    """
    This endpoint gets all products 
    :return: 
    """
    products_list = ProductModel.get_products()
    return jsonify({'Products List': products_list}), 200

@app.route('/api/v1/products/<int:search_id>', methods = ['GET'])
@token_required
def get_single_product(current_user, search_id):
    product = ProductModel.get_product(search_id)
    if product ==  "No product found, Check your id":
        return jsonify({"message": "No product found, Check your id"}), 404
    return jsonify({'Product': product}), 200

@app.route('/api/v1/products', methods = ['POST'])
@token_required
def add_products(current_user):
    """
    This endpoint adds a product 
    :return: 
    """
    if (not request.json or not 'product_name'in request.json
                         or not 'category'in request.json
                         or not 'quantity'in request.json
                         or not 'unit_price' in request.json
                         ):
        abort(400)

    data = request.get_json() or {}
    validate = ValidateInput.validate_product()
    if not validate(data):
        return make_response("Check your input values."
            "\n product Name* and category"
            " \n\t\t\t\t- Required"
            "\n\t\t\t\t- Must be a string, "
            "\n\t\t\t\t- Minlength: 2 characters"
            "\n\t\t\t\t- Must begin with a character"
            "\n quantity and unit price "
            "\n\t\t\t\t- Required"
            "\n\t\t\t\t- Must be an integer "
            "\n\t\t\t\t- Must begin with a number"
            ), 422

    total_price =  int(data['quantity']) * int(data['unit_price'])
    create_product = ProductModel(current_user, data['product_name'], 
                                                data['category'], data['quantity'],
                                                data['unit_price'], total_price)
    return_create_category  = create_product.create_product()
    if return_create_category == "Product already exists":
         return jsonify({"message":return_create_category}), 403
    return jsonify({"product successfully added":return_create_category}), 201

@app.route('/api/v1/products/<int:search_id>', methods = ['PUT'])
@token_required
def update_product(current_user, search_id):
    """
    This endpoint modifies a product
    :param version: 
    :param search_id: 
    :return: 
    """
    if (not request.json or not 'product_name'in request.json
                         or not 'category'in request.json
                         or not 'quantity'in request.json
                         or not 'unit_price' in request.json
                         ):
        abort(400)
    data = request.get_json() or {}
    validate = ValidateInput.validate_product()
    if not validate(data):
        return make_response("Check your input values."
            "\n product Name* and category"
            " \n\t\t\t\t- Required"
            "\n\t\t\t\t- Must be a string, "
            "\n\t\t\t\t- Minlength: 2 characters"
            "\n\t\t\t\t- Must begin with a character"
            "\n quantity and unit price "
            "\n\t\t\t\t- Required"
            "\n\t\t\t\t- Must be an integer "
            "\n\t\t\t\t- Must begin with a number"
            ), 422
    total_price =  int(data['quantity']) * int(data['unit_price'])
    modify_product = ProductModel.modify_product(search_id, data['product_name'], 
                                                data['category'], data['quantity'],
                                                data['unit_price'], total_price)
    if modify_product == "No product found, Check your id":
        return jsonify({"message":modify_product}), 404
    if modify_product == "product exists":
        return jsonify({"message":modify_product}), 403
    return jsonify({"message":modify_product}), 201
@app.route('/api/v1/products/<int:search_id>', methods = ['DELETE'])
@token_required
def delete_product(current_user, search_id):
    product = ProductModel.delete_product(search_id)
    return jsonify({'Message': product}), 200
