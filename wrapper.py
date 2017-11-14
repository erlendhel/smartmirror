# Wrapper class used in the user registration process
# TODO: Bugs with facerec and singletonCamera. Needs fix before face registration will work. Pathing

from db import smartmirrordb
from facerec import register_face
from news import News
from speech_rec import registration_speech
from speech_rec import register_news


class Wrapper(object):
    db = None
    speech = None
    reg_news = None
    news = None
    user = None

    def __init__(self):
        self.db = smartmirrordb.UserDB()
        self.speech = registration_speech.Registration()
        self.reg_news = register_news.RegisterNews()
        self.news = News.News()

    #   Wrapper function used to set username and store it to the database
    #   Returns the ID / Primary Key assigned to the registered user.
    def set_user_name(self, name):  # TODO: TAKES ARGUMENT FOR TESTING ONLY
        # name = self.speech.set_name() TODO: COMMENTED FOR TESTING ONLY
        print(name)  # TODO: FOR TESTING
        self.db.register_user(name, None, None, None, None, None)
        id = self.db.get_max_id()
        return id

    #   Wrapper function which stores reference images of the user's face to
    #   file and saves the path to the dir in the database.
    def add_user_face(self, id):
        path = register_face.add_face(id)
        self.db.update_path(id, path)

    #   Wrapper function which stores the user's preferred news to the database
    def add_news(self, id):
        self.reg_news.set_preferred_news()
        news_list = self.reg_news.get_preferred_news()
        self.db.update_news(id, news_list)

    def user_db_to_dict(self, id):
        user_list = self.db.get_user_by_id(id)
        # Create a user object as a dict for easy reference with the field names from the database
        self.user = {
            'id': user_list[0],
            'name': user_list[1],
            'img_path': user_list[2],
            'news_source_one': user_list[3],
            'news_source_two': user_list[4],
            'news_source_three': user_list[5],
            'destination': user_list[6]
        }

    def get_user(self):
        if self.user is not None:
            return self.user


if __name__ == '__main__':
    reg = Wrapper()
    user = reg.get_user()
    print(user)
