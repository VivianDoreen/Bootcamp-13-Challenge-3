import re

pattern = re.compile(r"^[a-zA-Z]{2,50}(?:[\s_-]{1}[a-zA-Z]+)*$")

def product_validate_name(data):
    name = data['product_name']
    if len(name) < 1:
        return "Product name is required"
    if not isinstance(name, str):
        return "product input must be a string"
    if not pattern.match(name):
        return "product must begin with a letter"
    return True

def product_validate_category(data):
    name = data['category']
    if len(name) < 1:
        return "Category name is required"
    if not isinstance(name, str):
        return "category input must be a string"
    if not pattern.match(name):
        return "category must begin with a letter"
    return True

def validate_quantity(data):
    name = data['quantity']
    if name == "":
        return "Quantity is required"
    return True

def validate_unit_price(data):
    name = data['unit_price']
    if name == "":
        return "Unit price is required"
    return True

def validate_input(data):
    validate_all = {
        "product_name": product_validate_name(data),
        "product_category": product_validate_category(data),
        "quantity": validate_quantity(data),
        "unit_price": validate_unit_price(data)
    }
    if validate_all['product_name'] != True:
        return validate_all['product_name']
    if validate_all['product_category'] != True:
        return validate_all['product_category']
    if validate_all['quantity'] != True:
        return validate_all['quantity']
    if validate_all['unit_price'] != True:
        return validate_all['unit_price']
    return True