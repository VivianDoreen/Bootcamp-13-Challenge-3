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
            query_to_search_category = "SELECT * FROM sales WHERE products_id=%s"
            connection.cursor.execute(query_to_search_category, [self.products_id])
            added_sale = connection.cursor.fetchone()
            result = {
                        'id': added_sale[0],
                        'created by': added_sale[1],
                        'product': added_sale[2],
                        'quantity':added_sale[3],
                        'unit_price':added_sale[4],
                        'total_price':added_sale[5],
                        'Date Created': added_sale[6]
                        }
            return result
            
        except Exception as exc:
            print(exc)
    @classmethod        
    def get_sales(cls):
        """
        This method gets all sales
        :return: all sales in the store
        """
        response =[]
        query_to_get_all_sales = 'SELECT * FROM sales'
        connection.cursor.execute(query_to_get_all_sales)
        rows = connection.cursor.fetchall()
        if not rows:
            return "Sales not available"
        for row in rows:
            response.append({
                            'id': row[0],
                            'created by': row[1],
                            'product': row[2],
                            'quantity':row[3],
                            'unit_price':row[4],
                            'total_price':row[5],
                            'Date Created': row[6]
                            })
        return response