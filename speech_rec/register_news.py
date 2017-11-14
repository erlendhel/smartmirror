from speech_rec import speechrec
from speech_rec import news_keywords


# Class housing the functions used to register different news sources in the registration
# process. Compares the voice commands given to the dict of news given in news_keywords.py
class RegisterNews(object):
    recognizer = None
    preferred_news = None

    def __init__(self):
        self.recognizer = speechrec.SpeechRecognition()
        self.preferred_news = list()

    # Function used to return the list preferred news. Used in the registration process
    # where the returned list is added to the database as news sources.
    def get_preferred_news(self):
        return self.preferred_news

    # Function used to set the preferred news based on given voice commands.
    # Iterates through the dict given in news_keywords.py and appends a positive
    # result to the list preferred_news. Counter makes sure no more than 3 sources
    # are added per registration. For simplicity, the user cannot undo choices made
    # in the selection.
    def set_preferred_news(self):
        finished = False
        counter = 0
        while not finished:
            audio = str(self.recognizer.get_audio())
            found = False
            if counter < 3:
                for source in news_keywords.sources:
                    if audio == source:
                        self.preferred_news.append(source)
                        counter = counter + 1
                        found = True
                    elif found is False:
                        for item in news_keywords.sources[source]:
                            if audio == item:
                                self.preferred_news.append(source)
                                counter = counter + 1
                                found = True
                if found is False:
                    print('Invalid source, try again..')
            else:
                print('Registration of news complete..')
                finished = True
