import unittest
import json
from app.views import sales
from app import app
from datetime import datetime
from config import application_config
from tests.test_base import MyTestCase

date = datetime.now()

from flask import json
from tests.test_base import MyTestCase

class TestUser(MyTestCase):
    def test_add_empty_sale(self):
        """ Should return a 422 status error code"""
        response = self.client.post('/api/v1/sales',
                                    content_type='application/json',
                                    data=self.empty_sale,
                                    headers=self.header
                                    )
        self.assertEqual(self.result_empty_sale, response.data.decode())
        self.assertEqual(response.status_code, 422)

    def test_invalid_url(self):
        """ should test sale with wrong url"""

        response = self.client.post('/api/v1/userhb ,jhs ',
                                    content_type='application/json',
                                    data=self.sale,
                                    headers=self.header
                                   )
        self.assertIn('{\n  "Method found": "please check id"\n}\n', response.data.decode())
        self.assertEqual(response.status_code, 404)

    def test_method_not_allowed(self):
        """ should test sale using a method with wrong url"""
        response = self.client.post('/api/v1/sales/1',
                                    content_type='application/json',
                                    data=self.sale,
                                    headers=self.header
                                   )
        self.assertEqual(response.status_code, 404)

    def test_get_users(self):
        """ should test get sale"""
        self.client.post('/api/v1/sale',
                                    content_type='application/json',
                                    data=self.sale,
                                    headers=self.header
                                )
        response = self.client.get('/api/v1/sales', headers=self.header)
        self.assertEqual(response.status_code, 200)
 
    
    def test_delete_sale_with_invalid_id(self):
        """ should test delete sale with an invalid it"""
        self.client.post('/api/v1/sale',
                                    content_type='application/json',
                                    data=self.sale,
                                    headers=self.header
                                   )
        response = self.client.delete('/api/v1/sale/1', headers=self.header)
        self.assertEqual(response.data.decode(), '{\n  "Method found": "please check id"\n}\n')
        self.assertEqual(response.status_code, 404)

 