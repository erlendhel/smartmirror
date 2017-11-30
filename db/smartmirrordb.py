import sqlite3
import os


# Class containing all functions used for the handling of the database in the smartmirror app.
# Based on SQLite3, which stores the database locally in 'smartmirrordb'. Objects returned
# from the database are returned as tuples. For easier usage throughout this is refactored
# into a list format.
class UserDB(object):
    cursor = None
    db = None

    def __init__(self):
        # Establish connection to the database
        self.connect()
        # Assign the database-cursor
        self.cursor = self.db.cursor()
        # If a table for the users of the smartmirror does not exist in the database, it is created
        # on initialization.
        self.cursor.execute(
            '''
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    name TEXT, 
                    img_path TEXT, 
                    news_source_one TEXT,
                    news_source_two TEXT,
                    news_source_three TEXT,
                    destination TEXT,
                    travel_type TEXT
                )
            '''
        )
        # Commit changes to the database
        self.db.commit()

    # Function to connect to, or create the database if it does not exist. If it has to be created it is
    # created in the same folder as 'smartmirrordb.py' is located in.
    def connect(self):
        self.db = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + '/smartmirrordb')

    # Function which registers a user to the database.
    def register_user(self, name, img_path, news_source_one,
                      news_source_two, news_source_three, destination, travel_type):
        self.cursor.execute(
            '''
                INSERT INTO users(
                    name,
                    img_path,
                    news_source_one,
                    news_source_two,
                    news_source_three,
                    destination,
                    travel_type)
                VALUES(?, ?, ?, ?, ?, ?, ?)
            ''', (name, img_path, news_source_one, news_source_two, news_source_three, destination, travel_type)
        )
        self.db.commit()

    # Function to return all registered users
    def get_all_users(self):
        self.cursor.execute(
            '''
                SELECT * FROM users
            '''
        )
        users_tuple = self.cursor.fetchall()
        users = list()
        for user in users_tuple:
            users.append(user[0])

        return users

    # Function to return all ID's of registered users
    def get_all_ids(self):
        self.cursor.execute(
            '''
                SELECT id FROM users
            '''
        )

        id_tuples = self.cursor.fetchall()
        ids = list()
        for id in id_tuples:
            ids.append(id[0])

        return ids

    # Function to return a user from the database given an ID
    def get_user_by_id(self, user_id):
        self.cursor.execute(
            '''
                SELECT * FROM users 
                WHERE id = ?
            ''', (user_id,)
        )
        user_tuple = self.cursor.fetchone()
        user = list()
        for item in user_tuple:
            user.append(item)

        return user

    # Function to return all names of users registered in the database
    def get_all_names(self):
        self.cursor.execute(
            '''
                SELECT name FROM users
            '''
        )
        names_tuple = self.cursor.fetchall()
        names = list()
        for name in names_tuple:
            names.append(name[0])

        return names

    # Function to return a name of a user by ID
    def get_name_by_id(self, user_id):
        self.cursor.execute(
            '''
                SELECT name FROM users
                WHERE id = ?
            ''', (user_id,)
        )
        name_tuple = self.cursor.fetchone()
        name = name_tuple[0]

        return name

    # Function which gets path to training data for a user specified by ID
    def get_path_by_id(self, user_id):
        self.cursor.execute(
            '''
                SELECT img_path FROM users 
                WHERE id = ?
            ''', (user_id,)
        )
        path_tuple = self.cursor.fetchone()
        path = path_tuple[0]

        return path

    # Function which returns the news sources preferred by a user given by the ID
    def get_news_sources_by_id(self, user_id):
        self.cursor.execute(
            '''
                SELECT 
                    news_source_one,
                    news_source_two,
                    news_source_three
                FROM users WHERE id = ?
            ''', (user_id,)
        )
        sources_tuple = self.cursor.fetchall()
        sources = list()
        for source in sources_tuple:
            for item in source:
                sources.append(item)

        return sources

    # Function returning the highest primary key at the time of calling
    def get_max_id(self):
        self.cursor.execute(
            '''
                SELECT id FROM users
                ORDER BY id desc
                LIMIT 1
            '''
        )
        id_tuple = self.cursor.fetchone()
        id_value = id_tuple[0]

        return id_value

    # Function used to update the image path of a given user, takes user id and path
    def update_path(self, id, path):
        self.cursor.execute(
            '''
                UPDATE users
                SET img_path = ?
                WHERE id = ?
            ''', (path, id)
        )
        self.db.commit()

    # Function to update the news fields into the database, takes user id and a list of
    # news sources.
    def update_news(self, id, news_sources):
        source_one = news_sources[0]
        source_two = news_sources[1]
        source_three = news_sources[2]
        self.cursor.execute(
            '''
                UPDATE users
                SET
                    news_source_one = ?,
                    news_source_two = ?,
                    news_source_three = ?
                WHERE id = ?
            ''', (source_one, source_two, source_three, id)
        )
        self.db.commit()

    # Function used to update the desired destination of a user given the ID and destination
    def update_destination(self, id, destination):
        self.cursor.execute(
            '''
                UPDATE users
                SET
                    destination = ?
                WHERE id = ?
            ''', (destination, id)
        )
        self.db.commit()

    # Function used to update the type of travel used to give the travel-time
    def update_travel_type(self, id, type):
        self.cursor.execute(
            '''
                UPDATE users
                SET
                    travel_type = ?
                WHERE id = ?
            ''', (type, id)
        )
        self.db.commit()

    def add_travel_type(self):
        self.cursor.execute(
            '''
                ALTER TABLE users
                ADD COLUMN travel_type TEXT
            '''
        )
        self.db.commit()

