import re

pattern = re.compile(r"^[a-zA-Z]{2,50}(?:[\s_-]{1}[a-zA-Z]+)*$")
pattern_email = re.compile(r'[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]{2,4}')
pattern_password = re.compile(r'^[a-zA-Z0-9]{5,100}.*[\s.]*$')
def user_validate_name(data):
    name = data['name']
    if len(name) < 1:
        return "name is required"
    if not isinstance(name, str):
        return "name input must be a string"
    if not pattern.match(name):
        return "name must begin with a letter"
    return True

def user_validate_email(data):
    email = data['email']
    if len(email) < 1:
        return "email is required"
    if not isinstance(email, str):
        return "email input must be a string"
    if not pattern_email.match(email):
        return "Wrong email format"
    return True

def validate_password(data):
    password = data['password']
    if password == "":
        return "password is required"
    if not isinstance(password, str):
        return "email input must be a string"
    if not pattern_password.match(password):
        return "password must be atleast 5 characters"
    return True

def validate_confirm_password(data):
    password = data['password']
    if password == "":
        return "password is required"
    if not isinstance(password, str):
        return "email input must be a string"
    if not pattern_password.match(password):
        return "password must be atleast 5 characters"
    return True

def user_validate_role(data):
    role = data['role']
    if len(role) < 1:
        return "role is required"
    if not isinstance(role, str):
        return "role input must be a string"
    if not pattern.match(role):
        return "role must begin with a letter"
    return True

def validate_input(data):
    validate_all = {
        "user_name": user_validate_name(data),
        "email": user_validate_email(data),
        "password": validate_password(data),
        "confirm_password": validate_confirm_password(data),
        "role": user_validate_role(data)
    }
    if validate_all['user_name'] != True:
        return validate_all['user_name']
    if validate_all['email'] != True:
        return validate_all['email']
    if validate_all['password'] != True:
        return validate_all['password']
    if validate_all['confirm_password'] != True:
        return validate_all['confirm_password']
    if validate_all['role'] != True:
        return validate_all['role']
    return True
def validate_input_login(data):
    validate_all = {
        "email": user_validate_email(data),
        "password": validate_password(data),
    }
    if validate_all['email'] != True:
        return validate_all['email']
    if validate_all['password'] != True:
        return validate_all['password']

    return True