# Wrapper class used in the user registration process
# TODO: Bugs with facerec and singletonCamera. Needs fix before face registration will work. Pathing

from db import smartmirrordb
from facerec import register_face
from speech_rec import registration_speech
from speech_rec import register_news


class Registration(object):
    db = None
    speech = None
    news = None

    def __init__(self):
        self.db = smartmirrordb.UserDB()
        self.speech = registration_speech.Registration()
        self.news = register_news.RegisterNews()

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
        self.news.set_preferred_news()
        news_list = self.news.get_preferred_news()
        self.db.update_news(id, news_list)

        pass
        
if __name__ == '__main__':
    reg = Registration()
    reg.add_news(1)