import re

pattern = re.compile(r"^[a-zA-Z]{2,50}(?:[\s_-]{1}[a-zA-Z]+)*$")
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
        "quantity": validate_quantity(data),
        "unit_price": validate_unit_price(data)
    }
    if validate_all['quantity'] != True:
        return validate_all['quantity']
    if validate_all['unit_price'] != True:
        return validate_all['unit_price']
    return True