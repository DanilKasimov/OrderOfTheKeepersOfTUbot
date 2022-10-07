import sqlite3
import os
import datetime


class DbConnection:
    def __init__(self, name):
        self.db_name = name
        if not os.path.isfile(self.db_name):
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()

            cursor.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                            id INTEGER,
                            login TEXT,
                            name TEXT
                        )
                    """)
            cursor.execute("""
                        CREATE TABLE IF NOT EXISTS logs (
                            login TEXT,
                            action TEXT,
                            date TEXT
                        )
                    """)
            connection.commit()

    def check_user(self, user_id):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
        if cursor.fetchone() is None:
            return False
        else:
            return True

    def insert_user(self, user_id, user_login, user_name):
        if os.path.isfile(self.db_name):
            if not (self.check_user(user_id)):
                connection = sqlite3.connect(self.db_name)
                cursor = connection.cursor()
                cursor.execute(f"INSERT INTO users VALUES({user_id}, '{user_login}', '{user_name}')")
                connection.commit()
                cursor.close()
                connection.close()
            else:
                print('Error!! User already exists')
        else:
            print('Error!! DataBase don`t exists')

    def get_all_users(self):
        if os.path.isfile(self.db_name):
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users")
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            return result
        else:
            print('Error!! DataBase don`t exists')

    def get_user_id(self, username):
        if os.path.isfile(self.db_name):
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()
            cursor.execute(f"SELECT id FROM users WHERE login = '{username}'")
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            return result[0][0]
        else:
            print('Error!! DataBase don`t exists')

    def get_user_login(self, user_id):
        if os.path.isfile(self.db_name):
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()
            cursor.execute(f"SELECT login FROM users WHERE id = '{user_id}'")
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            return result[0][0]
        else:
            print('Error!! DataBase don`t exists')
    def insert_log(self, login, action):
        if os.path.isfile(self.db_name):
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()
            cursor.execute(
                f"""
                    INSERT INTO logs(login, action, date) 
                    VALUES('{login}', '{action}', '{datetime.datetime.now().strftime('%m/%d/%Y')}')
                """
            )
            connection.commit()
            cursor.close()
            connection.close()
        else:
            print('Error!! DataBase don`t exists')
    def get_statistic(self, login):
        if os.path.isfile(self.db_name):
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()
            cursor.execute(
                f"""
                    SELECT action, date
                    FROM logs 
                    WHERE login = '{login}'
                """
            )
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            return result
        else:
            print('Error!! DataBase don`t exists')