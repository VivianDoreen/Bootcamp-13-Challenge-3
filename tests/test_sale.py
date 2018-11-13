import unittest
import json
from app.views import sales
# from app import create_app
from datetime import datetime
from config import application_config
from tests.test_base import MyTestCase
date = datetime.now()
from flask import json
from tests.test_base import MyTestCase

class TestUser(MyTestCase):
    def test_add_sale_without_token(self):
        """ should test add sale without token"""
        response = self.client.post('/api/v1/sales',
                                    content_type='application/json',
                                    data=self.sale)
        json_data = json.loads(response.data.decode())
        self.assertEqual(json_data, {'message': 'token is missing'})
        self.assertEqual(response.status_code, 401)

    def test_invalid_url(self):
        """ should test sale with wrong url"""
        response = self.client.post('/api/v1/saless',
                                    content_type='application/json',
                                    data=self.sale,
                                    headers=self.header
                                   )
        json_data = json.loads(response.data.decode())
        self.assertEqual({"Method not found": "please check id"}, json_data)
        self.assertEqual(response.status_code, 404)

    # def test_add_sale_method_not_allowed(self):
    #     """ should test sale using a method with wrong url"""
    #     response = self.client.post('/api/v1/sales/1',
    #                                 content_type='application/json',
    #                                 data=self.sale,
    #                                 headers=self.header
    #                                )
    #     self.assertEqual(response.status_code, 405)

    def test_add_empty_sale(self):
        """ Should return a 422 status error code"""
        response = self.client.post('/api/v1/sales',
                                    content_type='application/json',
                                    data=self.empty_sale,
                                    headers=self.header
                                    )
        self.assertEqual(self.result_empty_sale, response.data.decode())
        self.assertEqual(response.status_code, 422)

    def test_sale_with_wrong_params(self):
        """ should test if the sale has wrong parameters"""
        response = self.client.post('/api/v1/sales',
                                content_type='application/json',
                                data=self.sale_with_wrong_params,
                                headers=self.header
                                )
        json_data = json.loads(response.data.decode())
        self.assertEqual({'not found': 'Wrong params for json'}, json_data)
        self.assertEqual(response.status_code, 400)
    
    # def test_add_sale_successfully(self):
    #     """should test adding a sale successfully"""
    #     response = self.client.post('/api/v1/sales',
    #                                 content_type='application/json',
    #                                 data=self.new_sale,
    #                                 headers=self.header
    #                                )
    #     json_data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 201)
        # self.assertEqual(json_data,{'product successfully added': {'id':2,
        #                                                             'created by':1,
        #                                                             'category':'Furniture',
        #                                                             'product':'Chairs',
        #                                                             'quantity':'2',
        #                                                             'Unit _price':50000,
        #                                                             'Total _price':100000
        #                                                             # 'date_created': datetime.datetime.utcnow()
        #                                                             }}
        #                                                            )


    # def test_invalid_url(self):
    #     """ should test sale with wrong url"""

    #     response = self.client.post('/api/v1/userhb ,jhs ',
    #                                 content_type='application/json',
    #                                 data=self.sale,
    #                                 headers=self.header
    #                                )
    #     self.assertIn('{\n  "Method not found": "please check id"\n}\n', response.data.decode())
    #     self.assertEqual(response.status_code, 404)

    # def test_method_not_allowed(self):
    #     """ should test sale using a method with wrong url"""
    #     response = self.client.post('/api/v1/sales/1',
    #                                 content_type='application/json',
    #                                 data=self.sale,
    #                                 headers=self.header
    #                                )
    #     self.assertEqual(response.status_code, 404)

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
        self.assertEqual(response.data.decode(), '{\n  "Method not found": "please check id"\n}\n')
        self.assertEqual(response.status_code, 404)

 