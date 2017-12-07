import sys
sys.path.append('/home/pi/Desktop/repos/smartmirror/')

from speech_rec import speechrec
from speech_rec import news_keywords
from db import smartmirrordb
from news import News


class MenuSpeech(object):
    news_list = list()
    selected_news = None
    recognizer = None
    db = None

    def __init__(self):
        self.recognizer = speechrec.SpeechRecognition()
        self.db = smartmirrordb.UserDB()

    # Function to wake up smartmirror from sleepmode. 'Magic words' are given in command
    def initialize_mirror(self):
        command = self.recognizer.get_audio()
        if command == 'Wake up mirror' or command == 'wake up mirror':
            print('Initialize smartmirror')

    # Chech to see if microphone is opened
    def is_busy(self):
        return self.recognizer.is_busy()

    # Function used in the login screen, takes voice commands and determines the validity
    # of the given commands.
    def login_screen(self):
        command = self.recognizer.get_audio()
        if command is None:
            return None  
        elif self.login_command(command):
            return "login"
        elif self.register_command(command):
            return "register"
        elif self.guest_command(command):
            return "guest"
        

    # Defining functions to use in each module of the smartmirror to
    # minimize the workload on each screen
    def main_menu_speech(self):
        command = self.recognizer.get_audio()
        if command == 'Weather' or command == 'weather':
            return "weather"
        elif command == 'Settings' or command == 'settings':
            return "settings"
        elif self.determine_news_source(command):
            print('Going to: ', self.selected_news)
            return self.selected_news
        elif self.logout_command(command):
            return "logout"
        elif command == 'Hello' or command =='hello':
            return "hello"

    def weather_speech(self):
        command = self.recognizer.get_audio()
        if self.back_command(command):
            return "back"

    # Only listening for the user asking to go back to main menu
    def back_speech(self):
        command = self.recognizer.get_audio()
        if self.back_command(command):
            return "back"
        


    # TODO: Used in startup to assign a user's preferred news. Gets values from the database based on id
    def assign_pref_news(self, id):
        pref_news = self.db.get_news_sources_by_id(id)
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

        print("Prefered news has been assigned in menu_speechrec")
        

    # Function to determine if a user has issued a login command, iterates through
    # a list of valid commands and returns true if the given input matches a valid command.
    # Passes if not
    def login_command(self, command):
        if command is None:
            return False
        
        valid_commands = [
            'log in','login','logon',
            'log on','sign in','morgan',
            'not in','logmein','logan',
            'nothing','blogging','looking',
            'onions', 'bullying','sending',
            'finding','london', 'phantom',
            'find him','tanning', 'simon',
            'find in'
        ]

        command = command.lower()
        
        for valid in valid_commands:
            if command == valid:
                return True

        return False
        
        # Check if the  command is in the valid_commands list
        # lower() will make the string lowercase,
        # used to shrinken size of command list
        # if any(command.lower() in s for s in valid_commands):
            #return True

    def logout_command(self, command):
        if command is None:
            return False
        
        valid_commands = [
            'sign out', 'log out', 'logout',
            'sign off','signout', 'log off'
            'logoff', 'lookout', 'look up',
            'no doubt', 'look at','knockout',
            'got out', 'look out','google',
            'return', 'knocked up', 'adult',
            'bergen', 'guardian', 'not up',
            'renault', 'bob hope', 'return',
            'mcgowan'
        ]

        command = command.lower()
        if 'out' in command:
            return True
        
        for valid in valid_commands:
            if command == valid:
                return True

        return False
        
        # Check if the  command is in the valid_commands list
        # lower() will make the string lowercase,
        # used to shrinken size of command list
        #if any(command.lower() in s for s in valid_commands):
        #    return True

    # Function to determine if a user has issued a register command, iterates through
    # a list of valid commands and returns true if the given input matches a valid command.
    # Passes if not
    def register_command(self, command):
        if command is None:
            return False
        
        valid_commands = [
            'register','registration','sign up'
        ]

        command = command.lower()
        
        for valid in valid_commands:
            if command == valid:
                return True

        return False
        
        # Check if the  command is in the valid_commands list
        #if any(command.lower() in s for s in valid_commands):
        #    return True

    # Function to determine if a user has issued a command to login as a guest, iterates through
    # a list of valid commands and returns true if the given input matches a valid command.
    # Passes if not
    def guest_command(self, command):
        if command is None:
            return False 
        
        valid_commands = [
            'guest','guess','log in as guest'
            'login as guest', 'sign in as guest'
            'desk', 'best','just','test'
        ]

        command = command.lower()

        for valid in valid_commands:
            if command == valid:
                return True

        return False

        # Check if the  command is in the valid_commands list
        # if any(command.lower() in s for s in valid_commands):
        #    return True

    def back_command(self, command):
        if command is None:
            return False
        
        valid_commands = [
            'back', 'go back','previous',
            'main menu', 'menu','black',
            'call back','callback','tobacco',
            'brought back', 'dekk', 'bolt back',
            'baalbek', 'min meny', 'main',
            'birkbeck','golf back', 'bullock',
            'blu-tack','backwards', 'return',
            'returned'
            ]
        
        command = command.lower()
       
        # Check if the command contains 'back' as a substring
        if "back" in command:
            return True

        for valid in valid_commands:
            if command == valid:
                return True

        return False
        
        # Check if the  command is in the valid_commands list
        #if any(command.lower() in s for s in valid_commands):
        #    return True

    # TODO: OLD!!! MAYBE REDUNDANT
    # Uses the list of preferred news defined in News.py. This list will be
    # based on the individual preferences of the user. In order to optimize
    # performance during runtime, this check will be done at the activation
    # of the mirror. The loop is constrained by the size of preferred_sources,
    # which is 3. The predefined voice-commands of a news source are appended
    # to news_list if the given news-source is contained in preferred_sources.
    def assign_preferred_news(self):
        pref_news = News.News.preferred_sources

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
                

