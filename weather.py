import  urllib.request
import  urllib.parse
import json
from pprint import pprint
from time import ctime, time
from datetime import datetime

class WeekForecastWeatherData:

    date = str()
    temperature = int()
    description = str()

    def __repr__(self):
        return "[" + self.date + ", " + str(self.temperature) + "°, " + self.description +  "]"

class DayForecastWeatherData:

    time = str()
    temperature = int()
    description = str()

    def __repr__(self):
        return "[" + self.time + ", " + str(self.temperature) + "°, " + self.description + "]"

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
    __forecast_day_url = str()
    __kongsberg_id = "6453373"

    #Current weather data
    __current_dict = dict()
    __weather_data = WeatherData()

    # Week Forecast data
    __forecast_week_dict = dict()
    __forecast_7days = list()

    # Day forecast data
    __forecast_day_dict = dict()
    __forecast_day = list()


    def __init__(self):
        self.__current_weather_url = "http://api.openweathermap.org/data/2.5/weather?id="+self.__kongsberg_id+"&APPID="+self.__api_key
        self.__forecast_url = "http://api.openweathermap.org/data/2.5/forecast/daily?id="+self.__kongsberg_id+"&APPID="+self.__api_key
        self.__forecast_day_url = "http://api.openweathermap.org/data/2.5/forecast?id="+self.__kongsberg_id+"&APPID="+self.__api_key
        self.updateCurrentData()
        self.updateWeekForecastData()
        self.updateDayForecastData()


    def getWeatherJSON(self):
        return self.__current_dict


    def getWeekForecastJSON(self):
        return self.__forecast_weeek_dict


    def getDayliyForecastJSON(self):
        return self.__forecast_day_dict


    #Returns a WeatherData object
    def getWeather(self):
        return self.__weather_data


    # Returns a list containing 8 DayForecastWeatherData objects, i.e. the temperature
    # and description for the next 24h (3h intervals)
    def getDailyForecast(self):
        return self.__forecast_day


    # Returns a list containing 7 WeekForecastWeatherData objects, i.e. the temperature
    # and description for the next 7 days (including current day)
    def getWeeklyForecast(self):
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


    def updateWeekForecastData(self):
        # get data from url
        with urllib.request.urlopen(self.__forecast_url) as response:
            self.__forecast_week_dict = json.loads(response.read().decode())

        # put data into list of WeekForecastWeatherData objects
        for day in self.__forecast_week_dict['list']:
            forecastData = WeekForecastWeatherData()
            forecastData.date = datetime.fromtimestamp(day['dt']).strftime("%m%d")
            forecastData.temperature = int(day['temp']['day'] - 272) #Kelvin to Celsius
            forecastData.description = self.__fillDescriptions(day)
            self.__forecast_7days.append(forecastData)


    def updateDayForecastData(self):
        # get data from url
        with urllib.request.urlopen(self.__forecast_day_url) as response:
            self.__forecast_day_dict = json.loads(response.read().decode())

        # put data into list of 8 DayForecastWeatherData objects
        for index in range(0,8):
            listItem = self.__forecast_day_dict['list']
            forecastData = DayForecastWeatherData()
            forecastData.time = datetime.fromtimestamp(listItem[index]['dt']).strftime("%H:%M")
            forecastData.temperature = int(listItem[index]['main']['temp'] - 272) #Kelvin to Celsius
            forecastData.description = self.__fillDescriptions(listItem[index])
            self.__forecast_day.append(forecastData)


    def __fillDescriptions(self,weatherList):
        for x in weatherList['weather']:
            return x['description']



# An example of the use of the weather interface
if __name__ == "__main__":
    test = Weather()
    print("Current: ",test.getWeather())
    print("Daily forecast: ", test.getDailyForecast())
    print("Weekly forecast: ", test.getWeeklyForecast())


