from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request,make_response, abort
from app import create_app
from app.models.product_model import CategoryModel, ProductModel
import uuid
from validation import make_public_user
from app.decorators import generate_token, token_required
import datetime
app = create_app('DevelopmentEnv')

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
    if (not request.json or not 'cat_name'in request.json):
        abort(400)

    data = request.get_json() or {}
    create_category = CategoryModel(data['cat_name'], current_user)
    return_create_category  = create_category.create_category()
    return return_create_category, 201

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
    return jsonify({'Product': product}), 200

@app.route('/api/v1/products', methods = ['POST'])
@token_required
def add_products(current_user):
    """
    This endpoint adds a product 
    :return: 
    """
    if (not request.json or not 'pdt_name'in request.json
                         or not 'pdt_description'in request.json
                         or not 'cat_name'in request.json):
        abort(400)

    data = request.get_json() or {}
    create_product = ProductModel(current_user, data['pdt_name'], data['pdt_description'], data['cat_name'])
    return_create_category  = create_product.create_product()
    return return_create_category, 201

@app.route('/api/v1/products/<int:search_id>', methods = ['PUT'])
@token_required
def update_product(current_user, search_id):
    """
    This endpoint modifies a product
    :param version: 
    :param search_id: 
    :return: 
    """
    if (not request.json or not 'pdt_name'in request.json 
                         or not 'pdt_description'in request.json
                         or not 'cat_name'in request.json):
            abort(400)

    data = request.get_json() or {}
    modify_product  = ProductModel.modify_product(search_id, data['pdt_name'], data['pdt_description'], data['cat_name'])
    return modify_product, 201
@app.route('/api/v1/products/<int:search_id>', methods = ['DELETE'])
@token_required
def delete_product(current_user, search_id):
    product = ProductModel.delete_product(search_id)
    return jsonify({'Message': product}), 200
