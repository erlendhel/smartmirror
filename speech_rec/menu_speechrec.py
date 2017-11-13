from speech_rec import speechrec
from speech_rec import news_keywords
from news import news


class MenuSpeech(object):
    news_list = list()
    selected_news = None
    recognizer = None

    def __init__(self):
        self.recognizer = speechrec.SpeechRecognition()

    # Function to wake up smartmirror from sleepmode. 'Magic words' are given in command
    def initialize_mirror(self):
        command = self.recognizer.get_audio()
        if command == 'Wake up mirror' or command == 'wake up mirror':
            print('Initialize smartmirror')

    # Defining functions to use in each module of the smartmirror to
    # minimize the workload on each screen
    def main_menu_speech(self):
        command = self.recognizer.get_audio()
        if command == 'Weather' or command == 'weather':
            print('Going to weather')
        elif command == 'Settings' or command == 'settings':
            print('Going to settings')
        elif self.determine_news_source(command):
            print('Going to: ', self.selected_news)

    def weather_speech(self):
        command = self.recognizer.get_audio()
        if command == 'Back' or command == 'back':
            print('Going to main menu')

    # TODO: MAYBE REDUNDANT
    # Uses the list of preferred news defined in news.py. This list will be
    # based on the individual preferences of the user. In order to optimize
    # performance during runtime, this check will be done at the activation
    # of the mirror. The loop is constrained by the size of preferred_sources,
    # which is 3. The predefined voice-commands of a news source are appended
    # to news_list if the given news-source is contained in preferred_sources.
    def assign_preferred_news(self):
        pref_news = news.News.preferred_sources

        for source in pref_news:
            if source == 'bbc-news':
                self.news_list.append(news_keywords.bbc)
            elif source == 'bbc-sport':
                self.news_list.append(news_keywords.bbc_sport)
            elif source == 'business-insider':
                self.news_list.append(news_keywords.business_insider)
            elif source == 'daily-mail':
                self.news_list.append(news_keywords.daily_mail)
            elif source == 'engadged':
                self.news_list.append(news_keywords.engadged)
            elif source == 'espn':
                self.news_list.append(news_keywords.espn)
            elif source == 'financial-times':
                self.news_list.append(news_keywords.financial_times)
            elif source == 'fortune':
                self.news_list.append(news_keywords.fortune)
            elif source == 'fox-sports':
                self.news_list.append(news_keywords.fox_sports)
            elif source == 'mirror':
                self.news_list.append(news_keywords.mirror)
            elif source == 'national-geographic':
                self.news_list.append(news_keywords.national_geographic)
            elif source == 'techcrunch':
                self.news_list.append(news_keywords.techcrunch)
            elif source == 'techradar':
                self.news_list.append(news_keywords.techradar)
            elif source == 'the-new-york-times':
                self.news_list.append(news_keywords.the_new_york_times)
            elif source == 'time':
                self.news_list.append(news_keywords.time)

    # TODO: MAYBE REDUNDANT
    # Function that determines if a specific news-source is called upon.
    # Takes the 'command' variable which contains the voice-recording in
    # string-format. Checks if the string matches any of the strings given
    # for the preferred news-sources in 'news_list'. 'news_list' is a list
    # which contains lists for all three preferred news-sources. Each of
    # the lists are populated with the keywords predefined in news_keywords.py.
    # If a match is found, 'selected_news' is set to the first index of the
    # list item, which contains the keyword used in the News API to get
    # articles from the API.
    def determine_news_source(self, command):
        for source in self.news_list:
            for keyword in source:
                if command == keyword:
                    self.selected_news = source[0]
                    return True
