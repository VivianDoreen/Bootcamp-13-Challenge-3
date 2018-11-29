import re

pattern = re.compile(r"^[a-zA-Z]{2,50}(?:[\s_-]{1}[a-zA-Z]+)*$")

def category_validate_name(data):
    name = data['category']
    if len(name) < 1:
        return "category name is required"
    if not isinstance(name, str):
        return "category input must be a string"
    if not pattern.match(name):
        return "category must begin with a letter"
    return True

def validate_input_category(data):
    validate_all = {
        "category_name": category_validate_name(data)
    }
    if validate_all['category_name'] != True:
        return validate_all['category_name']
    return True