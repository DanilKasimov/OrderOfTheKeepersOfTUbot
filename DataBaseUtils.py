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