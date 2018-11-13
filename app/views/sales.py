from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request,make_response, abort
from app import app
from validation import ValidateInput
from app.models.sales_model import SaleModel
from config import application_config
import uuid
from validation import make_public_user
from app.decorators import generate_token, token_required
import datetime
# app = create_app('DevelopmentEnv')
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
    validate = ValidateInput.validate_sale()
    if not validate(data):
        return make_response("Check your input values."
            "\n products_id, quantity and unit price "
            "\n\t\t\t\t- Required"
            "\n\t\t\t\t- Must be an integer "
            "\n\t\t\t\t- Must begin with a number"
            ), 422

    total_price =  int(data['quantity']) * int(data['unit_price'])
    create_sale =SaleModel(current_user, data['products_id'],
                                                data['quantity'],
                                                data['unit_price'], total_price)
    return_create_sale  = create_sale.create_sales()
    return jsonify({"message":return_create_sale}), 

@app.route('/api/v1/sales', methods = ['GET'])
@token_required
def get_sales(current_user):
    sales_list = SaleModel.get_sales()
    return jsonify({'Sales': sales_list}), 200






