import psycopg2
from flask import Flask
from config import application_config

import os

app = Flask(__name__)

class DatabaseConnection():
    def __init__(self):
        """
        This constructor creates a connection to the database
        :param dbname: 
        :param user: 
        :param password: 
        :param host: 
        :param port: 
        """
        self.conn_params = dict(
            user = "postgres",
            password = "viv",
            host = "127.0.0.1",
            port = "5432",
            database = 'ManagerStore'
            )
        
        self.connection = psycopg2.connect(**self.conn_params)                        
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def create_tables(self):
        """ This method creates all tables"""
        create_table_query_for_category = ( 
                                    """ CREATE TABLE IF NOT EXISTS 
                                    category(
                                                category_id SERIAL PRIMARY KEY NOT NULL,
                                                users_id INTEGER,
                                                cat_name VARCHAR (50) UNIQUE,
                                                date_created TIMESTAMP, 
                                                date_modified TIMESTAMP,
                                                FOREIGN KEY (users_id)REFERENCES 
                                                users (users_id) ON DELETE CASCADE ON UPDATE CASCADE
                                            );"""
                                    )

        create_table_query_for_products = ( 
                                           """ CREATE TABLE IF NOT EXISTS 
                                            products(
                                                        products_id SERIAL PRIMARY KEY,
                                                        users_id INTEGER,
                                                        cat_name VARCHAR (50),
                                                        pdt_name VARCHAR (50) NOT NULL, 
                                                        quantity VARCHAR (50),
                                                        unit_price INTEGER NOT NULL,
                                                        total_price INTEGER NOT NULL,
                                                        date_created TIMESTAMP, 
                                                        date_modified TIMESTAMP, 
                                                        FOREIGN KEY (users_id)REFERENCES 
                                                        users (users_id) ON DELETE CASCADE ON UPDATE CASCADE,
                                                        FOREIGN KEY (cat_name)REFERENCES 
                                                        category (cat_name) ON DELETE CASCADE ON UPDATE CASCADE 
                                                    );"""
                                            )
        
        create_table_query_for_users = (
                                        """CREATE TABLE IF NOT EXISTS
                                        users(
                                                users_id SERIAL PRIMARY KEY,
                                                name VARCHAR(50) NOT NULL,
                                                email VARCHAR (50) UNIQUE,
                                                password VARCHAR(100) NOT NULL,
                                                role VARCHAR(50) NOT NULL
                                                ); """
                                        )
        create_table_query_for_sales = (
                                        """CREATE TABLE IF NOT EXISTS
                                        sales(
                                                sales_id SERIAL PRIMARY KEY,
                                                users_id INTEGER,
                                                products_id INTEGER,
                                                quantity INTEGER NOT NULL,
                                                unit_price INTEGER NOT NULL,
                                                total_price INTEGER NOT NULL,
                                                date_created TIMESTAMP, 
                                                date_modified TIMESTAMP,
                                                FOREIGN KEY (users_id)REFERENCES 
                                                users (users_id) ON DELETE CASCADE ON UPDATE CASCADE,
                                                FOREIGN KEY (products_id)REFERENCES 
                                                products (products_id) ON DELETE CASCADE ON UPDATE CASCADE 

                                                ); """
                                        )
        # Execute creating tables
        self.cursor.execute(create_table_query_for_users)
        self.cursor.execute(create_table_query_for_category)
        self.cursor.execute(create_table_query_for_products)
        self.cursor.execute(create_table_query_for_sales)
    
    # def create_admin(self):
    #     register_admin_query = " INSERT INTO users(name, email, password, role) VALUES (%s,%s,%s,%s)"
    #     self.cursor.execute(register_admin_query,("Nabulo vivian doreen", "nabwire@gmail.com", "pbkdf2:sha256:50000$5NsHWNe0$2bef20e2d5bb71000577132950ac888976e3008af7f08832d29442c71b4fdc14", "admin"))

    # Remove all the records from the table
    def drop_table(self, table_name):
        """
        This method truncates a table
        :param table_name: 
        :return: 
        """
        self.cursor.execute("TRUNCATE TABLE {} RESTART IDENTITY CASCADE"
                            .format(table_name))