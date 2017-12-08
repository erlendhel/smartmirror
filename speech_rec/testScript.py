import speech_recognition as sr

r = sr.Recognizer()
while True:
    print('Starting record')
    with sr.Microphone() as source:
        audio = r.record(source, duration = 5)
        print('Speak:')
        #audio = r.listen(source)
        try:
            print('Inside try')
            command = r.recognize_google(audio)
            print(command)
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print('Could not request')
    print('Record ended')
# with open("microphone-results.wav", "wb") as f:
#    f.write(audio.get_wav_data())


