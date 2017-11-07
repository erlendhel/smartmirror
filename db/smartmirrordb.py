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
                )
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
        return user_tuple

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

    def update_path(self, id, path):
        self.cursor.execute(
            '''
                UPDATE users
                SET img_path = ?
                WHERE id = ?
            ''', (path, id)
        )

db = UserDB()
print(db.get_all_names())
