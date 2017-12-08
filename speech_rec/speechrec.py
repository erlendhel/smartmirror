import speech_recognition as sr

class SpeechRecognition(object):
    recognizer = None
    busy = bool()

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.busy = False

    def get_audio(self):
        print('Recording start')
        with sr.Microphone() as source:
            print('Speak')
            self.busy = True
            audio = self.recognizer.record(source, duration = 3)
            try:
                print('Google is processing voice...')
                command = self.recognizer.recognize_google(audio)
                print(command)
                self.busy = False
                return command
            except sr.UnknownValueError:
                print('Could not understand audio')
                self.busy = False
                return None
            except sr.RequestError as e:
                print('Could not request results; {0}'.format(e))
                self.busy = False
                return None

    def is_busy(self):
        return self.busy

