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
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<h2>Welcome to ManagerStore</h2>")

    def test_get_users(self):
        """ should test get users"""
        self.client.post('/api/v1/auth/signup',
                                    content_type='application/json',
                                    data=self.new_user,
                                    headers=self.header
                                   )
        response = self.client.get('/api/v1/users', headers=self.header)
        self.assertEqual(response.status_code, 200)

    def test_get_user_with_wrong_id(self):
        """ should test get users"""
        self.client.post('/api/v1/auth/signup',
                                    content_type='application/json',
                                    data=self.new_user,
                                    headers=self.header
                                   )
        response = self.client.get('/api/v1/users/1', headers=self.header)
        self.assertEqual(response.data.decode(), '{\n  "User": "No such user, check id"\n}\n')
        self.assertEqual(response.status_code, 200)
    
    def test_delete_user_with_invalid_id(self):
        """ should test delete users with an invalid it"""
        self.client.post('/api/v1/users',
                                    content_type='application/json',
                                    data=self.new_user,
                                    headers=self.header
                                   )
        response = self.client.delete('/api/v1/users/1', headers=self.header)
        self.assertEqual(response.data.decode(), '{\n  "Message": "No such user, check id"\n}\n')
        self.assertEqual(response.status_code, 200)