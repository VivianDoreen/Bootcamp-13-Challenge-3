from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request,make_response, abort
from app import app
from app.models.shopping_cart_model import ShoppingCartModel
from config import application_config
import uuid
from validation.utils_sales import validate_input
from app.decorators import generate_token, token_required
import datetime
env = application_config['DevelopmentEnv']

@app.route('/api/v1/shopping_cart', methods=['POST'])
@token_required
def add_sales_to_shopping_cart(current_user):
    """
    This endpoint adds a sale 
    :return: 
    """
    if (not request.json or not 'products_id'in request.json
                         or not 'quantity'in request.json
                         or not 'unit_price' in request.json
                         ):
        abort(400)
    data = request.get_json() or {}
    print(data)
    validate = validate_input(data)
    if validate != True:
        return jsonify({"message":validate_input(data)}),422
    total_price =  int(data['quantity']) * int(data['unit_price'])
    create_sale =ShoppingCartModel(current_user, data['products_id'],
                                                data['quantity'],
                                                data['unit_price'], total_price)
    return_create_sale  = create_sale.create_sales()
    if return_create_sale == "quantity must be a positive number":
        return jsonify({"message":return_create_sale}),422 
    if return_create_sale == "unit price must be a positive number":
        return jsonify({"message":return_create_sale}),422 
    if return_create_sale == "Sale unit price must be greater than the purchase unit price":
        return jsonify({"message":return_create_sale}),422 
    if return_create_sale == "Quantity must be less than the available quantity":
        return jsonify({"message":return_create_sale}),422 
    return jsonify({"message":return_create_sale}), 201

@app.route('/api/v1/shopping_cart', methods = ['GET'])
@token_required
def get_sales_from_shopping_cart(current_user):
    sales_list = ShoppingCartModel.get_sales()
    if sales_list =="Sales not available":
        return jsonify({'sales': sales_list}),404
    return jsonify({'sales': sales_list}), 200

