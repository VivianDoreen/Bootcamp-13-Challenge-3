from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request,make_response, abort
from app import app
from app.models.product_model import CategoryModel, ProductModel
import uuid
from config import application_config
from app.decorators import generate_token, token_required
import datetime
from validation.utils_products import validate_input
from validation.utils_category import validate_input_category

env = application_config['DevelopmentEnv']

@app.route('/api/v1/categories', methods = ['GET'])
@token_required
def get_category(current_user):
    """
    This endpoint gets all categories 
    :return: 
    """
    category_list = CategoryModel.get_categories()
    if category_list == "Categories not available":
        return jsonify({'categories': category_list}), 404
    return jsonify({'categories': category_list}), 200

@app.route('/api/v1/categories/<int:search_id>', methods = ['GET'])
@token_required
def get_single_category(current_user, search_id):
    category = CategoryModel.get_category(search_id)
    if category == 'No category found, Check your id':
        return jsonify({'categories': category}), 404
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

    validate = validate_input_category(data)
    if validate != True:
        return jsonify({"message":validate_input_category(data)}),422

    create_category = CategoryModel(data['category'], current_user)
    return_create_category  = create_category.create_category()
    return jsonify({"message":return_create_category}), 201

@app.route('/api/v1/categories/<int:search_id>', methods = ['PUT'])
@token_required
def update_category(current_user, search_id):
    """
    This endpoint modifies a category
    :param version: 
    :param search_id: 
    :return: 
    """
    if (not request.json or not 'category'in request.json):
        abort(400)
    data = request.get_json() or {}
    validate = validate_input_category(data)
    if validate != True:
        return jsonify({"message":validate_input_category(data)}),422
    modify_category = CategoryModel.modify_category(search_id, data['category'])
    if modify_category == "No category found, Check your id":
        return jsonify({"message":modify_category}), 404
    if modify_category == "Category already exists":
        return jsonify({"message":modify_category}), 403
    return jsonify({"message":modify_category}), 201


@app.route('/api/v1/categories/<int:search_id>', methods = ['DELETE'])
@token_required
def delete_single_category(current_user, search_id):
    category_delete = CategoryModel.delete_category(search_id)
    if category_delete == 'No category found, please check your id':
        return jsonify({'Message': category_delete}), 404
    return jsonify({'Message': category_delete}), 200

@app.route('/api/v1/products', methods = ['GET'])
@token_required
def get_products(current_user):
    """
    This endpoint gets all products 
    :return: 
    """
    products_list = ProductModel.get_products()
    if products_list == "Products not available":
        return jsonify({'ProductsList': products_list}),404
    return jsonify({'ProductsList': products_list}),200

@app.route('/api/v1/products/<int:search_id>', methods = ['GET'])
@token_required
def get_single_product(current_user, search_id):
    product = ProductModel.get_product(search_id)
    if product ==  "No product found, Check your id":
        return jsonify({"message": product}),404
    return jsonify({'product': product}),200

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
    validate = validate_input(data)
    if validate != True:
        return jsonify({"message":validate_input(data)}),422

    total_price =  int(data['quantity']) * int(data['unit_price'])
    create_product = ProductModel(current_user, data['product_name'], 
                                                data['category'], data['quantity'],
                                                data['unit_price'], total_price)
    return_create_product  = create_product.create_product()
    if return_create_product == "product already exists":
        return jsonify({"message":return_create_product}),403
    if return_create_product == "category doesnot exist":
        return jsonify({"message":return_create_product}),404  
    if return_create_product == "quantity must be a positive number":
        return jsonify({"message":return_create_product}),422 
    if return_create_product == "unit price must be a positive number":
        return jsonify({"message":return_create_product}),422 
    return jsonify({"message":return_create_product}),201

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
    validate = validate_input(data)
    if validate != True:
        return jsonify({"message":validate_input(data)}),422
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
