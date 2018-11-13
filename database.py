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
        # self.conn_params = dict(
        #     user = "postgres",
        #     password = "viv",
        #     host = "127.0.0.1",
        #     port = "5432",
        #     database = ''
        #     )
        self.conn_params = dict(
                user = "gfivvjrdwipjtq",
                password = "13a48a0f3204482bc5468647f5251f0878f826f29459e55f0374bc72fb38daa0",
                host = "ec2-23-23-101-25.compute-1.amazonaws.com",
                port = "5432",
                database = 'dd1t4am05632i'
                # ssl=true;
                # sslfactory='org.postgresql.ssl.NonValidatingFactory'
                )
            
        # if application_config['DevelopmentEnv'].ENV == 'development':
        #     dbname = application_config['DevelopmentEnv'].DATABASE
        #     self.conn_params['database'] = dbname
            
            # if application_config['TestingEnv'].ENV == 'testing':
            #     dbname = application_config['TestingEnv'].DATABASE
            #     self.conn_params['database'] = dbname

        
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
                                                email VARCHAR (20) UNIQUE,
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
    # Remove all the records from the table
    def drop_table(self, table_name):
        """
        This method truncates a table
        :param table_name: 
        :return: 
        """
        self.cursor.execute("TRUNCATE TABLE {} RESTART IDENTITY CASCADE"
                            .format(table_name))