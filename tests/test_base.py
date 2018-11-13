import unittest
import json
from app.views import users
from app import app
from cerberus import Validator
from datetime import datetime
from config import application_config
from database import DatabaseConnection
import jwt
import datetime
env = application_config['TestingEnv']
# app = create_app('TestingEnv')
class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

        self.empty_user=json.dumps({
                                "name":"",
                                "email":"",
                                "password":"",
                                "confirm_password":"",
                                "role":""
                                })

        self.existing_user=json.dumps({
                               	    "name":"Mukuwa Geoffrey",
                                    "email":"doreenv.@gmail.com",
                                    "password":"mukuwa",
                                    "confirm_password":"mukuwa",
                                    "role":"admin"
                                    })

        self.new_user = json.dumps({
                                "name":"Mukuwa Geoffrey",
                                "email":"mhgfg@gmail.com",
                                "password":"mukuwa",
                                "confirm_password":"mukuwa",
                                "role":"admin"
                               })

        self.new_user_register = json.dumps({
                                    "name":"Mukuwa Geoffrey",
                                    "email":"doreenv.@gmail.com",
                                    "password":"mukuwa",
                                    "confirm_password":"mukuwa",
                                    "role":"admin"
                                })
        self.update_user = json.dumps({
                                    "name":"Nabwire Cedella",
                                    "email":"nabwirec.@gmail.com",
                                    "password":"mukuwa",
                                    "role":"admin"
                                })
        self.update_user_with_existing_email = json.dumps(
                                    {
                                        "name":"Mukuwa Geoffrey",
                                        "email":"doreenv.@gmail.com",
                                        "password":"mukuwa",
                                        "role":"admin"
                                    }
                                        )

        self.missing_params = json.dumps({
                                        "":"jiiii@gmail.com",
                                        "password":"joanita"
                                        })

        self.empty_user_login=json.dumps(
                                    {
                                    "email":"",
                                    "password":""
                                    }
                                )
        self.invalid_user=json.dumps(
                                     {
                                    	"email":"doreenv.@gmail.com",
                                        "password":"jopta"
                                     }
                                    )

        self.invalid_email = json.dumps(
                                     {
                                    	"email":"jumunaH@gmail.com",
                                        "password":"jopta"
                                     }
                                    )

        self.valid_user = json.dumps({
                                    	"email":"doreenv.@gmail.com",
                                        "password":"mukuwa"
                                    })

        self.category = json.dumps({
                                    	"category":"Furniture"
                                    })

        self.product = json.dumps({
                                "product_name":"Frames",
                                "category":"Furniture",
                                "quantity":1,
                                "unit_price":50
                                })

        self.new_product = json.dumps({
                            "product_name":"Chairs",
                            "category":"Furniture",
                            "quantity":2,
                            "unit_price":50000
                            })

        self.wrong_param_product = json.dumps({
                            "category":"Furniture",
                            "quantity":4,
                            "unit_price":50000
                            })

        self.update_product = json.dumps({
                            "product_name":"Tables",
                            "category":"Furniture",
                            "quantity":4,
                            "unit_price":50000
                            })                    
        
        self.product_with_wrong_params = json.dumps({
                                "category":"Furniture",
                                "quantity":1,
                                "unit_price":50
                                })

        self.empty_product = json.dumps({
                                        "product_name":"",
                                        "category":"",
                                        "quantity":1,
                                        "unit_price":50
                                        })
        self.sale = json.dumps({
                                    "products_id":"1",
                                    "quantity":8,
                                    "unit_price":5000
                                })

        self.sale_with_wrong_params = json.dumps({
                                    "quantity":8,
                                    "unit_price":5000
                                })
        self.empty_sale = json.dumps({
                                        "products_id":"",
                                        "quantity":"",
                                        "unit_price":5000
                                    })

        self.new_sale = json.dumps({
                                    "products_id":"1",
                                    "quantity":8,
                                    "unit_price":5000
                                })

        self.result_empty_sale = (
                                "Check your input values."
                                "\n products_id, quantity and unit price "
                                "\n\t\t\t\t- Required"
                                "\n\t\t\t\t- Must be an integer "
                                "\n\t\t\t\t- Must begin with a number"
                                )
        self.result_empty_string_login = (
                                            "\n Email*"
                                            "\n\t\t\t\t- Required"
                                            "\n\t\t\t\t- Must begin with any character"
                                            "\n\t\t\t\t- Must be a valid mail"
                                            "\n Password* "
                                            "\n\t\t\t\t- Required"
                                            "\n\t\t\t\t- Must be a string "
                                            "\n\t\t\t\t- Minlength : 5 characters"
                                            "\n\t\t\t\t- Must begin with a character"
                                         )
        self.result_empty_string = ("Check your input values."
                                    "\n name*"
                                    " \n\t\t\t\t- Required"
                                    "\n\t\t\t\t- Must be a string, "
                                    "\n\t\t\t\t- Minlength: 2 characters"
                                    "\n\t\t\t\t- Must begin with a character"
                                    "\n Email*"
                                    "\n\t\t\t\t- Required"
                                    "\n\t\t\t\t- Must begin with any character"
                                    "\n\t\t\t\t- Must be a valid mail"
                                    "\n Password* "
                                    "\n\t\t\t\t- Required"
                                    "\n\t\t\t\t- Must be a string "
                                    "\n\t\t\t\t- Minlength : 5 characters"
                                    "\n\t\t\t\t- Must begin with a character"
                                    )
        self.empty_email = (
                            "\n Email*"
                            "\n\t\t\t\t- Required"
                            "\n\t\t\t\t- Must begin with any character"
                            "\n\t\t\t\t- Must be a valid mail"
                            "\n Password* "
                            "\n\t\t\t\t- Required"
                            "\n\t\t\t\t- Must be a string "
                            "\n\t\t\t\t- Minlength : 5 characters"
                            "\n\t\t\t\t- Must begin with a character"
                            )
        self.result_empty_product = (
                                    "Check your input values."
                                    "\n product Name* and category"
                                    " \n\t\t\t\t- Required"
                                    "\n\t\t\t\t- Must be a string, "
                                    "\n\t\t\t\t- Minlength: 2 characters"
                                    "\n\t\t\t\t- Must begin with a character"
                                    "\n quantity and unit price "
                                    "\n\t\t\t\t- Required"
                                    "\n\t\t\t\t- Must be an integer "
                                    "\n\t\t\t\t- Must begin with a number"
                                )

        response = self.client.post('/api/v1/auth/signup',
                                    content_type='application/json',
                                    data=self.new_user_register,
                                   )
        
        response = self.client.post('/api/v1/auth/login',
                                content_type='application/json',
                                data=self.valid_user)
        json_data = json.loads(response.data.decode())
        self.token = json_data['x-access-token']
        self.header = {'x-access-token': self.token}

        response = self.client.post('/api/v1/categories',
                                    content_type='application/json',
                                    data=self.category,
                                    headers=self.header
                                   )

        response = self.client.post('/api/v1/products',
                                    content_type='application/json',
                                    data=self.product,
                                    headers=self.header
                                   )

        response = self.client.post('/api/v1/sales',
                                    content_type='application/json',
                                    data=self.sale,
                                    headers=self.header
                                   )
        # payload = {
        #             'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        #             'iat': datetime.datetime.utcnow(),
        #             'sub':7
        #         }
        # self.invalid_token = jwt.encode(
        #                                 payload,
        #                                 'thisissecrete',
        #                                 algorithm='HS256'
        #                                 )
        # self.wrong_header = {'xgfcjkhbn': self.invalid_token}
        

    def tearDown(self):
        db = DatabaseConnection()
        db.drop_table('users')
        db.drop_table('products')
        db.drop_table('category')
        db.drop_table('sales')

        