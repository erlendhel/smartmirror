# Wrapper class used in the user registration process
# TODO: Bugs with facerec and singletonCamera. Needs fix before face registration will work. Pathing

from db import smartmirrordb
from facerec import register_face
from facerec import facerec
from news import News
from speech_rec import registration_speech
from speech_rec import register_news


class Wrapper(object):
    fr = None
    db = None
    speech = None
    reg_news = None
    news = None
    user = None
    news_sources = list()

    def __init__(self):
        self.db = smartmirrordb.UserDB()
        self.speech = registration_speech.Registration()
        self.reg_news = register_news.RegisterNews()
        self.news = News.News()

    # Wrapper function used to set username and store it to the database
    # Returns the ID / Primary Key assigned to the registered user.
    def set_user_name(self, name):  # TODO: TAKES ARGUMENT FOR TESTING ONLY
        # name = self.speech.set_name() TODO: COMMENTED FOR TESTING ONLY
        print(name)  # TODO: FOR TESTING
        self.db.register_user(name, None, None, None, None, None)
        id = self.db.get_max_id()
        return id

    # Wrapper function which stores reference images of the user's face to
    # file and saves the path to the dir in the database.
    def add_user_face(self, id):
        path = register_face.add_face(id)
        self.db.update_path(id, path)

    # Wrapper function which stores the user's preferred news to the database
    def add_news(self, id):
        self.reg_news.set_preferred_news()
        news_list = self.reg_news.get_preferred_news()
        self.db.update_news(id, news_list)

    # Function which returns self.user
    def get_user(self, id):
        if self.user is not None:
            return self.user
        # If the user is None, we need to assign values to the user from the db
        else:
            user_list = self.db.get_user_by_id(id)
            print(user_list)
            # Create a user object as as dict for easier reference with the field names from the db
            self.user = {
                'id': user_list[0],
                'name': user_list[1],
                'img_path': user_list[2],
                'news_source_one': user_list[3],
                'news_source_two': user_list[4],
                'news_source_three': user_list[5],
                'destination': user_list[6]
            }
            return self.user

    # Function which gets news sources for a specific user given by the id and sets them
    # to self.news_sources
    def set_news_sources(self, id):
        placeholder_sources = self.db.get_news_sources_by_id(id)
        sources = self.news.set_preferred_sources(placeholder_sources)
        for source in sources:
            self.news_sources.append(source.source)

    # Function which returns self.news_sources
    def get_news_sources(self):
        return self.news_sources

    # Function which returns all articles for a source given by the source_id
    def get_articles_by_source(self, source_id):
        articles = self.news.get_articles_by_source(self.news_sources, source_id)
        return articles
    
    def get_article_by_id(self, article_id):
        article = self.news.get_article_by_id(article_id)
        return article

    def predict(self):
        if self.fr is None:
            self.fr = facerec.FacialRecognition()
        return self.fr.predict()

# TODO: For testing
if __name__ == '__main__':
    reg = Wrapper()
    # reg.predict() uses the predict() function from FacialRecognition class in facerec.py. The predict() function
    # now times each prediction to ensure the loop doesn't last longer than 10 seconds. If the duration exceeds 10s,
    # the function will return False. If the function manages to predict a user within the 10 seconds, the USER ID, is
    # returned for further use. Example of usage below:

    # Get the return value from reg.predict(), which in turn calls fr.predict(). Returns false if it doesn't find
    # user within 10 seconds, returns user_id if found.
    id = reg.predict()
    if id is False:
        print(id)
        # Do something ....
    else:
        print('User found!', id)
        # Use ID to get a user from the database, returns a dict with all field names as written in db. See function
        # get_user() line: 49.
        user = reg.get_user(id)
        print(user)
        # Access different indexes of the dict in user
        print(user['name'])
        print(user['img_path'])
        print(user['news_source_one'])
        print(user['news_source_two'])
        print(user['news_source_three'])