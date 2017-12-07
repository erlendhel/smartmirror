#!/usr/bin/env/python3

# Python modules
from time import ctime, time, sleep
from datetime import datetime
from dateutil import parser
import _thread

# Kivy modules
import kivy
kivy.require('1.10.0')
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, ListProperty, DictProperty, ObjectProperty
from kivy.uix.image import Image
from kivy.uix.progressbar import ProgressBar
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.config import Config
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.screenmanager import SwapTransition

# Own modules
from weather import Weather
from news import News
from gmaps import travel
from facerec import facerec
import wrapper
from speech_rec import menu_speechrec
import arduino
from timer_module import time_module

# Set proper window size to fit iPad dimensions
Config.set('graphics', 'resizable',0)
Window.size = (int(600 / 1.13) ,int(800 / 1.13)) # (int(600 / 1.11) ,int(800 / 1.11)) => b = 15cm, l = 20cm

Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'borderless', 1)
Window.resizable = 0
Window.borderless = 1

Window.left = 0
Window.top = 0

# Create shared variables 
weather = Weather()
news = News.News()
travel = travel.Travel()
registration = wrapper.Wrapper()
menu_speech = menu_speechrec.MenuSpeech()
face_rec = None
tarduino = arduino.Arduino()
active_user = dict()
new_user_logged_in = False
guest_login = False

# This list contains a list of three preferred(chosen) sources.
# Fetched when login in by adding the news soruces from the user database
preferredNews = list()  

# This list of NewsArticles holds articles based on what icon is clicked
# The title will be displayed in the NewsSourceScreen as buttons
chosenTitles = list()

# This dict is set when a source title is clicked in the NewsSourceScreen
# Is set in TitleButton::set_article()
chosenArticle = dict()


def set_titles(source):
    articles = registration.get_articles_by_source(source)
    
    # Set the global variable to contain the articles based on what icon was clicked
    global chosenTitles
    chosenTitles = articles


# Used in several classes used to set weather image paths
def set_weather_image(description):
    length = len(description)

    # Because of the many different types of weather descriptions
    # The program will only look for the type of weather
    # i.e. it will not differentiate between 'heavy intensity rain' and 'shower rain'
    if description.find('rain', 0, length) is not -1:
        image_source = "icons/weather/rainy.png"
    elif description.find('clear sky', 0, length) is not -1:
        image_source = "icons/weather/sunny.png"
    elif description.find('few clouds', 0, length) is not -1:
        image_source = "icons/weather/partlysun.png"
    elif description.find('clouds') is not -1 and description.find('few clouds') is -1:
        image_source = "icons/weather/cloudy.png"
    elif description.find('snow', 0, length) is not -1:
        image_source = "icons/weather/snowy.png"
    elif description.find('thunder', 0, length) is not -1:
        image_source = "icons/weather/thunder.png"
    else:
        image_source = "icons/weather/cloudy.png"

    return image_source


class StartupScreen(Screen):
    first_startup = bool()
    progress_bar = ObjectProperty()
    started_recording = bool()
    wait = bool()
    progress_bar_created = False
    in_screen = bool()
    refill = bool()

    def __init__(self, **kwargs):
        super(StartupScreen, self).__init__(**kwargs)
        self.first_startup = True
        

    # On the first enter, wait 20 seconds to start recording audio
    # This is to avoid any unwanted commands on startup
    def on_enter(self):
        print("Entered startup screen")
        global guest_login
        guest_login = False
        self.in_screen = True
        if self.first_startup is True:
            _thread.start_new_thread(self.record_speech,("startup screen voicerecognition",20))
            self.first_startup = False
        else:
            _thread.start_new_thread(self.record_speech,("startup screen voicerecognition",1))
        
    # Runs in seperate thread
    def record_speech(self, threadName, delay):
        print("Getting ready to record voice in startup screen...")
        sleep(delay)
       
        # Create a new progress bar on every entry to the screen
        # This must be done to prevent some bugs with the bar sometimes freezing
        self.progress_bar = ProgressBar(max=100,value=100,pos=(0,-300))
        self.add_widget(self.progress_bar)
        self.progress_bar_created = True
        
        # If the microphone hasn't been closed, wait for it to close
        # Happens if the user uses the mouse to navigate instead of speech
        # as the voice recording thread in the screen left will finish the last
        # iteration of the while loop
        while menu_speech.is_busy():
            print("Microphone is busy, thread " + threadName + " sleeps for 0.5s")
            sleep(0.5)

        print("Starting thread " + threadName)
        
        # Start thread to continiously update the progress bar indicating when the user can speak
        _thread.start_new_thread(self.update_bar,("startup screen progressbar updater",0))

        # Listens for a command until it finds a valid one
        # Currently no action to enter the registration module
        valid_command = False
        while valid_command is False and self.in_screen is True:
            self.started_recording = True
            self.wait = False
            command = menu_speech.login_screen()
            self.started_recording = False
            if command == "login":
                #Set proper screen transition parameters
                self.parent.transition = SlideTransition()
                self.parent.transition.direction = 'left'
                self.parent.current = 'facerec'
                valid_command = True
            elif command == "guest":
                global guest_login
                guest_login = True

                #Set proper screen transition parameters
                self.parent.transiiton = SlideTransition()
                self.parent.transition.direction = 'left'
                self.parent.current = 'main'
                valid_command = True
            else:
                print("Did not recognize command")
        
        # Remove the progress bar when leaving the thread (i.e when leaving screen)
        # This is to prevent some bugs where the progress bar stops updating
        self.remove_widget(self.progress_bar)
        self.in_screen = False

    # Runs in seperate thread to update the progress bar
    # Used to indicate to user when the voice is recording
    def update_bar(self, threadName, delay):
        print("Starting thread "+ threadName)
        iterations = 225 
        self.wait = False
        timer = time_module.Timer()
        while self.in_screen is True:
            sleep(0.01)   
            if self.progress_bar.value <= 0 and self.refill is False:
                self.wait = True
                self.refill = True
                print("Time used to process voice: " + str(timer.get_time_in_seconds())[:3])
                timer.restart()
            elif self.started_recording is True and self.wait is False:
                if self.refill is True:
                    # Remove the previous bar and create a new one every time it empties
                    # To prevent bug where the bar freezes
                    self.refill = False
                    self.remove_widget(self.progress_bar)
                    self.progress_bar = ProgressBar(max=100,value=100,pos=(0,-300))
                    self.add_widget(self.progress_bar)

                # Slowly decrease the value of the progress bar
                self.progress_bar.value = self.progress_bar.value - self.progress_bar.max / iterations


    def on_leave(self):
        self.in_screen = False
        self.refill = False

            
class FaceRecognitionScreen(Screen):

    def __init__(self, **kwargs):
        super(FaceRecognitionScreen, self).__init__(**kwargs)
        global face_rec
        face_rec = facerec.FacialRecognition()

    # When this screen is entered, the camera will try to find
    # a user registered in the database
    def on_enter(self):
        print("Entered face recognition screen")
        # Start looking for a registered face
        user_id = face_rec.predict()
        if user_id is False:
            # Inform that no face was found
            feedback_text = "Face not recognized\n\n Returning to start screen"
            self.feedback = Label(text=feedback_text,font_size=40, halign='center')
            self.ids.facerec_grid.add_widget(self.feedback)
            # Remove status label
            self.ids.recognizing_label.text = ""
            # Go to the startup screen after a small delay
            Clock.schedule_once(self.go_to_startscreen, 10)
        else:
            global active_user
            active_user = registration.get_user(user_id)
            print("User " + active_user['name'] + " logged in!")
            
            news_list = [active_user['news_source_one'],active_user['news_source_two'],active_user['news_source_three']]
            global preferredNews
            preferredNews.clear()
            preferredNews = news.set_preferred_sources(news_list)

            # Used to set the news sources for the active user just once (first time entering main screen)
            global new_user_logged_in
            new_user_logged_in = True
            
            # Inform the user that he/she has sucessfully logged in
            feedback_text = "Face recognized\n\n Welcome " + active_user['name'] + "!"
            self.feedback = Label(text=feedback_text,font_size=40, halign='center')
            self.ids.facerec_grid.add_widget(self.feedback)
            # Remove status label
            self.ids.recognizing_label.text = ""
            # Go to the main application screen after a small delay
            Clock.schedule_once(self.go_to_mainscreen, 10)
            

    def go_to_mainscreen(self, *args):
        self.parent.current = "main"
        # Remove feedback label
        self.ids.facerec_grid.remove_widget(self.feedback)
        # Add status label so it will apear next time trying to log in
        self.ids.recognizing_label.text = "Recognizing face..."
        registration.set_news_sources(active_user['id'])
        

    def go_to_startscreen(self, *args):
        self.parent.current = "startup"
        # Remove feedback label
        self.ids.facerec_grid.remove_widget(self.feedback)
        # Add status label so it will apear next time trying to log in
        self.ids.recognizing_label.text = "Recognizing face..."
        

# Currently (07.12.2017)
class RegistrationScreen(Screen):
    
    
    def __init__(self, **kwargs):
        super(RegistrationScreen, self).__init__(**kwargs)
        

    def on_enter(self):
        self.ids.text_input.focus = True
        self.ids.step1.font_size = 25

    def create_facecapture_button(self):
        self.ids.grid.clear_widgets()
        self.ids.step1.font_size = 15
        self.ids.step2.font_size = 25
        self.ids.grid.add_widget(StartFaceCaptureButton(size_hint_y=0.2,
                                                        size_hint_x=0.2,
                                                        text="Press to start capturing images of face",
                                                        font_size=25,
                                                        background_color=[0,0,0,1]
                                                        ))
    
        

class SaveButton(Button):
    
    
    def __init__(self, **kwargs):
        super(SaveButton, self).__init__(**kwargs)
        
    def save_input(self, username_input):
        user.username = username_input
        user_id = registration.set_user_name(username_input)
        user.user_id = user_id

class StartFaceCaptureButton(Button):
    counter = 0
    
    def __init__(self, **kwargs):
        super(StartFaceCaptureButton, self).__init__(**kwargs)

    def on_release(self):
        self.text = "Capturing face..."  
        self.disabled = True
        
        # Go wait a few seconds before images are taken to ensure label is updated
        Clock.schedule_once(self.start_capturing_face, 5)
        

    def start_capturing_face(self, *args):
        if self.counter == 0:
            registration.add_user_face(user.user_id)
            self.text = "Face captured!"
        self.counter = self.counter + 1


class TestFaceImageButton(Button):
    pass


class FaceRegistrationScreen(Screen):
    pass


class MainScreen(Screen):
    # Variables used to control voice GUI
    progress_bar = ObjectProperty()
    started_recording = bool()
    wait = bool()
    in_screen = bool()
    refill = bool()
    
    
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

    def on_pre_enter(self):
        print("Loading main screen")
        global new_user_logged_in
        if new_user_logged_in is True:
            self.ids.icon_container.set_news_icons()
            self.ids.nav_label.set_destination_from_db()
            new_user_logged_in = False
    
    
    def on_enter(self):
        print("Entered main screen")

        # If the user logs in as guest, set predefined news-sources
        global guest_login
        if guest_login is True:
            print("Logged in as guest")
            news_list = ['daily-mail', 'the-new-york-times','mirror']
            global preferredNews
            preferredNews.clear()
            preferredNews = news.set_preferred_sources(news_list)
            self.ids.icon_container.set_news_icons()

            # Set news to active user so the speech recognition can be
            # used on news even though a guest is logged in
            active_user['news_source_one'] = news_list[0]
            active_user['news_source_two'] = news_list[1]
            active_user['news_source_three'] = news_list[2]
        else:
            # Update the news list in speechrecognition module so it knows
            # which commands to look for
            menu_speech.assign_pref_news(active_user['id'])
        self.in_screen = True
        
        # Start new thread listening for voice commands from the user
        _thread.start_new_thread(self.record_speech,("main screen-voicerecognition",0.5))
        
    # Runs in seperate thread
    def record_speech(self, threadName, delay):
        print("Getting ready to record voice")
        sleep(delay)
        
        # Create a progress bar on every entry of the screen
        # This is done to prevent some bugs where the bar freezes
        self.progress_bar = ProgressBar(max=100,value=100,pos=(0,-300))
        self.add_widget(self.progress_bar)
        self.progress_bar_created = True
        
        # Checks if the microfone is currently opened by another thread
        while menu_speech.is_busy():
            print("Microphone is busy, thread " + threadName + " sleeps for 0.5s")
            sleep(0.5)
        
        print("Starting thread " + threadName) 

        # Start new thread which continiously updates the progress bar
        # used to indicate to the user when he/she can speek
        _thread.start_new_thread(self.update_bar,("main screen progressbar updater",0))

        # Loop until a valid command is found, then enter new screen and exit thread
        valid_command = False
        while (valid_command is False) and (self.in_screen is True):
            self.started_recording = True
            self.wait = False
            command = menu_speech.main_menu_speech()
            self.started_recording = False
            if command == "weather":
                #Set proper screen transition parameters
                self.parent.transition = SlideTransition()
                self.parent.transition.direction = 'left'
                self.parent.current = 'weather'
                valid_command = True
            elif command == "settings":
                #Set proper screen transition parameters
                self.parent.transition = SlideTransition()
                self.parent.transition.direcetion = 'left'
                self.parent.current = 'settings'
                valid_command = True
            elif (command == active_user['news_source_one'] or\
                 command == active_user['news_source_two'] or \
                 command == active_user['news_source_three']):
                # Set the titles from the active users preferred news sources
                set_titles(command)

                #Set proper screen transition parameters
                self.parent.transition = SlideTransition()
                self.parent.transition.direction ='left'
                self.parent.current = 'source'
                valid_command = True
            elif command == "logout":
                global guest_login
                guest_login = False

                #Set proper screen transition parameters
                self.parent.transition = SwapTransition()
                self.parent.current = 'startup'
                valid_command = True
            elif command == "hello":
                global tarduino
                if tarduino.is_connected():
                    tarduino.write(b's')
            else:
                print("Did not recognize command")
                

        print("Leaving thread " + threadName)

        # Remove the progress bar when exiting the thread
        # To prevent freezing of the bar
        self.remove_widget(self.progress_bar)
        self.in_screen = False

    
    def update_bar(self, name, delay):
        print("Starting thread " + name)
        iterations = 225 
        self.wait = False
        self.refill = False
        timer = time_module.Timer()
        while self.in_screen:
            sleep(0.01)   
            if self.progress_bar.value <= 0 and self.refill is False:
                self.wait = True
                self.refill = True
                print("Time used to process voice: " + str(timer.get_time_in_seconds())[:3])
                timer.restart()
            elif self.started_recording is True and self.wait is False:
                if self.refill is True:
                    # Remove the previous bar and create a new one every timeit empties
                    # To prevent bug where the bar freezes
                    self.refill = False
                    self.remove_widget(self.progress_bar)
                    self.progress_bar = ProgressBar(max = 100, value=100, pos=(0,-300))
                    self.add_widget(self.progress_bar)

                # Slowly decrease the value of the progress bar
                self.progress_bar.value = self.progress_bar.value - self.progress_bar.max / iterations

        print("Leaving thread " + name)


    def on_leave(self):
        self.in_screen = False
        self.refill = False


class NavigationGrid(GridLayout):
    pass


class NavLabel(Label):
    travel_dict = DictProperty()
    travel_mode = StringProperty()

    def __init__(self, **kwargs):
        super(NavLabel, self).__init__(**kwargs)
        
        # Get the dict from the Travel interface, and set relevant variables
        result = travel.get_travel_time("Krona, Kongsberg", "driving")
        if result is not None:
            self.travel_dict = travel.get_travel_time("Krona, Kongsberg", "driving")
            self.travel_mode = self.travel_dict['travel_mode']

            # Get first word of string, quick fix of long destination name. 
            destination = self.travel_dict['destination_name'].split(' ', 1)[0]

            # Set the displayed text
            self.text = self.travel_dict['duration'] + " to " + destination

    def set_destination_from_db(self):
        
        result = travel.get_travel_time(active_user['destination'], active_user['travel_type'])
        if result is not None:
            self.travel_dict = travel.get_travel_time(active_user['destination'], active_user['travel_type'])
            self.travel_mode = self.travel_dict['travel_mode']

            # Get first word of string, quick fix of long destination name.
            destination = self.travel_dict['destination_name'].split(' ', 1)[0]

            # Set the displayed text
            self.text = self.travel_dict['duration'] + " to " + destination

class ClockLabel(Label):
    clock = StringProperty()

    def __init__(self, **kwargs):
        super(ClockLabel, self).__init__(**kwargs)
        self.clock = datetime.fromtimestamp(time()).strftime("%H:%M")
        Clock.schedule_interval(self.update_clock, 1)

    def update_clock(self, *args):
        self.clock = datetime.fromtimestamp(time()).strftime("%H:%M")
        self.text = self.clock


class DateLabel(Label):
    date = StringProperty()

    def __init__(self, **kwargs):
        super(DateLabel, self).__init__(**kwargs)
        self.date = datetime.fromtimestamp(time()).strftime("%B %d")

        # Update date label every second
        Clock.schedule_interval(self.update_date, 1)

    def update_date(self, *args):
        new_date = datetime.fromtimestamp(time()).strftime("%B %d")

        # Update date if it has changed since last call to the function
        if self.date != new_date:
            self.date = new_date
            self.text = new_date


class WeatherButton(Button):
    temperature = StringProperty()
    description = StringProperty()
    source = StringProperty()

    def __init__(self, **kwargs):
        super(WeatherButton, self).__init__(**kwargs)

        if weather.is_connected() is True:
            # Convert to int before string to cut out decimal points
            self.temperature = str(int(weather.getWeather().temperature)) + "°"
            self.description = weather.getWeather().weather_description
            self.source = set_weather_image(self.description)

        # Set a callback timer to send in a new requeset to the weather API every 10 minutes
        Clock.schedule_interval(self.update_temperature, 600)

    def update_temperature(self, *args):
        print("Updating temperature data")
        weather.updateCurrentData()

        if weather.is_connected() is True:
            # Convert to int before string to cut out decimal points
            self.temperature = str(int(weather.getWeather().temperature)) + "°"
            self.description = weather.getWeather().weather_description
            self.source = set_weather_image(self.description)


class WeatherGrid(GridLayout):
    pass


class WeatherLabel(Label):
    pass


class NewsButton(Button):
    preferredNewsIDs = ListProperty()

    def __init__(self, **kwargs):
        super(NewsButton, self).__init__(**kwargs)

        # Get the ids of the chosen preferred sources
        # These ids will be used to identify the different icons on the main screen
        for x in range(len(preferredNews)):
            self.preferredNewsIDs.append(preferredNews[x].source['source_id'])
            
    def set_news_icons(self):
        for x in range(len(preferredNews)):
            self.preferredNewsIDs.append(preferredNews[x].source['source_id'])


class SourceLayout(GridLayout):
    preferredNewsIDs = ListProperty()

    def __init__(self, **kwargs):
        super(SourceLayout, self).__init__(**kwargs)
        

    # Get the ids of the chosen preferred sources fetched from the user DB (or hard-coded if guest)
    # These ids will be used to identify the different icons on the main screen
    # Called when entering main screen
    def set_news_icons(self):
        global guest_login
        if guest_login is True:
            print("Setting news sources for guest")
        else:
            print("Setting " + active_user['name'] + "'s favorite news sources")
        self.clear_widgets()
        self.preferredNewsIDs.clear()

        # Loop through the preferredNews list and create three buttons with images
        for x in range(len(preferredNews)):
            self.preferredNewsIDs.insert(x,preferredNews[x].source['source_id'])
            button_background = "icons/news/" + str(self.preferredNewsIDs[x]) + ".png"
            self.add_widget(NewsIcon(background_normal=(button_background),
                                     background_down=(button_background),
                                     name=preferredNews[x].source['source_id']
                                     ))

            
        

class NewModule(Button):
    pass


class SettingButton(Button):
    
    def __init__(self, **kwargs):
        super(SettingButton, self).__init__(**kwargs)
    
    # Obsolete, the arduino is started by voice command
    def start_arduino(self):
        if tarduino.is_connected() is True:
            tarduino.write(b'12')

    

class NewsScreen(Screen):
    pass


class BackButton(Button):

    def __init__(self, **kwargs):
        super(BackButton, self).__init__(**kwargs)
        print("Back button created")

    def on_press(self):
        print("Back button was pressed")


class NewsIcon(Button):
    titles = ListProperty()
    name = StringProperty()

    def __init__(self, **kwargs):
        super(NewsIcon, self).__init__(**kwargs)
        

    def set_titles(self):
        # Set titles based on which button was pressed, self.name will pass a source id
        articles = registration.get_articles_by_source(self.name)
        self.titles = articles

        # Set the global variable to contain the articles based on what icon was clicked
        global chosenTitles
        chosenTitles = articles



# There are some bugs with the title buttons in the news source screen
# When it is entered with voice command. This does not happen when the news icon
# button is pushed. The bug also seem to be random so I have no idea of how to fix it
class NewsSourceScreen(Screen):
    titles = ListProperty()

    # Variables used to control voice GUI
    progress_bar = ObjectProperty()
    started_recording = bool()
    wait = bool()
    in_screen = bool()
    refill = bool()

    # Sets the titles based on what source is clicked from MainScreen
    # If the button is clicked by mouse, NewsIcon::set_titles() has appended
    # the proper titles to the global list variable chosenTitles
    # If navigating by voice, the global function set_titles() has appended
    # the titles to the chosenTitles list
    def on_pre_enter(self):
        print("Loading news source screen")
        # Set the titles to be displayed (dependent on chosen source)
        global chosenTitles
        self.titles = chosenTitles

        # Clear previous widgets in layout
        self.ids.grid.clear_widgets()
        self.ids.grid.add_widget(Image(source="icons/news/" + self.titles[0]['article_id'][:-1] + ".png"))
        

        # Add one button for each title in the source
        for i in range(len(self.titles)):
            title_text = self.titles[i]['title']

            # If the length of the title is to long, finish it off with "..."
            if len(title_text) > 55:
                title_text = title_text[:55] + "..."

            # Add the button to the layout. Button has name and id taken from the article dict
            # The id and name will be in the form of 'sourceXX' (e.g. bbc9 for the ninth article from bbc)
            button = TitleButton(text=title_text, id=self.titles[i]['article_id'])
            self.ids.grid.add_widget(button)


        # Add a button to go back to main screen
        self.ids.grid.add_widget(BackButton())

    def on_enter(self):
        self.in_screen = True
        _thread.start_new_thread(self.record_speech,("news screen voicerecognition",0.5))

    def record_speech(self, threadName, delay):
        print("Getting ready to record voice in news source screen...")
        sleep(delay)
        
        # Add a progress bar on entry of screen 
        self.progress_bar = ProgressBar(max=100,value=100,pos=(0,-290))
        self.add_widget(self.progress_bar)
        
        # If the microphone is opened by another thread, wait for it to finish
        while menu_speech.is_busy():
            print("Microphone is busy, thread " + threadName + " sleeps for 0.5s")
            sleep(0.5)

        print("Starting thread " + threadName)

        # Start thread to continiuosly update the progress bar
        # Used to indicate when the user can speek
        _thread.start_new_thread(self.update_bar,("news source screen progressbar updater",0))
        
        # Loop until a valid command has been found
        # Thread will exit, and the application will leave the current screen
        valid_command = False
        while valid_command is False and self.in_screen is True:
            self.started_recording = True
            self.wait = False
            command = menu_speech.back_speech()
            self.started_recording = False
            if command == "back":
                # Set parameters for screen transtition animation
                self.parent.transition.direction = 'right'
                self.parent.current = 'main'
                valid_command = True
            else:
                print("Did not recognize command")
                
        print("Leaving thread " + threadName)
        
        # Remove progress bar when leaving screen
        self.remove_widget(self.progress_bar)
        self.in_screen = False

    def update_bar(self, name, delay):
        print("Starting thread " + name)
        iterations = 225 
        self.wait = False
        self.refill = False
        timer = time_module.Timer()
        while self.in_screen:
            sleep(0.01)   
            if self.progress_bar.value <= 0 and self.refill is False:
                self.wait = True
                self.refill = True
                print("Time to used to process voice: " + str(timer.get_time_in_seconds())[:3])
                timer.restart()
            elif self.started_recording is True and self.wait is False:
                if self.refill is True:
                    self.refill = False
                    self.remove_widget(self.progress_bar)
                    self.progress_bar = ProgressBar(max=100,value=100,pos=(0,-290))
                    self.add_widget(self.progress_bar)

                # Slowly decrease the value of the progress bar
                self.progress_bar.value = self.progress_bar.value - self.progress_bar.max / iterations

        print("Leaving thread " + name)

    def on_leave(self):
        self.in_screen = False



class TitleButton(Button):
    article = DictProperty()

    def __init__(self, **kwargs):
        super(TitleButton, self).__init__(**kwargs)
        print("Created button: " + str(self.id))

    def set_article(self):
        print("Loading article with id: " + str(self.id))
        self.article = registration.get_article_by_id(self.id)
        global chosenArticle
        chosenArticle = self.article

    def on_press(self):
        print(str(self.id) + " was pressed")


class NewsArticleScreen(Screen):
    article = DictProperty()

    def __init__(self, **kwargs):
        super(NewsArticleScreen, self).__init__(**kwargs)

    # Sets the different labels in the screen based on what article is chosen
    # Before this function runs, TitleButton::set_article()
    # has set the global variable chosenArticle to contain
    # the correct article data based on what title is pushed
    def on_pre_enter(self):
        self.article = chosenArticle
        self.ids.title.text = self.article['title']

        # Convert the published string to simpler format
        published = self.article['published']
        if published is not None:
            # Parse string using dateutil module
            published = str(parser.parse(self.article['published']))

            # Remove last 9 chars of string
            published = published[:-9]
        else:
            published = "N/A"

        self.ids.published.text = "Published at: " + published
        if self.article['description'] is not None:
            self.ids.description.text = self.article['description']


class TitleLabel(Label):
    pass


class PublishedLabel(Label):
    pass


class DescriptionLabel(Label):
    pass


class WeatherScreen(Screen):
    # Variables used to control voice GUI
    progress_bar = ObjectProperty()
    started_recording = bool()
    wait = bool()
    in_screen = bool()
    refill = bool()
    
    def __init__(self, **kwargs):
        super(WeatherScreen, self).__init__(**kwargs)


    def on_pre_enter(self):
        print("Loading weather screen")

    def on_enter(self):
        print("Entered weather screen")
        self.in_screen = True
        _thread.start_new_thread(self.record_speech,("weather screen speechrecognition",1))

    def record_speech(self, threadName, delay):
        print("Getting ready to record voice in weather screen...")
        sleep(delay)
        
        # Create a progress bar when screen is entered
        self.progress_bar = ProgressBar(max=100,value=100,pos=(0,-310))
        self.add_widget(self.progress_bar)
        
        # If the microphone is opened by another thread, wait for it to finish
        while menu_speech.is_busy():
            print("Microphone is busy, thread " + threadName + " sleeps for 0.5s")
            sleep(0.5) 
        
        print("Starting thread " + threadName)
        
        # Start thread to update the value of the progress bar
        _thread.start_new_thread(self.update_bar,("weather screen progressbar updater",0))
       
        # Loop until a valid command has been recorded
        # or until the user leaves the screen via a mouse click
        valid_command = False
        while valid_command is False and self.in_screen is True:
            self.started_recording = True
            self.wait = False  
            command = menu_speech.weather_speech()
            self.started_recording = False
            if command == "back":
                # Set parameters for screen transtition animation
                self.parent.transition.direction = 'right'
                self.parent.current = 'main'
                valid_command = True
            else:
                print("Did not recognize command")
                
        print("Leaving thread " + threadName)

        # Remove the progress bar to prevent freezing bugs
        self.remove_widget(self.progress_bar)
        self.in_screen = False

    def update_bar(self, name, delay):
        print("Starting thread " + name)
        iterations = 225 
        self.wait = False
        self.refill = False
        timer = time_module.Timer()
        while self.in_screen:
            sleep(0.01)   
            if self.progress_bar.value <= 0 and self.refill is False:
                self.wait = True
                self.refill = True
                print("Time to used to process voice: " + str(timer.get_time_in_seconds())[:3])
                timer.restart()
            elif self.started_recording is True and self.wait is False:
                if self.refill is True:
                    self.refill = False
                    self.remove_widget(self.progress_bar)
                    self.progress_bar = ProgressBar(max=100,value=100,pos=(0,-310))
                    self.add_widget(self.progress_bar)

                # Slowly decrease the value of the progress bar
                self.progress_bar.value = self.progress_bar.value - self.progress_bar.max / iterations

        print("Leaving thread " + name)

    def on_leave(self):
        self.in_screen = False
        self.refill = False
            
    
class PresentWeatherLayout(GridLayout):
    temperature = StringProperty()
    humidity = StringProperty()
    sunrise = StringProperty()
    sunset = StringProperty()
    description = StringProperty()
    image_source = StringProperty()

    def __init__(self, **kwargs):
        super(PresentWeatherLayout, self).__init__(**kwargs)
        self.set_data()
        Clock.schedule_interval(self.update_current_weather, 600)

    def update_current_weather(self, *args):
        print("Updating current weather")
        weather.updateCurrentData()
        self.set_data()

    def set_data(self):
        
        if weather.is_connected() is True:
            self.temperature = str(int(weather.getWeather().temperature)) + "°"
            self.humidity = str(weather.getWeather().humidity) + "%"
            self.sunset = weather.getWeather().sunset
            self.sunrise = weather.getWeather().sunrise
            self.description = weather.getWeather().weather_description
            self.image_source = set_weather_image(self.description)


class DayWeatherLayout(GridLayout):
    day_forecast = ListProperty()

    def __init__(self, **kwargs):
        super(DayWeatherLayout, self).__init__(**kwargs)

        if weather.is_connected() is True:
            self.day_forecast = weather.getDailyForecast()

            for x in range(0, 7):
                layout = GridLayout(rows=3)
                source = set_weather_image(self.day_forecast[x].description)
                image = Image(source=source, allow_stretch=True)
                layout.add_widget(image)
                layout.add_widget(Label(text=str(self.day_forecast[x].temperature) + "°"))
                layout.add_widget(Label(text=self.day_forecast[x].time))
                self.add_widget(layout)


class WeekWeatherLayout(GridLayout):
    week_forecast = ListProperty()

    def __init__(self, **kwargs):
        super(WeekWeatherLayout, self).__init__(**kwargs)

        if weather.is_connected() is True:
            self.week_forecast = weather.getWeeklyForecast()

            for x in range(0, 7):
                layout = GridLayout(rows=3)
                source = set_weather_image(self.week_forecast[x].description)
                image = Image(source=source, allow_stretch=True)
                layout.add_widget(image)
                layout.add_widget(Label(text=str(self.week_forecast[x].temperature) + "°"))
                layout.add_widget(Label(text=self.week_forecast[x].date))
                self.add_widget(layout)


class SettingScreen(Screen):
    # Variables used to control voice GUI
    progress_bar = ObjectProperty()
    started_recording = bool()
    wait = bool()
    in_screen = bool()
    refill = bool()
    
    def __init__(self, **kwargs):
        super(SettingScreen, self).__init__(**kwargs)
        

    def on_enter(self):
        print("Entered setting screen")
        self.in_screen = True
        _thread.start_new_thread(self.record_speech,("setting screen speechrecognition",0.5))
        

    def record_speech(self, threadName, delay):
        print("Getting ready to record voice in settings screen...")
        sleep(delay)

        self.progress_bar = ProgressBar(max=100,value=100,pos=(0,-300))
        self.add_widget(self.progress_bar)

        while menu_speech.is_busy():
            print("Microphone is busy, thread " + threadName + " sleeps for 0.5s")
            sleep(0.5)
        
        print("Starting thread " + threadName) 

        _thread.start_new_thread(self.update_bar,("settings screen progressbar updater",0))
        
        valid_command = False
        while valid_command is False and self.in_screen is True:
            self.started_recording = True
            self.wait = False  
            command = menu_speech.back_speech()
            self.started_recording = False
            if command == "back":
                # Set screen transtition animation parameters
                self.parent.transition.direction = 'right'
                self.parent.current = 'main'
                valid_command = True
            else:
                print("Did not recognize command")
                

        print("Leaving thread " + threadName)
        self.remove_widget(self.progress_bar)
        self.in_screen = False
            

    
    def update_bar(self, name, delay):
        print("Starting thread " + name)
        iterations = 225 
        self.wait = False
        self.refill = False
        timer = time_module.Timer()
        while self.in_screen:
            sleep(0.01)   
            if self.progress_bar.value <= 0 and self.refill is False:
                self.wait = True
                self.refill = True
                print("Time used to process voice: " + str(timer.get_time_in_seconds())[:3])
                timer.restart()
            elif self.started_recording is True and self.wait is False:
                if self.refill is True:
                    self.refill = False
                    self.remove_widget(self.progress_bar)
                    self.progress_bar = ProgressBar(max=100,value=100,pos=(0,-300))
                    self.add_widget(self.progress_bar)

                self.progress_bar.value = self.progress_bar.value - self.progress_bar.max / iterations

        print("Leaving thread " + name)


    def on_leave(self):
        self.in_screen = False
        self.refill = False
        self.remove_widget(self.progress_bar)

    def on_pre_leave(self):
        self.in_screen = False
    


class LogoutButton(Button):
    pass

class ToothbrushButton(Button):
    pass

class ScreenManagement(ScreenManager):
    pass


class MirrorApp(App):

    def build(self):
        root = ScreenManagement()
        return root


if __name__ == '__main__':
    MirrorApp().run()
