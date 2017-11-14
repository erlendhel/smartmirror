import speech_recognition as sr


# Class used in order to get and process audio inputs given by the user.
class SpeechRecognition(object):
    recognizer = None

    def __init__(self):
        self.recognizer = sr.Recognizer()

    # Function to get audio from microphone
    def get_audio(self):

        while True:
            # Get audio from microphone
            with sr.Microphone() as source:
                print('Speak:')
                audio = self.recognizer.listen(source)
            try:
                command = self.recognizer.recognize_google(audio)
                return command
            except sr.UnknownValueError:
                print('Could not understand audio')
            except sr.RequestError as e:
                print('Could not request results; {0}'.format(e))
