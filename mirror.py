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
from kivy.properties import NumericProperty, StringProperty, ListProperty, DictProperty
from kivy.uix.image import Image
from kivy.core.window import Window

from weather import Weather
from news import news

from time import ctime, time
from datetime import datetime
from dateutil import parser
from pprint import pprint

# TODO: Create drawing of tree-hierarchy

# TODO: program crashes if there is no internet connection
weather = Weather()
news = news.News()


# TODO: Wrap these global variables into a class?

# This list contains a list of three preferred(chosen) sources
preferredNews = news.set_preferred_sources()

# This list of NewsArticles holds articles based on what icon is clicked
# The title will be displayed in the NewsSourceScreen as buttons
chosenTitles = list()

# This dict is set when a source title is clicked in the NewsSourceScreen
# Is set in TitleButton::set_article()
chosenArticle = dict()





class MainScreen(Screen):
    pass

class NavigationGrid(GridLayout):
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
        self.date = datetime.fromtimestamp(time()).strftime("%B %d")
        Clock.schedule_interval(self.update_date, 1) # Check to see if new date every 1 second, if so, update it

    def update_date(self,*args):
        newDate = datetime.fromtimestamp(time()).strftime("%B %d")
        if  self.date !=  newDate:
            self.date = newDate
            self.text = newDate

class WeatherButton(Button):
    temperature = StringProperty()
    description = StringProperty()
    source = StringProperty()

    def __init__(self, **kwargs):
        super(WeatherButton, self).__init__(**kwargs)
        self.temperature = str(int(weather.getWeather().temperature)) + "°"  # Convert to int before string to cut out decimal points
        self.description = weather.getWeather().weather_description
        self.set_weather_image()
        Clock.schedule_interval(self.update_temperature, 600)  # Update weather data every 10 minutes


    def update_temperature(self, *args):
        weather.updateCurrentData()
        self.temperature = str(int(weather.getWeather().temperature)) + "°"  # Convert to int before string to cut out decimal points
        self.description = weather.getWeather().weather_description
        self.set_weather_image()

    def set_weather_image(self):
        length = len(self.description)
        # Because of the many different types of weather descriptions
        # The program will only look for the type of weather
        # i.e. it will not differentiate between 'heavy intensity rain' and 'shower rain'
        if self.description.find('rain', 0, length) is not -1:
            self.source = "icons/weather/rainy.png"
        elif self.description.find('clear sky', 0, length) is not -1:
            self.source = "icons/weather/sunny.png"
        elif self.description.find('few clouds', 0, length) is not -1:
            self.source = "icons/weather/partlysun.png"
        elif self.description.find('clouds') is not -1 and self.description.find('few clouds') is -1:
            self.source = "icons/weather/cloudy.png"
        elif self.description.find('snow', 0, length) is not -1:
            self.source = "icons/weather/snowy.png"
        elif self.description.find('thunder', 0, length) is not -1:
            self.source = "icons/weather/thunder.png"
        else:
            self.source = "icons/weather/cloudy.png"

class WeatherGrid(GridLayout):
    pass

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

class SourceLayout(GridLayout):
    preferredNewsIDs = ListProperty()

    def __init__(self, **kwargs):
        super(SourceLayout, self).__init__(**kwargs)

        # Get the ids of the chosen preferred sources
        # These ids will be used to identify the different icons on the main screen
        for x in range(len(preferredNews)):
            self.preferredNewsIDs.append(preferredNews[x].source['source_id'])
            print(self.preferredNewsIDs[x])

class NewModule(Button):
    pass

class SettingButton(Button):
    pass


class NewsScreen(Screen):
    pass


class BackButton(Button):
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



class NewsSourceScreen(Screen):
    titles = ListProperty()

    # Sets the titles based on what source is clicked from MainScreen
    # Before this function runs, NewsIcon::set_titles() has appended
    # the proper titles to the global list variable chosenTitles
    def on_pre_enter(self):
        # Set the titles to be displayed (dependent on chosen source)
        global chosenTitles
        self.titles = chosenTitles

        # Clear previous widgets in layout
        self.ids.grid.clear_widgets()
        self.ids.grid.add_widget(Image(source = "icons/news/" + self.titles[0]['article_id'][:-1] + ".png")) # Easy hack to refer to source name

        # Add one button for each title in the source
        for i in range(len(self.titles)):
            title_text = self.titles[i]['title']

            #If the length of the title is to long, finish it off with "..."
            if len(title_text) > 55:
                title_text = title_text[:55] + "..."
            # Add the button to the layout. Button has name and id taken from the article dict
            # The id and name will be in the form of 'sourceXX' (e.g. bbc9 for the ninth article from bbc)
            button = TitleButton(text=title_text, id = self.titles[i]['article_id'])
            self.ids.grid.add_widget(button)

        # Add a button to go back to main screen
        self.ids.grid.add_widget(BackButton())



class TitleButton(Button):
    article = DictProperty()

    def __init__(self,**kwargs):
        super(TitleButton, self).__init__(**kwargs)

    def set_article(self):
        self.article = news.get_article_by_id(self.id)
        global chosenArticle
        chosenArticle = self.article


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
        self.ids.description.text = self.article['description']

class TitleLabel(Label):
    pass

class PublishedLabel(Label):
    pass

class DescriptionLabel(Label):
    pass

class WeatherScreen(Screen):
    pass

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

    def update_current_weather(self):
        weather.updateCurrentData()
        self.set_data()

    def set_data(self):
        self.temperature = str(int(weather.getWeather().temperature)) + "°"
        self.humidity = str(weather.getWeather().humidity) + "%"
        self.sunset = weather.getWeather().sunset
        self.sunrise = weather.getWeather().sunrise
        self.description = weather.getWeather().weather_description
        self.set_weather_image()

    def set_weather_image(self):
        length = len(self.description)
        # Because of the many different types of weather descriptions
        # The program will only look for the type of weather
        # i.e. it will not differentiate between 'heavy intensity rain' and 'shower rain'
        if self.description.find('rain', 0, length) is not -1:
            self.image_source = "icons/weather/rainy.png"
        elif self.description.find('clear sky', 0, length) is not -1:
            self.image_source = "icons/weather/sunny.png"
        elif self.description.find('few clouds', 0, length) is not -1:
            self.image_source = "icons/weather/partlysun.png"
        elif self.description.find('clouds') is not -1 and self.description.find('few clouds') is -1:
            self.image_source = "icons/weather/cloudy.png"
        elif self.description.find('snow', 0, length) is not -1:
            self.image_source = "icons/weather/snowy.png"
        elif self.description.find('thunder', 0, length) is not -1:
            self.image_source = "icons/weather/thunder.png"
        else:
            self.image_source = "icons/weather/cloudy.png"



class DayWeatherLayout(GridLayout):
    day_forecast = ListProperty()


    # TODO: How often should a callback update the daily forecast?

    def __init__(self, **kwargs):
        super(DayWeatherLayout, self).__init__(**kwargs)
        self.day_forecast = weather.getDailyForecast()

        for x in range(0,7):
            layout = GridLayout(rows = 3)
            source = self.set_weather_image(self.day_forecast[x].description)
            image = Image(source = source, allow_stretch = True)
            layout.add_widget(image)
            layout.add_widget(Label(text = str(self.day_forecast[x].temperature)+"°"))
            layout.add_widget(Label(text = self.day_forecast[x].time))
            self.add_widget(layout)

    def set_weather_image(self,description):
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


class WeekWeatherLayout(GridLayout):
    week_forecast = ListProperty()

    # TODO: How often should a callback update the weekly forecast?

    def __init__(self,**kwargs):
        super(WeekWeatherLayout, self).__init__(**kwargs)
        self.week_forecast = weather.getWeeklyForecast()

        for x in range(0,7):
            layout = GridLayout(rows = 3)
            source = self.set_weather_image(self.week_forecast[x].description)
            image = Image(source=source, allow_stretch=True)
            layout.add_widget(image)
            layout.add_widget(Label(text = str(self.week_forecast[x].temperature)+"°"))
            layout.add_widget(Label(text = self.week_forecast[x].date))
            self.add_widget(layout)

    def set_weather_image(self,description):
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

class SettingScreen(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass


class MirrorApp(App):
    def build(self):
        root = ScreenManagement()
        return root


if __name__ == '__main__':
    Window.size = (450, 700)
    MirrorApp().run()
