import kivy
kivy.require('1.10.0')
from pprint import pprint
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Line
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scatter import Scatter
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.uix.image import Image

from kivy.core.window import Window
Window.size = (450,700)

from weather import Weather
from news import news

from time import ctime, time
from datetime import datetime
from news import news



weather = Weather()
news = news.News()

# This list contains a list of three preferred(chosen) sources
preferredNews = news.set_preferred_sources()

# This list of NewsArticles holds articles based on what icon is clicked
# The title will be displayed in the NewsSourceScreen as buttons
chosenTitles = list()




class MainScreen(Screen):
    pass

class ClockLabel(Label):
    clock = StringProperty()

    def __init__(self,**kwargs):
        super(ClockLabel, self).__init__(**kwargs)
        self.clock = datetime.fromtimestamp(time()).strftime("%H:%M")
        Clock.schedule_interval(self.update_clock,1)

    def update_clock(self, *args):
        self.clock = datetime.fromtimestamp(time()).strftime("%H:%M")
        self.text = self.clock

class DateLabel(Label):
    date = StringProperty()

    def __init__(self,**kwargs):
        super(DateLabel, self).__init__(**kwargs)
        self.date = datetime.fromtimestamp(time()).strftime("%d %b %Y")
        Clock.schedule_interval(self.update_date,1) # Check to see if new date every 1 second, if so, update it

    def update_date(self,*args):
        newDate = datetime.fromtimestamp(time()).strftime("%d %b %Y")
        if  self.date !=  newDate:
            self.date = newDate
            self.text = newDate

class WeatherButton(Button):
    temperature = StringProperty()

    def __init__(self, **kwargs):
        super(WeatherButton, self).__init__(**kwargs)
        self.temperature = str(int(weather.getTemperature())) + "°"  # Convert to int before string to cut out decimal points
        Clock.schedule_interval(self.update_temperature, 600)  # Update weather data every 10 minutes

    def update_temperature(self):
        weather.updateCurrentData()
        temperature = str(int(weather.getTemperature())) + "°"  # Convert to int before string to cut out decimal points
        self.text = temperature

class WeatherLabel(Label):
    pass

class NewsButton(Button):
    preferredNewsIDs = ListProperty()


    def __init__(self,**kwargs):
        super(NewsButton, self).__init__(**kwargs)

        # Get the ids of the chosen preferred sources
        # These ids will be used to identify the different icons on the main screen
        for x in range(len(preferredNews)):
            self.preferredNewsIDs.append(preferredNews[x].source['source_id'])

class IconContainer(GridLayout):
    pass


class NewsIcon(Button):
    titles = ListProperty()

    def __init__(self, **kwargs):
        super(NewsIcon, self).__init__(**kwargs)


    def set_titles(self):
        #Set titles based on which button was pressed, self.name will pass a source id
        articles = news.get_articles_by_source(preferredNews, self.name)
        self.titles = articles

        # Set the global variable to contain the articles based on what icon was clicked
        global chosenTitles
        chosenTitles = articles




class SettingButton(Button):
    pass


class NewsScreen(Screen):
    pass

class TitleButton(Button):
    pass

class NewsSourceScreen(Screen):
    titles = ListProperty()

    def on_pre_enter(self):
        global chosenTitles
        self.titles = chosenTitles

        self.ids.grid.clear_widgets()
        for i in range(len(self.titles)):
            text = self.titles[i]['title']
            button_text = str()
            if len(text) > 60:
                button_text = text[:60] + "..."
                text = button_text
            button = TitleButton(text=text)

            self.ids.grid.add_widget(button)


class WeatherScreen(Screen):
    pass

class SettingScreen(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass

class DrawInput(Widget):
    def on_touch_down(self, touch):
        with self.canvas:
            touch.ud["line"] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        touch.ud["line"].points += (touch.x, touch.y)


class MirrorApp(App):
    def build(self):
        root = ScreenManagement()
        return root


if __name__ == '__main__':
    MirrorApp().run()
