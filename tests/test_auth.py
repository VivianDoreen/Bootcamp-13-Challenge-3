import unittest
import json
from app.views import users
from app import app
from datetime import datetime
from config import application_config
from tests.test_base import MyTestCase

date = datetime.now()

from flask import json
from tests.test_base import MyTestCase

class TestUser(MyTestCase):
    def test_add_empty_user(self):
        """ Should return missing or bad parameters"""
        response = self.client.post('/api/v1/auth/signup',
                                    content_type='application/json',
                                    data=self.empty_user,
                                    headers=self.header
                                    )
        self.assertEqual(self.result_empty_string, response.data.decode())
        self.assertEqual(response.status_code, 422)

    def test_user_already_exists(self):
        """ should test if the email exists"""
        response = self.client.post('/api/v1/auth/signup',
                                content_type='application/json',
                                data=self.users,
                                headers=self.header
                                )
        self.assertIn("Email already exists", response.data.decode())
        self.assertEqual(response.status_code, 201)

    def test_add_user_successfully(self):
        """ should test adding a user successfully"""

        response = self.client.post('/api/v1/auth/signup',
                                    content_type='application/json',
                                    data=self.new_user_register,
                                    headers=self.header
                                   )
        self.assertEqual(response.status_code, 201)
        
    def test_add_invalid_token(self):
        """ should test user with invalid token"""

        response = self.client.post('/api/v1/auth/signup',
                                    content_type='application/json',
                                    data=self.new_user,
                                    headers=self.wrong_header
                                   )
        self.assertEqual('{\n  "message": "token is missing"\n}\n', response.data.decode())
        self.assertEqual(response.status_code, 401)
    
    def test_invalid_url(self):
        """ should test user with wrong url"""

        response = self.client.post('/api/v1/userhb ,jhs ',
                                    content_type='application/json',
                                    data=self.new_user,
                                    headers=self.header
                                   )
        self.assertIn('{\n  "Method found": "please check id"\n}\n', response.data.decode())
        self.assertEqual(response.status_code, 404)
    def test_method_not_allowed(self):
        """ should test user using a method with wrong url"""
        response = self.client.post('/api/v1/users/1',
                                    content_type='application/json',
                                    data=self.new_user,
                                    headers=self.header
                                   )
        self.assertEqual(response.status_code, 405)
    
    def test_add_user_with_missing_params(self):
        """ should test if the email exists"""
        response = self.client.post('/api/v1/auth/signup',
                                content_type='application/json',
                                data=self.missing_params,
                                headers=self.header
                                )
        self.assertIn('{\n  "message": "Wrong params for json"\n}\n', response.data.decode())
        self.assertEqual(response.status_code, 422)
    
    def test_login_user_with_empty_email(self):
        """ should test logging in with an empty email"""

        response = self.client.post('/api/v1/auth/login',
                                    content_type='application/json',
                                    data=self.no_mail_login,
                                    headers=self.header
                                    )
        self.assertIn(self.empty_email, response.data.decode())
        self.assertEqual(response.status_code, 422)
    
    def test_wrong_password(self):
        """ should test wrong_password"""
        response = self.client.post('/api/v1/auth/login',
                                    content_type='application/json',
                                    data=self.wrong_password,
                                    headers=self.header
                                    )
        self.assertIn('{\n  "message": "Wrong password"\n}\n', response.data.decode())
        self.assertEqual(response.status_code, 422)