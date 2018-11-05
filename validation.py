from flask import Flask, jsonify, request, url_for, abort, make_response
from cerberus import Validator

def make_public_user(user):
    new_user = {}
    for field in user:
        if field == 'id':
            new_user['uri'] = url_for('get_users', user_id=user['id'], _external=True)
        else:
            new_user[field] = user[field]
    return new_user

class ValidateInput:
        @staticmethod
        def validate_input():
                schema = {
                    'name': {
                            'required': True,
                            'type': 'string',
                            'empty': False,
                            'regex': r'^[a-zA-Z]{2,50}(?:[\s_-]{1}[a-zA-Z]+)*$'
                            },
                    'email': {
                            'required': True,
                            'type': 'string',
                            'empty': False,
                            'regex': r'[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]{2,4}'
                            },
                    'password': {
                            'required': True,
                            'type': 'string',
                            'empty': False,
                            'regex': r'^[a-zA-Z0-9]{5,100}.*[\s.]*$'
                            },
                    'confirm_password':{
                            'required': True,
                            'type': 'string',
                            'empty': False,
                            'regex': r'^[a-zA-Z0-9].*[\s.]*$'
                            },
                    'role': {
                                'required': True,
                                'type': 'string',
                                'empty': False,
                                'regex': r'^[a-zA-Z]{2,50}(?:[\s_-]{1}[a-zA-Z]+)*$'
                                }
                           
                }
            
                return Validator(schema)

        @staticmethod
        def validate_login_input():
                login_schema = {
                     'password': {
                            'required': True,
                            'type': 'string',
                            'empty': False,
                            'regex': r'^[a-zA-Z0-9]{5,100}.*[\s.]*$'
                            },
                    'email': {
                            'required': True,
                            'type': 'string',
                            'empty': False,
                            'regex': r'[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]{2,4}'
                            }
                }
                return Validator(login_schema)
                
        @staticmethod
        def validate_product():
                schema = {
                'product_name': {
                        'required': True,
                        'type': 'string',
                        'empty': False,
                        'regex': r'^[a-zA-Z]{2,50}(?:[\s_-]{1}[a-zA-Z]+)*$'
                            },
                'category': {
                        'required': True,
                        'type': 'string',
                        'empty': False,
                        'regex': r'^[a-zA-Z]{2,50}(?:[\s_-]{1}[a-zA-Z]+)*$'
                        },
                'quantity': {
                        'required': True,
                        'type': 'integer',
                        'empty': False,
                        'regex': r'^[0-9]'
                        },
                'unit_price': {
                        'required': True,
                        'type': 'integer',
                        'empty': False,
                        'regex': r'^[0-9]'
                        }
                }
                return Validator(schema)
        @staticmethod
        def validate_category():
                schema = {
                'category': {
                        'required': True,
                        'type': 'string',
                        'empty': False,
                        'regex': r'^[a-zA-Z]{2,50}(?:[\s_-]{1}[a-zA-Z]+)*$'
                        }
                }
                return Validator(schema)
        
        @staticmethod
        def validate_sale():
                schema = {
                'products_id': {
                        'required': True,
                        'type': 'integer',
                        'empty': False,
                        'regex': r'^[0-9]'
                            },
                'quantity': {
                        'required': True,
                        'type': 'integer',
                        'empty': False,
                        'regex': r'^[0-9]'
                        },
                'unit_price': {
                        'required': True,
                        'type': 'integer',
                        'empty': False,
                        'regex': r'^[0-9]'
                        }
                }
                return Validator(schema)


