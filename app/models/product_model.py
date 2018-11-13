import datetime
from database import  DatabaseConnection
connection = DatabaseConnection()
response = []

class CategoryModel(object):
    def __init__(self, cat_name, current_user):
        """
        This constructor initialises category
        :param cat_name: 
        :param admin_id: 
        """
        self.current_user = current_user
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
            query_to_add_category = "INSERT INTO category(cat_name,users_id,date_created,date_modified) VALUES(%s,%s,%s,%s)"
            connection.cursor.execute(query_to_add_category,(self.cat_name, self.current_user, self.date_created, self.date_modified))
            query_to_search_category = "SELECT * FROM category WHERE cat_name=%s"
            connection.cursor.execute(query_to_search_category, [self.cat_name])
            added_category = connection.cursor.fetchone()
            result = {
                       'id': added_category[0],
                        'created by': added_category[1],
                        'category': added_category[2],
                        'Date Created': added_category[3]
                        }
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
                            'id': row[0],
                            'created by': row[1],
                            'category': row[2],
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
            response= {
                            'id': row[0],
                            'created by': row[1],
                            'category': row[2],
                            'Date Created': row[3]
                            }
            return response
        except Exception as exc:
            print(exc)
class ProductModel(object):
    def __init__(self, current_user, product_name, category, quantity, unit_price, total_price):
        """
        This constructor initialises category
        :param product_name: 
        :param category:
        :param quantity:
        :param unit_price:
        :param total_price:
        """
        self.current_user = current_user
        self.product_name = product_name
        self.category = category
        self.quantity = quantity
        self.unit_price = unit_price
        self.total_price = total_price
        self.date_created = datetime.datetime.utcnow()
        self.date_modified = datetime.datetime.utcnow()
    def create_product(self):
        """
        Adds product as an object to list
        :return: the product that has just been added
        """
        try:
            query_to_search_product = "SELECT * FROM products WHERE pdt_name=%s"
            connection.cursor.execute(query_to_search_product, [self.product_name])
            row = connection.cursor.fetchone()
            if row:
                return "Product already exists"
            query_to_add_products = "INSERT INTO products(users_id, pdt_name, cat_name, quantity, unit_price, total_price, date_created,date_modified) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
            connection.cursor.execute(query_to_add_products,(self.current_user, self.product_name,self.category, self.quantity, self.unit_price, self.total_price, self.date_created, self.date_modified))
            query_to_search_product = "SELECT * FROM products WHERE pdt_name=%s"
            connection.cursor.execute(query_to_search_product, [self.product_name])
            added_product = connection.cursor.fetchone()
            result = {
                        'id': added_product[0],
                        'created by': added_product[1],
                        'category': added_product[2],
                        'product':added_product[3],
                        'quantity': added_product[4],
                        'Unit _price': added_product[5],
                        'Total _price': added_product[6],
                        # 'date_created': added_product[7]
                        }

            return result
            
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
                            'id': row[0],
                            'created by': row[1],
                            'category': row[2],
                            'product':row[3],
                            'quantity': row[4],
                            'Unit _price': row[5],
                            'Total _price': row[6],
                            # 'date_created': row[7]
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
            response = {
                    'id': row[0],
                    'created by': row[1],
                    'category': row[2],
                    'product':row[3],
                    'quantity': row[4],
                    'Unit _price': row[5],
                    'Total _price': row[6],
                    # 'date_created': row[7]
                    }
            return response
        except Exception as exc:
            print(exc)
 
    @staticmethod
    def modify_product(search_id, product_name, category, quantity, unit_price, total_price):
        """
        This method modifies a product
        :param products_id: 
        :param product_name: 
        :param category: 
        :param quantity:
        :param unit_price:
        :param total_price:
        :return: updated product
        """
        try:
            date_created = datetime.datetime.utcnow()
            date_modified = datetime.datetime.utcnow()
            query_to_get_single_product = "SELECT * FROM products WHERE products_id=%s"
            connection.cursor.execute(query_to_get_single_product, [search_id])
            row = connection.cursor.fetchone()
            if not row:
                return "No product found, Check your id"
            query_to_check_for_product = "SELECT * FROM products WHERE pdt_name=%s"
            connection.cursor.execute(query_to_check_for_product, [product_name])
            row = connection.cursor.fetchone()
            if not row:
                print(search_id,product_name, category, quantity, unit_price, total_price)
                query_to_modify_product = "update products set pdt_name=%s, cat_name=%s,quantity=%s, unit_price = %s, total_price = %s, date_created = %s, date_modified = %s where products_id=%s"
                connection.cursor.execute(query_to_modify_product, (product_name, category, quantity, unit_price, total_price, date_created, date_modified, search_id))
                
                query_to_search_product = "SELECT * FROM products WHERE pdt_name=%s"
                connection.cursor.execute(query_to_search_product, [product_name])
                update_product_result = connection.cursor.fetchone()
                result = {
                            'id': update_product_result[0],
                            'created by': update_product_result[1],
                            'category': update_product_result[2],
                            'product':update_product_result[3],
                            'quantity': update_product_result[4],
                            'Unit _price': update_product_result[5],
                            'Total _price': update_product_result[6],
                            # 'date_created': update_product_result[7]
                            }

                return result
            return "product exists"
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
