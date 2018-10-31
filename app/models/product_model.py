import datetime
from database import  DatabaseConnection

connection = DatabaseConnection()
response = []

class CategoryModel(object):
    def __init__(self, cat_name, public_id):
        """
        This constructor initialises category
        :param cat_name: 
        :param admin_id: 
        """
        self.public_id = public_id
        self.cat_name = cat_name
        self.date_created = datetime.datetime.utcnow()
        self.date_modified = datetime.datetime.utcnow()
    def create_category(self):
        """
        Adds category as an object to list
        :return: the category that has just been added
        """
        try:
            query_to_search_category = "SELECT * FROM category WHERE cat_name=%s"
            connection.cursor.execute(query_to_search_category, [self.cat_name])
            row = connection.cursor.fetchone()
            if row:
                return "Category name already exists"
            query_to_add_category = "INSERT INTO category(cat_name,public_id,date_created,date_modified) VALUES(%s,%s,%s,%s)"
            connection.cursor.execute(query_to_add_category,(self.cat_name, self.public_id, self.date_created, self.date_modified))
            result=[]
            result.append({
                'cat_name': self.cat_name,
                'created by':self.public_id,
                'Date created': self.date_created,
                'Date Modified': self.date_modified
            })
            return result
        except Exception as exc:
            print(exc)
    @classmethod        
    def get_categories(cls):
        """
        This method gets all categories
        :param search_id: 
        :return: all categories in the store
        """
        response =[]
        query_to_get_all_categories = 'SELECT * FROM category'
        connection.cursor.execute(query_to_get_all_categories)
        rows = connection.cursor.fetchall()
        if not rows:
            return "Categories not available"
        for row in rows:
            response.append({
                            'category_id': row[0],
                            'created by': row[1],
                            'cat_name':row[3],
                            'Date Created': row[3]
                            })
        return response
    @classmethod
    def get_category(cls, search_id):
        """
        This method gets a single category
        :param search_id: 
        :return: single category and status code 200 
        """
        try:
            query_to_get_single_category = "SELECT * FROM category WHERE category_id=%s"
            connection.cursor.execute(query_to_get_single_category, [search_id])
            row = connection.cursor.fetchone()
            if not row:
                return "No category found, Check your id"
            response=[]
            response.append({
                            'category_id': row[0],
                            'created by': row[1],
                            'cat_name':row[3],
                            'Date Created': row[3]
                            })
            return response
        except Exception as exc:
            print(exc)
class ProductModel(object):
    def __init__(self, public_id, pdt_name, pdt_description, cat_name):
        """
        This constructor initialises category
        :param cat_name: 
        :param public_id:
        :param pdt_name:
        :param pdt_description:
        """
        self.public_id = public_id
        self.pdt_name = pdt_name
        self.pdt_description = pdt_description
        self.cat_name = cat_name
        self.date_created = datetime.datetime.utcnow()
        self.date_modified = datetime.datetime.utcnow()
    def create_product(self):
        """
        Adds category as an object to list
        :return: the category that has just been added
        """
        try:
            query_to_search_product = "SELECT * FROM products WHERE pdt_name=%s"
            connection.cursor.execute(query_to_search_product, [self.pdt_name])
            row = connection.cursor.fetchone()
            if row:
                return "Product already exists"
            query_to_add_products = "INSERT INTO products(public_id, pdt_name, pdt_description, cat_name,date_created,date_modified) VALUES(%s,%s,%s,%s,%s,%s)"
            connection.cursor.execute(query_to_add_products,(self.public_id, self.pdt_name, self.pdt_description, self.cat_name, self.date_created, self.date_modified))
            return "product successfully added"
            
        except Exception as exc:
            print(exc)

    @classmethod        
    def get_products(cls):
        """
        This method gets all products
        :param public_id: 
        :return: all products in the store
        """
        response =[]
        query_to_get_all_products = 'SELECT * FROM products'
        connection.cursor.execute(query_to_get_all_products)
        rows = connection.cursor.fetchall()
        if not rows:
            return "Products not available"
        for row in rows:
            response.append({
                            'pdt_id': row[0],
                            'created by': row[1],
                            'product name': row[2],
                            'cat_name':row[3],
                            'Category': row[4],
                            'Date Created': row[5]
                            })
        return response
    
    @classmethod
    def get_product(cls, search_id):
        """
        This method gets a single product
        :param search_id: 
        :return: single product and status code 200 
        """
        try:
            query_to_get_single_product = "SELECT * FROM products WHERE products_id=%s"
            connection.cursor.execute(query_to_get_single_product, [search_id])
            row = connection.cursor.fetchone()
            if not row:
                return "No product found, Check your id"
            response=[]
            response.append({
                            'pdt_id': row[0],
                            'created by': row[1],
                            'product name': row[2],
                            'product_description':row[3],
                            'Category': row[4],
                            'Date Created': row[5]
                            })
            return response
        except Exception as exc:
            print(exc)
        



    @staticmethod
    def modify_product(search_id, pdt_name, pdt_description, cat_name):
        """
        This method modifies a product
        :param products_id: 
        :param pdt_name: 
        :param pdt_description: 
        :param cat_name:
        :return: updated entry
        """
        try:
            query_to_modify_product = "update products set pdt_name=%s, pdt_description=%s, cat_name=%s where products_id=%s"
            connection.cursor.execute(query_to_modify_product, (pdt_name, pdt_description, cat_name, search_id))
            return "successfully Updated"
        except Exception as exc:
            print(exc)
       

    @classmethod
    def delete_product(cls, search_id):
        """
        This method deletes a single product
        :param search_id: 
        :return: message and status code 200 
        """
        try:
            query_to_delete_single_product = "delete from products where products_id=%s"
            connection.cursor.execute(query_to_delete_single_product, [search_id])
            return "product deleted successfully"
        except Exception as exc:
            print(exc)
