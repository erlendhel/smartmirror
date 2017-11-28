import sqlite3
import os


class UserDB(object):
    cursor = None
    db = None

    def __init__(self):
        self.connect()
        self.cursor = self.db.cursor()
        self.cursor.execute(
            '''
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    name TEXT, 
                    img_path TEXT, 
                    news_source_one TEXT,
                    news_source_two TEXT,
                    news_source_three TEXT,
                    destination TEXT
                    travel_type TEXT
                )
            '''
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

    def connect(self):
        self.db = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + '/smartmirrordb')

    def register_user(self, name, img_path, news_source_one,
                      news_source_two, news_source_three, destination):
        self.cursor.execute(
            '''
                INSERT INTO users(
                    name,
                    img_path,
                    news_source_one,
                    news_source_two,
                    news_source_three,
                    destination)
                VALUES(?, ?, ?, ?, ?, ?)
            ''', (name, img_path, news_source_one, news_source_two, news_source_three, destination)
        )
        self.db.commit()

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

    #
    #   Function which gets path to training data for a user specified by user_id (key)
    #
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

    #
    #   Function which gets news sources for a user specified by user_id (key)
    #   Returns a list of all news sources
    #
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

    # Function returning the max primary key of the database
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

    # Funtion used to update the image path of a given user, takes user id and path
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

db = UserDB()
db.add_travel_type()
db.update_destination(1, 'Kongsberg')
print(db.get_user_by_id(1))
db.update_travel_type(1, 'bicycling')
print(db.get_user_by_id(1))
