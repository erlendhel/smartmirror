import pyaudio
from subprocess import call
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
            with sr.Microphone(device_index = 2, sample_rate = 44100, chunk_size = 512) as source:
                print(sr.Microphone())
                print(sr.Microphone().get_pyaudio())
                print(sr.Microphone().list_microphone_names())
                print(sr.Microphone().format)
                print(sr.Microphone().CHUNK)
                print(sr.Microphone().device_index)
                print(sr.Microphone().SAMPLE_RATE)
                print('Speak:')
                audio = self.recognizer.listen(source)
                print('Done')
            try:
                print('Entered TRY')
                command = self.recognizer.recognize_google(audio)
                print(command)
                return command
            except sr.UnknownValueError:
                print('Could not understand audio')
            except sr.RequestError as e:
                print('Could not request results; {0}'.format(e))

if __name__ == "__main__":
    speech = SpeechRecognition()
    speech.get_audio()
