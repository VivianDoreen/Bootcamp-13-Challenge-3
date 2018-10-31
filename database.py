from psycopg2 import connect

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

        self.connection = connect("dbname=ManagerStore user =postgres password='viv' host=localhost port=5432")
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def create_tables(self):
        """ This method creates all tables"""
        create_table_query_for_category = ( 
                                    """ CREATE TABLE IF NOT EXISTS 
                                    category(
                                                category_id SERIAL PRIMARY KEY NOT NULL,
                                                public_id VARCHAR(50) UNIQUE,
                                                cat_name VARCHAR (50) NOT NULL,
                                                admin_id INTEGER NOT NULL,
                                                date_created TIMESTAMP, 
                                                date_modified TIMESTAMP,
                                                FOREIGN KEY (public_id)REFERENCES 
                                                users (public_id) ON DELETE CASCADE ON UPDATE CASCADE
                                            );"""
                                    )

        create_table_query_for_products = ( 
                                           """ CREATE TABLE IF NOT EXISTS 
                                            products(
                                                        products_id SERIAL PRIMARY KEY,
                                                        public_id VARCHAR(50) UNIQUE,
                                                        pdt_name VARCHAR (50) NOT NULL, 
                                                        pdt_description VARCHAR (50) NOT NULL,
                                                        category_id INTEGER NOT NULL,
                                                        admin_id INTEGER NOT NULL, 
                                                        date_created TIMESTAMP, 
                                                        date_modified TIMESTAMP, 
                                                        FOREIGN KEY (public_id)REFERENCES 
                                                        users (public_id) ON DELETE CASCADE ON UPDATE CASCADE,
                                                        FOREIGN KEY (public_id)REFERENCES 
                                                        category (public_id) ON DELETE CASCADE ON UPDATE CASCADE 
                                                        );"""
                                            )
        
        create_table_query_for_users = (
                                        """CREATE TABLE IF NOT EXISTS
                                        users(
                                                        users_id SERIAL PRIMARY KEY,
                                                        public_id VARCHAR(50) UNIQUE,
                                                        name VARCHAR(50) NOT NULL ,
                                                        username VARCHAR(50) NOT NULL,
                                                        password VARCHAR(100) NOT NULL,
                                                        email VARCHAR (20) NOT NULL,
                                                        address VARCHAR(50) NOT NULL,
                                                        gender CHAR(1),
                                                        admin BOOLEAN
                                                        ); """
                                        )

        # Execute creating tables
        self.cursor.execute(create_table_query_for_users)
        self.cursor.execute(create_table_query_for_category)
        self.cursor.execute(create_table_query_for_products)
    # Remove all the records from the table
    def drop_table(self, table_name):
        """
        This method truncates a table
        :param table_name: 
        :return: 
        """
        self.cursor.execute("TRUNCATE TABLE {} RESTART IDENTITY CASCADE"
                            .format(table_name))