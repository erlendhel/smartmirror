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
#Config.set('graphics', 'borderless', 1)
Window.resizable = 0
#Window.borderless = 1

Window.left = 0
Window.top = 0

# Create shared variables 
weather = Weather()
news = News.News()
travel = travel.Travel()
registration = wrapper.Wrapper()
menu_speech = menu_speechrec.MenuSpeech()
face_rec = None
arduino = arduino.Arduino()
active_user = None
new_user_logged_in = False

# This list contains a list of three preferred(chosen) sources.
# Fetched when login in by adding the news soruces from the user database
preferredNews = list()  

# This list of NewsArticles holds articles based on what icon is clicked
# The title will be displayed in the NewsSourceScreen as buttons
chosenTitles = list()

# This dict is set when a source title is clicked in the NewsSourceScreen
# Is set in TitleButton::set_article()
chosenArticle = dict()

# TODO: Might be removed??
class User():
    username = str()
    user_id = int()
    path_to_faceimg = str()

    def clear_all(self):
        username = ""
        user_id = None
        path_to_faceimg = ""

class VoiceWrapper():
    first_startup = bool()
    progress_bar = ObjectProperty()
    started_recording = bool()
    wait = bool()
    progress_bar_created = False
    in_screen = bool()


user = User()


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
        


    def on_enter(self):
        print("Entered startup screen")
        self.in_screen = True
        if self.first_startup is True:
            _thread.start_new_thread(self.record_speech,("menu-voice-recording",20))
            self.first_startup = False
        else:
            _thread.start_new_thread(self.record_speech,("menu-voice-recording",1))
        

    def record_speech(self, threadName, delay):
        print("Getting ready to record voice...")
        sleep(delay)
        print("Starting thread " + threadName)
        if self.progress_bar_created is False:
            self.progress_bar = ProgressBar(max=100,value=100,pos=(0,-300))
            self.add_widget(self.progress_bar)
            self.progress_bar_created = True
        
        _thread.start_new_thread(self.update_bar,("login screen progressbar updater",0))
        
        valid_command = False
        while valid_command is False and self.in_screen is True:
            self.started_recording = True
            self.wait = False
            command = menu_speech.login_screen()
            self.started_recording = False
            if command == "login":
                self.parent.current = 'facerec'
                valid_command = True
            elif command == "guest":
                self.parent.current = 'main'
                valid_command = True
            else:
                print("Did not recognize command")

                
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
                print(timer.get_time_in_seconds())
                timer.restart()
            elif self.started_recording is True and self.wait is False:
                if self.refill is True:
                    self.progress_bar.value = 100
                    self.refill = False
                self.progress_bar.value = self.progress_bar.value - self.progress_bar.max / iterations


    def on_leave(self):
        self.in_screen = False
        self.progress_bar.value = 100
        self.refill = False
        
        


                
            

    def update_progressbar(self, *args):
        if self.progress_bar.value <= 0:
            self.progress_bar.value = 100
        else:
            self.progress_bar.value = self.progress_bar.value - 7.5
            
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
        


class RegistrationScreen(Screen):
    user = User()
    
    
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
    first_startup = bool()
    progress_bar = ObjectProperty()
    started_recording = bool()
    wait = bool()
    progress_bar_created = False
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
        self.in_screen = True
        _thread.start_new_thread(self.record_speech,("main-screen-voice-recording",0.5))
        

    def record_speech(self, threadName, delay):
        print("Getting ready to record voice")
        sleep(delay)
        if self.progress_bar_created is False:
            self.progress_bar = ProgressBar(max=100,value=100,pos=(0,-300))
            self.add_widget(self.progress_bar)
            self.progress_bar_created = True
        print("Starting thread " + threadName) 

        _thread.start_new_thread(self.update_bar,("main screen progressbar updater",0))
        
        valid_command = False
        while valid_command is False and self.in_screen is True:
            self.started_recording = True
            self.wait = False  
            command = menu_speech.main_menu_speech()
            self.started_recording = False
            if command == "weather":
                self.parent.current = 'weather'
                valid_command = True
            elif command == "settings":
                self.parent.current = 'settings'
                valid_command = True
            elif command == "logout":
                self.parent.current = 'startup'
                valid_command = True
            else:
                print("Did not recognize command")
                

        print("Leaving thread " + threadName)
            

    
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
                print("Time to empty progressbar: " + str(timer.get_time_in_seconds()))
                timer.restart()
            elif self.started_recording is True and self.wait is False:
                if self.refill is True:
                    self.progress_bar.value = 100
                    self.refill = False
                self.progress_bar.value = self.progress_bar.value - self.progress_bar.max / iterations

        print("Leaving thread " + name)


    def on_leave(self):
        self.in_screen = False
        self.progress_bar.value = 100
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

            # Get first word of string, quick fix of long destination name. TODO: edit
            destination = self.travel_dict['destination_name'].split(' ', 1)[0]

            # Set the displayed text
            self.text = self.travel_dict['duration'] + " to " + destination

    def set_destination_from_db(self):
        
        result = travel.get_travel_time(active_user['destination'], active_user['travel_type'])
        if result is not None:
            self.travel_dict = travel.get_travel_time(active_user['destination'], active_user['travel_type'])
            self.travel_mode = self.travel_dict['travel_mode']

            # Get first word of string, quick fix of long destination name. TODO: edit
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
        
        '''for x in range(len(preferredNews)):
            print(x)
            self.preferredNewsIDs.append(preferredNews[x].source['source_id'])
        '''
        


    # Get the ids of the chosen preferred sources fetched from the user DB
    # These ids will be used to identify the different icons on the main screen
    # Called when entering main screen
    def set_news_icons(self):
        print("Setting " + active_user['name'] + "'s favorite news sources")
        self.clear_widgets()
        self.preferredNewsIDs.clear()
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

    def start_arduino(self):
        if arduino.is_connected() is True:
            arduino.write(b'12')


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


class NewsSourceScreen(Screen):
    titles = ListProperty()

    # Sets the titles based on what source is clicked from MainScreen
    # Before this function runs, NewsIcon::set_titles() has appended
    # the proper titles to the global list variable chosenTitles
    def on_pre_enter(self):
        #print("Loading news source screen")
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
        #print("Entered news source screen")
        pass

class TitleButton(Button):
    article = DictProperty()

    def __init__(self, **kwargs):
        super(TitleButton, self).__init__(**kwargs)
        print("Created title button with id: " + str(self.id))

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
    first_startup = bool()
    progress_bar = ObjectProperty()
    started_recording = bool()
    wait = bool()
    progress_bar_created = False
    in_screen = bool()
    refill = bool()
    
    def __init__(self, **kwargs):
        super(WeatherScreen, self).__init__(**kwargs)


    def on_pre_enter(self):
        print("Loading weather screen")

    def on_enter(self):
        print("Entered weather screen")
        self.in_screen = True
        _thread.start_new_thread(self.record_speech,("weather-screen-speech",1))

    def record_speech(self, threadName, delay):
        print("Getting ready to record voice")
        sleep(delay)
        print("Starting thread " + threadName)
        if self.progress_bar_created is False:
            self.progress_bar = ProgressBar(max=100,value=100,pos=(0,-310))
            self.add_widget(self.progress_bar)
            self.progress_bar_created = True
        
        _thread.start_new_thread(self.update_bar,("weather screen progressbar updater",0))
        
        valid_command = False
        while valid_command is False and self.in_screen is True:
            self.started_recording = True
            self.wait = False  
            command = menu_speech.weather_speech()
            self.started_recording = False
            if command == "back":
                self.parent.current = 'main'
                valid_command = True
            else:
                print("Did not recognize command")

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
                print("Time to empty progressbar: " + str(timer.get_time_in_seconds()))
                timer.restart()
            elif self.started_recording is True and self.wait is False:
                if self.refill is True:
                    self.progress_bar.value = 100
                    self.refill = False
                self.progress_bar.value = self.progress_bar.value - self.progress_bar.max / iterations

        print("Leaving thread " + name)

    def on_leave(self):
        self.in_screen = False
        self.progress_bar.value = 100
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


# TODO: How often should a callback update the daily forecast?
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


# TODO: How often should a callback update the weekly forecast?
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
    pass


class LogoutButton(Button):
    pass

    
class ScreenManagement(ScreenManager):
    pass


class MirrorApp(App):

    def build(self):
        root = ScreenManagement()
        return root


if __name__ == '__main__':
    MirrorApp().run()
