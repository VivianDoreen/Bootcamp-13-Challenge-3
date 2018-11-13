import unittest
import json
from app.views import users
# from app import create_app
from datetime import datetime
from config import application_config
from tests.test_base import MyTestCase

date = datetime.now()
# app = create_app('TestingEnv')

from flask import json
from tests.test_base import MyTestCase

class TestUser(MyTestCase):
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<h2>Welcome to ManagerStore</h2>")

    def test_get_users_without_token(self):
        """ should test get users with wrong url"""
        response = self.client.get('/api/v1/users')
        json_data = json.loads(response.data.decode())
        self.assertEqual(json_data, {'message': 'token is missing'})
        self.assertEqual(response.status_code, 401)

    def test_get_users(self):
        """ should test get users"""
        response = self.client.get('/api/v1/users', headers=self.header)
        json_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data, {'Users of ManagerStore':[{'email': 'doreenv.@gmail.com',
                                                                'name': 'Mukuwa Geoffrey',
                                                                'role': 'admin',
                                                                'uri': 'http://localhost/api/v1/users?user_id=1'}]
                                                                })

    def test_get_user_without_token(self):
        """ should test get users with wrong url"""
        response = self.client.get('/api/v1/users/1')
        json_data = json.loads(response.data.decode())
        self.assertEqual(json_data, {'message': 'token is missing'})
        self.assertEqual(response.status_code, 401)

    def test_get_user(self):
        """ should test get users"""
        self.client.post('/api/v1/auth/signup',
                                    content_type='application/json',
                                    data=self.new_user,
                                    headers=self.header
                                   )
        response = self.client.get('/api/v1/users/1', headers=self.header)
        json_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data, {'User':{
                                                'email': 'doreenv.@gmail.com',
                                                'name': 'Mukuwa Geoffrey',
                                                'role': 'admin',
                                                'id': 1}
                                            })

    def test_get_user_with_wrong_url(self):
        """ should test get users with wrong url"""
        response = self.client.get('/api/v1/usersusers', headers=self.header)
        json_data = json.loads(response.data.decode())
        self.assertEqual(json_data, {'Method not found':'please check id'})
        self.assertEqual(response.status_code, 404)

    def test_get_user_with_wrong_id(self):
        """ should test get users"""
        response = self.client.get('/api/v1/users/5', headers=self.header)
        json_data = json.loads(response.data.decode())
        self.assertEqual(json_data, {"User": "No such user, check id"})
        self.assertEqual(response.status_code, 404)
    
    def test_delete_user_without_token(self):
        """ should test delete user successfully"""
        response = self.client.delete('/api/v1/users/1')
        json_data = json.loads(response.data.decode())     
        self.assertEqual(json_data, {'message': 'token is missing'})
        self.assertEqual(response.status_code, 401)

    def test_delete_method_not_allowed(self):
        """ should test delete user using a method with wrong url"""
        response = self.client.delete('/api/v1/users',
                                    content_type='application/json',
                                    headers=self.header
                                   )
        self.assertEqual(response.status_code, 405) 

    def test_delete_user_with_invalid_id(self):
        """ should test delete users with an invalid it"""
        response = self.client.delete('/api/v1/users/5', headers=self.header)
        json_data = json.loads(response.data.decode())     
        self.assertEqual(json_data, { "Message": "No such user, check id"})
        self.assertEqual(response.status_code, 404)
    
    def test_delete_user_successfully(self):
        """ should test delete user successfully"""
        response = self.client.delete('/api/v1/users/1', headers=self.header)
        json_data = json.loads(response.data.decode())     
        self.assertEqual(json_data, {"Message": "Successfully Deleted"})
        self.assertEqual(response.status_code, 200)

    def test_update_user_without_token(self):
        """ should test delete user successfully"""
        response = self.client.put('/api/v1/users/1')
        json_data = json.loads(response.data.decode())     
        self.assertEqual(json_data, {'message': 'token is missing'})
        self.assertEqual(response.status_code, 401)

    def test_update_user_with_existing_email(self):
        """ should test for update with an existing email"""
        response = self.client.put('/api/v1/users/1',
                                    content_type='application/json',
                                    data=self.update_user_with_existing_email,
                                    headers=self.header)
        json_data = json.loads(response.data.decode())     
        self.assertEqual(json_data, {'message': 'email already exists'})
        self.assertEqual(response.status_code, 404) 

    def test_update_user_with_invalid_id(self):
        """ should test updates a user successfully"""
        response = self.client.put('/api/v1/users/5',
                                    content_type='application/json',
                                    data=self.update_user,
                                    headers=self.header)
        json_data = json.loads(response.data.decode())     
        self.assertEqual(json_data, { "message": "No such user, check id"}
                                                )
        self.assertEqual(response.status_code, 404)  

    def test_update_method_not_allowed(self):
        """ should test user using a method with wrong url"""
        response = self.client.put('/api/v1/users',
                                    content_type='application/json',
                                    data=self.update_user,
                                    headers=self.header
                                   )
        self.assertEqual(response.status_code, 405)  

    def test_update_user_successfully(self):
        """ should test delete user successfully"""
        response = self.client.put('/api/v1/users/1',
                                    content_type='application/json',
                                    data=self.update_user,
                                    headers=self.header)
        json_data = json.loads(response.data.decode())     
        self.assertEqual(json_data, {'message': {'email': 'nabwirec.@gmail.com',
                                                'id': 1,
                                                'name': 'Nabwire Cedella',
                                                'role': 'admin'}}
                                                )
        self.assertEqual(response.status_code, 201)