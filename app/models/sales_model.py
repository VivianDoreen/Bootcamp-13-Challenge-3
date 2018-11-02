import datetime
from database import  DatabaseConnection

connection = DatabaseConnection("ManagerStore")
response = []

class SaleModel(object):
    def __init__(self, current_user, products_id, quantity, unit_price, total_price):
        """
        This constructor initialises product
        :param products_id: 
        :param quantity:
        :param unit_price:
        :param total_price:
        """
        self.current_user = current_user
        self.products_id = products_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.total_price = total_price
        self.date_created = datetime.datetime.utcnow()
        self.date_modified = datetime.datetime.utcnow()
    def create_sales(self):
        """
        Adds product as an object to list
        :return: the product that has just been added
        """
        try:
            query_to_add_products = "INSERT INTO sales(users_id, products_id, quantity, unit_price, total_price, date_created,date_modified) VALUES(%s,%s,%s,%s,%s,%s,%s)"
            connection.cursor.execute(query_to_add_products,(self.current_user, self.products_id, self.quantity, self.unit_price, self.total_price, self.date_created, self.date_modified))
            return "sale successfully added"
            

            
        except Exception as exc:
            print(exc)
