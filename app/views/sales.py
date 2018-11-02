from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request,make_response, abort
from app import create_app
from app.models.sales_model import SaleModel
import uuid
from validation import make_public_user
from app.decorators import generate_token, token_required
import datetime
app = create_app('DevelopmentEnv')

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
    print(data)
    total_price =  int(data['quantity']) * int(data['unit_price'])
    create_sale =SaleModel(current_user, data['products_id'],
                                                data['quantity'],
                                                data['unit_price'], total_price)
    return_create_sale  = create_sale.create_sales()
    return jsonify({"message":return_create_sale}), 201





