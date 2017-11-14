from speech_rec import speechrec
from speech_rec import news_keywords
from news import News


# Class used for user-registration with the help of speech-recognition
class Registration(object):
    recognizer = None
    name = None
    alphabet = ['A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'EE', 'e', 'F', 'f',
                'G', 'g', 'H', 'h', 'I', 'i', 'J', 'j', 'K', 'k', 'L', 'l',
                'M', 'm', 'N', 'n', 'O', 'o', 'P', 'p', 'Q', 'q', 'R', 'r'
                'S', 's', 'T', 't', 'U', 'u', 'V', 'v', 'W', 'w', 'X', 'x'
                'Y', 'y', 'Z', 'z']

    def __init__(self):
        self.recognizer = speechrec.SpeechRecognition()
        self.name = ""

    def set_name(self):
        name_accept = False
        print('INSTRUCTIONS: ')
        print('Please spell your name, you have to do it one letter at a time. When a letter is registered'
              ' it will appear on the screen')
        print('If the wrong letter is recognized, say BACK, to erase the last letter.')
        print('When finished, say ENTER or COMPLETE to create your user.')
        while not name_accept:
            command = self.get_letter()
            if command == 'Delete':
                # Delete last character
                self.name = self.name[:len(self.name) - 1]
            elif command == 'Enter':
                # Return the name accepted by the user
                return self.name
            else:
                # Add letter to name
                self.name += command

    # Function used to get a single letter from the speech-recognition. Compares the given speech-input with
    # the predefined alphabet-list in order to process speech. Also checks for the defined commands for 'backspace'
    # and 'enter', namely 'Back' and 'Enter'.
    def get_letter(self):
        is_letter = False
        command = None
        while not is_letter:
            # Store speech in string
            command = str(self.recognizer.get_audio())
            # Check if user wants to erase last given letter
            if command == 'Back' or command == 'BACK' or command == 'back':
                return 'Delete'
            # Check if user is finished spelling username
            elif command == 'Enter' or command == 'ENTER' or command == 'enter'\
                    or command == 'Complete' or command == 'complete' or command == 'COMPLETE':
                return 'Enter'
            # Check the given speech-input with the alphabet-list
            else:
                for letter in self.alphabet:
                    if command is letter:
                        is_letter = True
        return command

    def set_news(self):
        print('Making ready to select news ..')
        command = None
        finished = False
        news_list = list()
        for attr in dir(news_keywords):
            if not (attr.startswith('__')):
                news_list.append(attr)