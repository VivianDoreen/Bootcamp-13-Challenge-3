from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request,make_response, abort
from app import app
# from validation import ValidateInput
from app.models.sales_model import SaleModel
from config import application_config
import uuid
from validation.utils_sales import validate_input
from app.decorators import generate_token, token_required
import datetime
env = application_config['DevelopmentEnv']

@app.route('/api/v1/sales', methods=['POST'])
@token_required
def add_sales(current_user):
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
    validate = validate_input(data)
    if validate != True:
        return jsonify({"message":validate_input(data)}),422
    total_price =  int(data['quantity']) * int(data['unit_price'])
    create_sale =SaleModel(current_user, data['products_id'],
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

@app.route('/api/v1/sales', methods = ['GET'])
@token_required
def get_sales(current_user):
    sales_list = SaleModel.get_sales()
    if sales_list =="Sales not available":
        return jsonify({'sales': sales_list}),404
    return jsonify({'sales': sales_list}), 200

@app.route('/api/v1/sales/<int:search_id>', methods = ['GET'])
@token_required
def get_single_sale(current_user, search_id):
    sale = SaleModel.get_single_sale(search_id)
    if sale ==  "No sale found, Check your id":
        return jsonify({"message": sale}), 404
    return jsonify({'sale': sale}), 200

@app.route('/api/v1/sales/total_sales', methods = ['GET'])
@token_required
def get_total_sale_by_attendant(current_user):
    total_sale = SaleModel.get_total_sale_by_attendant(current_user)
    if total_sale ==  "No sale made":
        return jsonify({"message": total_sale}), 404
    return jsonify({'total_sales': total_sale}), 200

@app.route('/api/v1/sales/<int:search_id>', methods = ['PUT'])
@token_required
def update_sales(current_user, search_id):
    """
    This endpoint modifies a sale
    :param version: 
    :param search_id: 
    :return: 
    """
    if (not request.json or not 'products_id'in request.json
                        or not 'quantity'in request.json
                        or not 'unit_price' in request.json
                        ):
        abort(400)
    data = request.get_json() or {}
    validate = validate_input(data)
    if validate != True:
        return jsonify({"message":validate_input(data)}),422

    total_price =  int(data['quantity']) * int(data['unit_price'])
    modify_sale = SaleModel.modify_sale(search_id,
                                        data['products_id'],
                                        data['quantity'],
                                        data['unit_price'],
                                        total_price)
    if modify_sale == "No sale found, Check your id":
        return jsonify({"message":modify_sale}), 404
    return jsonify({"message":modify_sale}), 201

@app.route('/api/v1/sales/<int:search_id>', methods = ['DELETE'])
@token_required
def delete_sale(current_user, search_id):
    sale = SaleModel.delete_sale(search_id)
    if sale == "No sale found, Check your id":
        return jsonify({'message': sale}), 404
    return jsonify({'message': sale}), 200