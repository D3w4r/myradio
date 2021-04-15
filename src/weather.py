import json
import os

import requests
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer
from azure.cognitiveservices.speech.audio import AudioOutputConfig

from geopy.geocoders import Nominatim


class Weather:
    """This class manages weather info through the OpenWeatherMap API"""

    api_key = os.environ.get('OPENWEATHERMAP_ID')

    def __init__(self, city):
        self.city = city

    def city(self):
        return self.city

    def location(self):
        print(f'Getting coordinates for {self.city}')
        geolocator = Nominatim(user_agent='weatherapp')
        return geolocator.geocode(self.city).latitude, geolocator.geocode(self.city).longitude

    def weather_info(self):
        print('Getting weather info...')
        location = self.location()
        url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric&lang=%s" % (
            location[0], location[1], self.api_key, "hu")

        response = requests.get(url)
        return json.loads(response.text)
