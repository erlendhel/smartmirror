import pyaudio
import speech_recognition as sr

class SpeechRecognition(object):
    recognizer = None

    def __init__(self):
        self.recognizer = sr.Recognizer()

    def get_audio(self):
        while True:
            print('Recording start')
            with sr.Microphone() as source:
                print('Speak')
                audio = self.recognizer.record(source, duration = 3)
                try:
                    print('Inside try')
                    command = self.recognizer.recognize_google(audio)
                    print(command)
                    return command
                except sr.UnknownValueError:
                    print('Could not understand audio')
                except sr.RequestError as e:
                    print('Could not request resuslts; {0}'.format(e))


