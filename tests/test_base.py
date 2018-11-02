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

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config.from_object(application_config['TestingEnv'])
        db = DatabaseConnection('testdatabase')
        db.create_tables()

        self.empty_user=json.dumps({
                                "name":"",
                                "email":"",
                                "password":"",
                                "confirm_password":"",
                                "role":""
                                })

        self.users=json.dumps({
                                "name":"Nabulo Vivian",
                                "email":"joaviv@gmail.com",
                                "password":"joanita",
                                "confirm_password":"joanita",
                                "role":"admin"
                             })
        self.new_user = json.dumps({
                                "name":"Mukuwa Geoffrey",
                                "email":"mhgfg@gmail.com",
                                "password":"mukuwa",
                                "confirm_password":"mukuwa",
                                "role":"admin"
                               })
        self.missing_params = json.dumps({
                                        "":"jiiii@gmail.com",
                                        "password":"joanita"
                                        })
        self.no_mail_login = json.dumps({
                                        "email":"",
                                        "password":"joanita"
                                        })
        self.wrong_password = json.dumps({
                                        "email":"jiiii@gmail.com",
                                        "password":"jopta"
                                        })
        self.valid_user = json.dumps({
                                    "email":"jiiii@gmail.com",
                                    "password":"joanita"
                                    })
        
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

        response = self.client.post('/api/v1/auth/login',
                                content_type='application/json',
                                data=self.valid_user)
        json_data = json.loads(response.data.decode())
        self.token = json_data['token']
        self.header = {'x-access-token': self.token}

        payload = {
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                    'iat': datetime.datetime.utcnow(),
                    'sub':7
                }
        self.invalid_token = jwt.encode(
                                        payload,
                                        'thisissecrete',
                                        algorithm='HS256'
                                        )
        self.wrong_header = {'xgfcjkhbn': self.invalid_token}
        

    def tearDown(self):
        db = DatabaseConnection('testdatabase')
        db.drop_table('users')
        db.drop_table('products')
        db.drop_table('category')
        db.drop_table('sales')

        