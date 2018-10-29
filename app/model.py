import datetime
from database import  DatabaseConnection

connection = DatabaseConnection()

class UserModel(DatabaseConnection):

    @staticmethod
    def register_store_attendant(name, username, password, c_password, email, address, dod, gender, admin):
        """
        This method registers a store attendant
        :param name:
        :param username:
        :param password:
        :param c_password:
        :param email:
        :param address:
        :param dod:
        :param gender: 
        :param admin:
        :return: 
        """
        register_attendant_query = " INSERT INTO store_attendant(name, username, password, c_password, email, address, dod, gender, admin) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        connection.cursor.execute(register_attendant_query,(name, username, password, c_password, email, address, dod, gender, admin))

    @staticmethod
    def check_if_attendant_exists_using_username(username):
        """
         This method checks for duplicate store attendant using username
        :param username: 
        :return: 
        """
        query_for_checking_username = "SELECT username FROM store_attendant WHERE username=%s"
        connection.cursor.execute(query_for_checking_username, [username])
        row = connection.cursor.fetchone()
        return row

    @staticmethod
    def check_if_is_valid_attendant(username, password):
        """
        This method logs in a store attendant
        :param username: 
        :param password: 
        :return: 
        """
        try:
            query_to_check_for_attendant = "SELECT attendant_id FROM store_attendant WHERE username=%s AND password=%s "
            connection.cursor.execute(query_to_check_for_attendant, (username, password))
            row = connection.cursor.fetchone()
            return row
        except Exception as exc:
            print(exc)


    @staticmethod
    def get_attendant_by_id(attendant_id):
        try:
            query_to_search_attendant = "SELECT attendant_id FROM store_attendant WHERE attendant_id=%s"
            connection.cursor.execute(query_to_search_attendant,[attendant_id])
            row = connection.cursor.fetchone()
            return row
        except Exception as exc:
            print(exc)

class CategoryModel(object):

    def __init__(self, cat_name, admin_id):
        """
        This constructor initialises category
        :param cat_name: 
        :param admin_id: 
        """
        self.admin_id = admin_id
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
                return True
            query_to_add_category = "INSERT INTO category(cat_name, admin_id,date_created,date_modified) VALUES(%s,%s,%s,%s)"
            connection.cursor.execute(query_to_add_category,(self.cat_name, self.admin_id, self.date_created, self.date_modified))
            result=[]
            result.append({
                'cat_name': self.cat_name,
                'admin_id':self.admin_id,
                'Date created': self.date_created,
                'Date Modified': self.date_created
            })
            return result
        except Exception as exc:
            print(exc)

    @classmethod
    def get_categories(cls, admin_id):
        """
        This method gets all categories
        :param admin_id: 
        :return: all categories in the store
        """
        response =[]
        query_to_get_all_categories = 'SELECT * FROM category WHERE admin_id=%s'
        connection.cursor.execute(query_to_get_all_categories,[admin_id])
        rows = connection.cursor.fetchall()
        if not rows:
            return False
        for row in rows:
            response.append({
                            'id': row[0],
                            'cat_name': row[1],
                            'Date created': row[4],
                            'Date Modified': row[5]
                            })
        return response

    @staticmethod
    def get_category(search_id, admin_id):
        """
        This method gets a single category
        :param search_id: 
        :param admin_id: 
        :return: single category and status code 200 
        """
        try:
            query_to_get_single_category = "SELECT * FROM category WHERE category_id=%s AND admin_id=%s"
            connection.cursor.execute(query_to_get_single_category, (search_id, admin_id))
            row = connection.cursor.fetchone()
            if not row:
                return False
            response=[]
            response.append({
                            'id': row[0],
                            'cat_name': row[1],
                            'Date created': row[4],
                            'Date Modified': row[5]
                })
            return response
        except Exception as exc:
            print(exc)


    @classmethod
    def modify_category(cls, category_id, cat_name, admin_id):
        """
        This method modifies a category
        :param cat_name:
        :param admin_id: 
        :return: updated category
        """
        query_to_search_category = "SELECT * FROM cat_name WHERE category_id=%s AND admin_id=%s"
        connection.cursor.execute(query_to_search_category, (category_id, admin_id))
        row = connection.cursor.fetchone()
        if not row:
            return False
        if row[1] == cat_name:
            return 'update with same name'
        date_modified=datetime.datetime.utcnow()
        query_to_update = "UPDATE category SET cat_name=%s, date_modified=%s WHERE admin_id=%s AND category_id=%s"
        connection.cursor.execute(query_to_update,(cat_name, date_modified,admin_id,category_id))
        row_updated = connection.cursor.rowcount
        return row_updated

class ProductsModel(object):

    def __init__(self, pdt_name, pdt_description, cat_name, admin_id):
        """
        This constructor initialises product
        :param name: 
        :param desc: 
        :param cat_name:
        :param admin_id: 
        """
        self.admin_id = admin_id
        self.pdt_name = pdt_name
        self.pdt_description = pdt_description
        self.cat_name = cat_name
        self.date_created = datetime.datetime.utcnow()
        self.date_modified = datetime.datetime.utcnow()

    def create_product(self):
        """
        Adds product as an object to list
        :return: the product that has just been added
        """

        try:
            query_to_search_product = "SELECT * FROM products WHERE pdt_name=%s"
            connection.cursor.execute(query_to_search_product, [self.pdt_name])
            row = connection.cursor.fetchone()
            if row:
                return True
            query_to_add_product = "INSERT INTO products(pdt_name, pdt_description, category_id, admin_id,date_created,date_modified) VALUES(%s,%s,%s,%s,%s)"
            connection.cursor.execute(query_to_add_product,(self.pdt_name, self.pdt_description, self.cat_name, self.admin_id, self.date_created, self.date_modified))
            result=[]
            result.append({
                'pdt_name': self.pdt_name,
                'pdt_description': self.pdt_description,
                'category_id':self.cat_name,
                'Date created': self.date_created,
                'Date Modified': self.date_created
            })
            return result
        except Exception as exc:
            print(exc)

    @classmethod
    def get_products(cls, admin_id):
        """
        This method gets all products
        :param admin_id: 
        :return: all products in the store
        """
        response =[]
        query_to_get_all_products = 'SELECT * FROM products WHERE admin_id=%s'
        connection.cursor.execute(query_to_get_all_products,[admin_id])
        rows = connection.cursor.fetchall()
        if not rows:
            return False
        for row in rows:
            response.append({
                            'id': row[0],
                            'pdt_name': row[1],
                            'pdt_description': row[2],
                            'cat_name':row[3],
                            'Date created': row[4],
                            'Date Modified': row[5]
                            })
        return response

    @staticmethod
    def get_product(search_id, admin_id):
        """
        This method gets a single product
        :param search_id: 
        :param admin_id: 
        :return: single product and status code 200 
        """
        try:
            query_to_get_single_product = "SELECT * FROM products WHERE products_id=%s AND admin_id=%s"
            connection.cursor.execute(query_to_get_single_product, (search_id, admin_id))
            row = connection.cursor.fetchone()
            if not row:
                return False
            response=[]
            response.append({
                    'id': row[0],
                    'pdt_name': row[1],
                    'pdt_description': row[2],
                    'cat_name':row[3],
                    'Date created': row[4],
                    'Date Modified': row[5]
                })
            return response
        except Exception as exc:
            print(exc)


    @classmethod
    def modify_product(cls, products_id, pdt_name, pdt_description, category_name, admin_id):
        """
        This method modifies a product
        :param products_id: 
        :param pdt_name: 
        :param pdt_description: 
        :param cat_name:
        :param admin_id: 
        :return: updated entry
        """
        query_to_search_category = "SELECT * FROM entries WHERE products_id=%s AND admin_id=%s"
        connection.cursor.execute(query_to_search_category, (products_id, admin_id))
        row = connection.cursor.fetchone()
        if not row:
            return False
        if row[1] == pdt_name:
            return 'update with same name'
        date_modified=datetime.datetime.utcnow() 
        query_to_update = "UPDATE products SET pdt_name=%s, pdt_description=%s, category_name=%s, date_modified=%s WHERE admin_id=%s AND products_id=%s"
        connection.cursor.execute(query_to_update,(pdt_name,pdt_description,date_modified,admin_id,products_id))
        row_updated = connection.cursor.rowcount
        return row_updated