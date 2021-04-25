import json
import os

import requests
from geopy.geocoders import Nominatim


class Weather:
    """This class manages weather info through the OpenWeatherMap API"""

    api_key = os.environ.get('OPENWEATHERMAP_ID')

    def __init__(self, city):
        self.city = city

    def city(self):
        """
        :return: the city of this object.
        """
        return self.city

    def location(self):
        """
        Get the location of self.city
        :return: tuple of location coordinates
        """
        print(f'Getting coordinates for {self.city}')
        geolocator = Nominatim(user_agent='weatherapp')
        return geolocator.geocode(self.city).latitude, geolocator.geocode(self.city).longitude

    def weather_info(self):
        """
        :return: the weather info in json format
        """
        print('Getting weather info...')
        location = self.location()
        url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric&lang=%s" % (
            location[0], location[1], self.api_key, "hu")

        response = requests.get(url)
        return json.loads(response.text)
