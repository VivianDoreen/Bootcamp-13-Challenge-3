import datetime
from database import  DatabaseConnection
connection = DatabaseConnection()
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
        Adds sales as an object to list
        :return: the sale that has just been added
        """
        try:
            query_to_get_product = "SELECT products_id, quantity, total_price, unit_price FROM products WHERE products.products_id=%s"
            connection.cursor.execute(query_to_get_product, [self.products_id])
            row = connection.cursor.fetchone()
            
            if not row:
                return "No product found, please check your id"
            
            product_quantity = row[1]
            product_total_price = row[2]
            product_unit_price = row[3]

            if (self.quantity):
                pass
            change_type_quantity = int(self.quantity)
            change_type_unit_price = int(self.unit_price)
            if change_type_quantity <= 0:
                return "quantity must be a positive number"
            if change_type_unit_price <=0:
                return "unit price must be a positive number"
            if change_type_unit_price <= int(product_unit_price):
                return "Sale unit price must be greater than the purchase unit price"
            if change_type_quantity > int(product_quantity):
                return "Quantity must be less than the available quantity"
            new_quantity = int(product_quantity) - change_type_quantity
            new_total_price = int(product_total_price) - self.total_price

            query_to_modify_product = "update products set quantity=%s, total_price = %s where products_id=%s;"
            connection.cursor.execute(query_to_modify_product, (new_quantity, new_total_price, self.products_id))
            
            query_to_search_product = "SELECT * FROM products WHERE products_id=%s"
            connection.cursor.execute(query_to_search_product, [self.products_id])
            update_product_result = connection.cursor.fetchone()
            print(update_product_result)
            if not update_product_result:
                return "Unable to update product"
            print("successfully updated")
            query_to_add_sales = "INSERT INTO sales(users_id, products_id, quantity, unit_price, total_price, date_created,date_modified) VALUES(%s,%s,%s,%s,%s,%s,%s)"
            connection.cursor.execute(query_to_add_sales,(self.current_user, self.products_id, change_type_quantity, change_type_unit_price, self.total_price, self.date_created, self.date_modified))
            query_to_search_sale = "SELECT * FROM sales WHERE products_id=%s"
            print(self.products_id)
            connection.cursor.execute(query_to_search_sale, [self.products_id])
            added_sale = connection.cursor.fetchone()
            print(added_sale)
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
        query_to_get_all_sales = "select sales.sales_id, sales.users_id, products.pdt_name, sales.quantity, sales.unit_price, sales.total_price, sales.date_created from sales, products where sales.products_id = products.products_id;"
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
    @classmethod
    def get_single_sale(cls, search_id):
        """
        This method gets a single sale
        :param search_id: 
        :return: single sale and status code 200 
        """
        try:
            query_to_get_single_sale = "select sales.sales_id, sales.users_id, products.pdt_name, sales.quantity, sales.unit_price, sales.total_price, sales.date_created from sales, products where sales.products_id = products.products_id AND sales_id = %s;"
            # query_to_get_single_sale = "SELECT * FROM sales WHERE sales_id=%s"
            connection.cursor.execute(query_to_get_single_sale, [search_id])
            row = connection.cursor.fetchone()
            if not row:
                return "No sale found, Check your id"
            response = {
                        'id': row[0],
                        'admin': row[1],
                        'product': row[2],
                        'quantity':row[3],
                        'unit_price':row[4],
                        'total_price':row[5],
                        'date_created': row[6]
                    }
            return response
        except Exception as exc:
            print(exc)
    @classmethod
    def get_total_sale_by_attendant(cls, search_id):
        """
        This method gets total sale made by an attendant
        :param search_id: 
        :return: single total sale and status code 200 
        """
        try:
            query_to_total_sale = "select sum(total_price) as total from sales where users_id = %s"
            connection.cursor.execute(query_to_total_sale, [search_id])
            row = connection.cursor.fetchone()
            if not row:
                return "No sale made"
            response = {
                        'total':row[0]
                    }
            print(response)
            return response
        except Exception as exc:
            print(exc)

    @staticmethod
    def modify_sale(search_id, products_id, quantity, unit_price, total_price):
        """
        This method modifies a sale
        :param sales_id: 
        :param products_id: 
        :param quantity:
        :param unit_price:
        :param total_price:
        :return: updated sale
        """
        try:
            date_modified = datetime.datetime.utcnow()
            query_to_get_single_sale = "SELECT * FROM sales WHERE sales_id=%s" 
            connection.cursor.execute(query_to_get_single_sale, [search_id])
            row = connection.cursor.fetchone()
            if not row:
                return "No sale found, Check your id"
            query_to_modify_sale = "update sales set products_id=%s, quantity=%s, unit_price=%s, total_price = %s, date_modified = %s where sales_id=%s"
            connection.cursor.execute(query_to_modify_sale, (products_id, quantity, unit_price, total_price, date_modified, search_id))
            
            query_to_search_sales = "SELECT * FROM sales WHERE sales_id=%s"
            connection.cursor.execute(query_to_search_sales, [search_id])
            row = connection.cursor.fetchone()
            print(row)
            result = {
                        'id': row[0],
                        'created by': row[1],
                        'product': row[2],
                        'quantity':row[3],
                        'unit_price':row[4],
                        'total_price':row[5],
                        'Date Created': row[6]
                        }
            return result
        except Exception as exc:
            print(exc)
    
    @classmethod
    def delete_sale(cls, search_id):
        """
        This method deletes a single sale
        :param search_id: 
        :return: message and status code 200 
        """
        try:
            query_to_get_single_sale = "SELECT * FROM sales WHERE sales_id=%s"
            connection.cursor.execute(query_to_get_single_sale, [search_id])
            row = connection.cursor.fetchone()
            if not row:
                response = "No sale found, Check your id"
                return response

            query_to_delete_single_sale = "delete from sales where sales_id=%s"
            connection.cursor.execute(query_to_delete_single_sale, [search_id])
            return "sale deleted successfully"
        except Exception as exc:
            print(exc)