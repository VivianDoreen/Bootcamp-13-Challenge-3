import unittest
import json
from app.views import users
# from app import create_app
from datetime import datetime
from config import application_config
from tests.test_base import MyTestCase
from flask import json
from tests.test_base import MyTestCase


date = datetime.now()

class TestUser(MyTestCase):
    def test_add_empty_user_login(self):
        """ Should return missing on error message"""
        response = self.client.post('/api/v1/auth/login',
                                    content_type='application/json',
                                    data=self.empty_user_login,
                                    headers=self.header
                                    )
        self.assertEqual(self.result_empty_string_login, response.data.decode())
        self.assertEqual(response.status_code, 422)

    def test_invalid_login_details(self):
        """ should test user with invalid login details"""
        response = self.client.post('/api/v1/auth/login',
                                    content_type='application/json',
                                    data=self.invalid_user,
                                   )
        json_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual({'message': 'Wrong password'}, json_data)

    def test_invalid_email_details(self):
        """ should test user with invalid login details"""
        response = self.client.post('/api/v1/auth/login',
                                    content_type='application/json',
                                    data=self.invalid_email
                                   )
        json_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual({'message': 'could not verify the user'}, json_data)

    def test_add_user_successfully(self):
        """ should test adding a user successfully"""

        response = self.client.post('/api/v1/auth/signup',
                                    content_type='application/json',
                                    data=self.new_user,
                                   )
        json_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_data,  {'message': {'email': 'mhgfg@gmail.com',
                                                'id': 2,
                                                'name': 'Mukuwa Geoffrey',
                                                'role': 'admin'}}
                                                )

    def test_valid_token(self):
        response = self.client.post('/api/v1/auth/login',
                                content_type='application/json',
                                data=self.valid_user)
        json_data = json.loads(response.data.decode())
        self.token = json_data['x-access-token']
        self.header = {'x-access-token': self.token}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data, {
                                    'id':1,
                                    'name':'Mukuwa Geoffrey',
                                    'email':'doreenv.@gmail.com',
                                    'message': 'Login successful',
                                    'x-access-token':self.token
                                    })

    def test_add_empty_user_signup(self):
        """ Should return missing on error message"""
        response = self.client.post('/api/v1/auth/signup',
                                    content_type='application/json',
                                    data=self.empty_user,
                                    headers=self.header
                                    )
        self.assertEqual(self.result_empty_string, response.data.decode())
        self.assertEqual(response.status_code, 422)

    def test_add_user_with_missing_params(self):
        """ should test if the email exists"""
        response = self.client.post('/api/v1/auth/signup',
                                content_type='application/json',
                                data=self.missing_params,
                                headers=self.header
                                )
        self.assertIn('{\n  "message": "Wrong params for json"\n}\n', response.data.decode())
        self.assertEqual(response.status_code, 422)

    def test_user_already_exists(self):
        """ should test if the email exists"""
        response = self.client.post('/api/v1/auth/signup',
                                content_type='application/json',
                                data=self.existing_user,
                                headers=self.header
                                )
        self.assertIn("Email already exists", response.data.decode())
        self.assertEqual(response.status_code, 403)
      
    def test_invalid_url(self):
        """ should test user with wrong url"""
        response = self.client.post('/api/v1/userhb ,jhs ',
                                    content_type='application/json',
                                    data=self.new_user,
                                    headers=self.header
                                   )
        json_data = json.loads(response.data.decode())
        self.assertEqual({"Method not found": "please check id"}, json_data)
        self.assertEqual(response.status_code, 404)

    def test_method_not_allowed(self):
        """ should test user using a method with wrong url"""
        response = self.client.post('/api/v1/users/1',
                                    content_type='application/json',
                                    data=self.new_user,
                                    headers=self.header
                                   )
        self.assertEqual(response.status_code, 405)
    