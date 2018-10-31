import datetime
from database import  DatabaseConnection

connection = DatabaseConnection()
response = []
class UserModel(DatabaseConnection):

    @staticmethod
    def register_user(public_id, name, username, password, email, address, gender, admin):
        """
        This method registers a store attendant
        :param public_id:
        :param name:
        :param username:
        :param password:
        :param c_password:
        :param email:
        :param address:
        :param gender: 
        :param admin:
        :return: 
        """
        register_user_query = " INSERT INTO users(public_id, name, username, password, email, address, gender, admin) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        connection.cursor.execute(register_user_query,(public_id, name, username, password, email, address, gender, admin))

        return "Successfully registered"
    @staticmethod
    def get_users():
        """
        This method gets all users
        :param: 
        :return: all users
        """
        response = []
        try:
            query_to_search_users = "SELECT * FROM users"
            connection.cursor.execute(query_to_search_users)
            rows = connection.cursor.fetchall()
            if not rows:
                return False
            for eachrow in rows:
                response.append({
                    'public_id':eachrow[1],
                    'name':eachrow[2], 
                    'username':eachrow[3],
                    'password':eachrow[4],
                    'email':eachrow[5],
                    'address':eachrow[6],
                    'gender':eachrow[7],
                    'admin' :eachrow[8]
            })
            # print(response)
            return response
        except Exception as exc:
            print(exc)

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
    def check_if_is_valid_user(username):
        """
        This method logs in a store attendant
        :param username: 
        :param password: 
        :return: 
        """
        try:
            query_to_check_for_user = "SELECT * FROM users WHERE username=%s"
            connection.cursor.execute(query_to_check_for_user, [username])
            row = connection.cursor.fetchone()
            return row
        except Exception as exc:
            print(exc)


    @staticmethod
    def get_user_by_id(search_id):
        try:
            query_to_search_user = "SELECT * FROM users WHERE public_id=%s"
            connection.cursor.execute(query_to_search_user,[search_id])
            row = connection.cursor.fetchone()
            if not row:
                return False
            response.append({
                'public_id':row[1],
                'name':row[2], 
                'username':row[3],
                'password':row[4],
                'email':row[5],
                'address':row[6],
                'gender':row[7],
                'admin' :row[8]
        })
            return response
        except Exception as exc:
            print(exc)

    @staticmethod
    def modify_user(search_id, name, username, password, email, address, gender, admin):
        """
        This method modifies a user
        :param public_id: 
        :param name:
        :param username:
        :param password:
        :param email:
        :param address:
        :param gender: 
        :param admin: 
        :return: updated user
        """
        query_to_search_entry = "SELECT * FROM users WHERE public_id=%s"
        connection.cursor.execute(query_to_search_entry, [search_id])
        row = connection.cursor.fetchone()
        if not row:
            return False
        if row[2] == username:
            return 'update with same username'
        query_to_update = "UPDATE users SET name=%s, username=%s, password=%s, email=%s, address=%s, gender=%s, admin = %s WHERE public_id=%s"
        connection.cursor.execute(query_to_update,(name, username, password, email, address, gender, admin, search_id))
        return "Successfully updated"
