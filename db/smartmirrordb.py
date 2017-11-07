import sqlite3
import os


class UserDB(object):
    cursor = None
    db = None

    def __init__(self):
        self.db = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + '/smartmirrordb')
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
        return self.cursor.fetchall()


    def get_user_by_id(self, user_id):
        self.cursor.execute(
            '''
                SELECT * FROM users 
                WHERE id = ?
            ''', (user_id,)
        )
        return self.cursor.fetchone()

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
        return self.cursor.fetchone()

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
        return self.cursor.fetchall()
