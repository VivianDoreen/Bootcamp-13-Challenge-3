import unittest
import json
from app.views import products
from app import app
from datetime import datetime
from config import application_config
from tests.test_base import MyTestCase

date = datetime.now()

from flask import json
from tests.test_base import MyTestCase

class TestUser(MyTestCase):
    def test_add_empty_product(self):
        """ Should return a 422 status error code"""
        response = self.client.post('/api/v1/products',
                                    content_type='application/json',
                                    data=self.empty_product,
                                    headers=self.header
                                    )
        self.assertEqual(self.result_empty_product, response.data.decode())
        self.assertEqual(response.status_code, 422)

    def test_product_with_wrong_paras(self):
        """ should test if the product has wrong parameters"""
        response = self.client.post('/api/v1/auth/signup',
                                content_type='application/json',
                                data=self.product,
                                headers=self.header
                                )
        self.assertIn('{\n  "message": "Wrong params for json"\n}\n', response.data.decode())
        self.assertEqual(response.status_code, 422)

    def test_add_user_successfully(self):
        """ should test adding a user successfully"""

        response = self.client.post('/api/v1/auth/signup',
                                    content_type='application/json',
                                    data=self.new_user_register,
                                    headers=self.header
                                   )
        self.assertEqual(response.status_code, 201)
    
    def test_invalid_url(self):
        """ should test product with wrong url"""

        response = self.client.post('/api/v1/userhb ,jhs ',
                                    content_type='application/json',
                                    data=self.product,
                                    headers=self.header
                                   )
        self.assertIn('{\n  "Method found": "please check id"\n}\n', response.data.decode())
        self.assertEqual(response.status_code, 404)

    def test_method_not_allowed(self):
        """ should test user using a method with wrong url"""
        response = self.client.post('/api/v1/products/1',
                                    content_type='application/json',
                                    data=self.product,
                                    headers=self.header
                                   )
        self.assertEqual(response.status_code, 405)

        def test_get_users(self):
            """ should test get products"""
            self.client.post('/api/v1/products',
                                        content_type='application/json',
                                        data=self.product,
                                        headers=self.header
                                    )
            response = self.client.get('/api/v1/products', headers=self.header)
            self.assertEqual(response.status_code, 200)

    def test_get_product_with_wrong_id(self):
        """ should test error status"""
        self.client.post('/api/v1/products',
                                    content_type='application/json',
                                    data=self.product,
                                    headers=self.header
                                   )
        response = self.client.get('/api/v1/products/1', headers=self.header)
        self.assertEqual(response.status_code, 200)
    
    def test_delete_product_with_invalid_id(self):
        """ should test delete product with an invalid it"""
        self.client.post('/api/v1/product',
                                    content_type='application/json',
                                    data=self.product,
                                    headers=self.header
                                   )
        response = self.client.delete('/api/v1/product/1', headers=self.header)
        self.assertEqual(response.data.decode(), '{\n  "Method found": "please check id"\n}\n')
        self.assertEqual(response.status_code, 404)

 