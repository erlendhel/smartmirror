import  urllib.request
import  urllib.parse
import json
from pprint import pprint
from time import ctime, time
from datetime import datetime

class ForecastWeatherData:

    date = str()
    temperature = int()
    description = str()

    def __repr__(self):
        return "[" + self.date + ", " + str(self.temperature) + ", " + self.description +  "]"

class WeatherData:

    temperature = None
    humidity = None
    sunrise = None
    sunset = None
    weather_description = None

    def __repr__(self):
        return "["+ str(int(self.temperature))+"°, "+ self.weather_description+"]" #To int before string to remove decimal points

class Weather:

    #API Data
    __api_key = "2a046a8a4775bd310aedf02cfd2519ae"
    __current_weather_url = str()
    __forecast_url = str()
    __kongsberg_id = "6453373"

    #Current weather data
    __current_dict = dict()
    __weather_data = WeatherData()

    #Forecast data
    __forecast_dict = dict()
    __forecast_7days = list()


    def __init__(self):
        self.__current_weather_url = "http://api.openweathermap.org/data/2.5/weather?id="+self.__kongsberg_id+"&APPID="+self.__api_key
        self.__forecast_url = "http://api.openweathermap.org/data/2.5/forecast/daily?id="+self.__kongsberg_id+"&APPID="+self.__api_key
        self.updateCurrentData()
        self.updateForecastData()

    def getWeatherJSON(self):
        return self.__current_dict

    def getForecastJSON(self):
        return self.__forecast_dict

    #Returns a WeatherData object
    def getWeather(self):
        return self.__weather_data

    def getSunset(self):
        return self.__weather_data.sunset

    def getSunrise(self):
        return self.__weather_data.sunrise

    def getTemperature(self):
        return self.__weather_data.temperature

    def getHumidity(self):
        return self.__weather_data.humidity

    def getWeatherDescription(self):
        return self.__weather_data.weather_description

    def getCity(self):
        return self.__current_dict['name']

    # Returns a list containing 7 ForecastWeatherData objects, i.e. the temperature
    # and description for the next 7 days (including current day)
    def getForecastList(self):
        return self.__forecast_7days

    def updateCurrentData(self):
        # get data from url
        with urllib.request.urlopen(self.__current_weather_url) as response:
            self.__current_dict = json.loads(response.read().decode())

        # put data into WeatherData object
        main_dict = self.__current_dict['main']
        self.__weather_data.sunset = ctime(self.__current_dict['sys']['sunset'])
        self.__weather_data.sunrise = ctime(self.__current_dict['sys']['sunrise'])
        self.__weather_data.temperature = main_dict['temp'] - (272.15)
        self.__weather_data.humidity = main_dict['humidity']
        self.__weather_data.weather_description = self.__current_dict['weather'][0]['description']

    def updateForecastData(self):
        # get data from url
        with urllib.request.urlopen(self.__forecast_url) as response:
            self.__forecast_dict = json.loads(response.read().decode())

        # put data into list of ForecastWeatherData objects
        for x in self.__forecast_dict['list']:
            forecastData = ForecastWeatherData()
            forecastData.date = datetime.fromtimestamp(x['dt']).strftime("%m%d")
            forecastData.temperature = int(x['temp']['day'] - 272) #Kelvin to Celsius
            forecastData.description = self.__fillDescriptions(x)
            self.__forecast_7days.append(forecastData)

    def __fillDescriptions(self,weatherList):
        for x in weatherList['weather']:
            return x['description']







