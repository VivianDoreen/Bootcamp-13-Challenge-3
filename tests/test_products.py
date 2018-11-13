import unittest
import json
from app.views import products
import datetime
from config import application_config
from tests.test_base import MyTestCase
date = datetime.datetime.now()
from flask import json
from tests.test_base import MyTestCase

class TestUser(MyTestCase):
    def test_add_product_without_token(self):
        """ should test add product without token"""
        response = self.client.post('/api/v1/products',
                                    content_type='application/json',
                                    data=self.new_product)
        json_data = json.loads(response.data.decode())
        self.assertEqual(json_data, {'message': 'token is missing'})
        self.assertEqual(response.status_code, 401)
    
    def test_invalid_url(self):
        """ should test product with wrong url"""
        response = self.client.post('/api/v1/productsproduct',
                                    content_type='application/json',
                                    data=self.product,
                                    headers=self.header
                                   )
        json_data = json.loads(response.data.decode())
        self.assertEqual({"Method not found": "please check id"}, json_data)
        self.assertEqual(response.status_code, 404)

    def test_add_product_method_not_allowed(self):
        """ should test user using a method with wrong url"""
        response = self.client.post('/api/v1/products/1',
                                    content_type='application/json',
                                    data=self.product,
                                    headers=self.header
                                   )
        self.assertEqual(response.status_code, 405)

    def test_add_empty_product(self):
        """ Should return a 422 status error code"""
        response = self.client.post('/api/v1/products',
                                    content_type='application/json',
                                    data=self.empty_product,
                                    headers=self.header
                                    )
        self.assertEqual(self.result_empty_product, response.data.decode())
        self.assertEqual(response.status_code, 422)

    def test_product_with_wrong_params(self):
        """ should test if the product has wrong parameters"""
        response = self.client.post('/api/v1/products',
                                content_type='application/json',
                                data=self.product_with_wrong_params,
                                headers=self.header
                                )
        json_data = json.loads(response.data.decode())
        self.assertEqual({'not found': 'Wrong params for json'}, json_data)
        self.assertEqual(response.status_code, 400)

    def test_add_product_with_existing_product(self):
        """ should test add product with an existing product"""
        response = self.client.post('/api/v1/products', 
                                    content_type='application/json',
                                    data=self.product,
                                    headers=self.header)
        json_data = json.loads(response.data.decode())
        self.assertEqual(json_data, {'message': 'Product already exists'})
        self.assertEqual(response.status_code, 403)

    def test_add_product_successfully(self):
        """should test adding a product successfully"""
        response = self.client.post('/api/v1/products',
                                    content_type='application/json',
                                    data=self.new_product,
                                    headers=self.header
                                   )
        json_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_data,{'product successfully added': {'id':2,
                                                                    'created by':1,
                                                                    'category':'Furniture',
                                                                    'product':'Chairs',
                                                                    'quantity':'2',
                                                                    'Unit _price':50000,
                                                                    'Total _price':100000
                                                                    # 'date_created': datetime.datetime.utcnow()
                                                                    }}
                                                                   )

    def test_get_products_without_token(self):
        """ should test get users without token"""
        response = self.client.get('/api/v1/products')
        json_data = json.loads(response.data.decode())
        self.assertEqual(json_data, {'message': 'token is missing'})
        self.assertEqual(response.status_code, 401)

    def test_get_products_with_wrong_url(self):
        """ should test error status"""
        response = self.client.get('/api/v1/productsprod', headers=self.header)
        json_data = json.loads(response.data.decode())
        self.assertEqual(json_data, {'Method not found': 'please check id'})
        self.assertEqual(response.status_code, 404)

    def test_get_products(self):
        """ should test get products"""
        response = self.client.get('/api/v1/products', headers=self.header)
        json_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data,{'Products List': [{  'id':1,
                                                        'created by':1,
                                                        'category':'Furniture',
                                                        'product':'Frames',
                                                        'quantity':'1',
                                                        'Unit _price':50,
                                                        'Total _price':50
                                                        # 'date_created': datetime.datetime.utcnow()
                                                        }]} )

    def test_get_product_without_token(self):
        """ should test get user without token"""
        response = self.client.get('/api/v1/products/1')
        json_data = json.loads(response.data.decode())
        self.assertEqual(json_data, {'message': 'token is missing'})
        self.assertEqual(response.status_code, 401)

    def test_get_product_with_wrong_id(self):
        """ should test error status"""
        response = self.client.get('/api/v1/products/5', headers=self.header)
        json_data = json.loads(response.data.decode())
        self.assertEqual(json_data, {"message": "No product found, Check your id"})
        self.assertEqual(response.status_code, 404)    

    def test_get_product(self):
        """ should test get product"""
        response = self.client.get('/api/v1/products/1', headers=self.header)
        json_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data,{'Product': {  'id':1,
                                                        'created by':1,
                                                        'category':'Furniture',
                                                        'product':'Frames',
                                                        'quantity':'1',
                                                        'Unit _price':50,
                                                        'Total _price':50
                                                        # 'date_created': datetime.datetime.utcnow()
                                                        }} )

    def test_delete_product_without_token(self):
        """ should test delete product without token"""
        response = self.client.delete('/api/v1/products/1')
        json_data = json.loads(response.data.decode())
        self.assertEqual(json_data, {'message': 'token is missing'})
        self.assertEqual(response.status_code, 401)

    def test_delete_product_method_not_allowed(self):
        """ should test user using a method with wrong url"""
        response = self.client.delete('/api/v1/products',
                                    content_type='application/json',
                                    headers=self.header
                                   )
        self.assertEqual(response.status_code, 405)

    def test_delete_product_with_invalid_id(self):
        """ should test delete product with an invalid it"""
        response = self.client.delete('/api/v1/product/5', headers=self.header)
        json_data = json.loads(response.data.decode())
        self.assertEqual(json_data, {"Method not found": "please check id"})
        self.assertEqual(response.status_code, 404)

    def test_delete_product_successfully(self):
        """ should test delete product successfully"""
        response = self.client.delete('/api/v1/products/1', headers=self.header)
        json_data = json.loads(response.data.decode())
        self.assertEqual(json_data, {'Message': 'product deleted successfully'})
        self.assertEqual(response.status_code, 200)

    def test_update_product_without_token(self):
        """ should test update product without token"""
        response = self.client.put('/api/v1/products/1')
        json_data = json.loads(response.data.decode())
        self.assertEqual(json_data, {'message': 'token is missing'})
        self.assertEqual(response.status_code, 401)

    def test_update_product_method_not_allowed(self):
        """ should test user using a method with wrong url"""
        response = self.client.put('/api/v1/products',
                                    content_type='application/json',
                                    data=self.product,
                                    headers=self.header
                                   )
        self.assertEqual(response.status_code, 405)

    def test_update_product_with_invalid_id(self):
        """ should test update product with an invalid id"""
        response = self.client.put('/api/v1/products/5', 
                                    content_type='application/json',
                                    data=self.product,
                                    headers=self.header)
        json_data = json.loads(response.data.decode())
        self.assertEqual(json_data, {'message': 'No product found, Check your id'})
        self.assertEqual(response.status_code, 404)
    
    def test_update_with_empty_product(self):
        """Should return a 422 status code"""
        response = self.client.put('/api/v1/products/1',
                                    content_type='application/json',
                                    data=self.empty_product,
                                    headers=self.header
                                    )
        self.assertEqual(self.result_empty_product, response.data.decode())
        self.assertEqual(response.status_code, 422)    

    def test_update_product_with_existing_product(self):
        """ should test update product with an existing product"""
        response = self.client.put('/api/v1/products/1', 
                                    content_type='application/json',
                                    data=self.product,
                                    headers=self.header)
        json_data = json.loads(response.data.decode())
        self.assertEqual(json_data, {'message': 'product exists'})
        self.assertEqual(response.status_code, 403)
    
    def test_update_product_with_wrong_params(self):
        """ should test update product with wrong params"""
        response = self.client.put('/api/v1/products/1',
                                    content_type='application/json',
                                    data=self.wrong_param_product,
                                    headers=self.header
                                   )
        json_data = json.loads(response.data.decode())
        self.assertEqual(json_data, {'not found': 'Wrong params for json'})
        self.assertEqual(response.status_code, 400)

    def test_update_product_successfully(self):
        """ should test update product successfully"""
        response = self.client.put('/api/v1/products/1',
                                    content_type='application/json',
                                    data=self.update_product,
                                    headers=self.header
                                   )
        json_data = json.loads(response.data.decode())
        self.assertEqual(json_data, {'message': {'Total _price': 200000,
                                                'Unit _price': 50000,
                                                'category': 'Furniture',
                                                'created by': 1,
                                                'id': 1,
                                                'product': 'Tables',
                                                'quantity': '4'
                                                # 'date_created': 'Mon, 12 Nov 2018 04:44:40 GMT'
                                                }}
                                                )
        self.assertEqual(response.status_code, 201)    