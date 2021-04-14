import json
import logging
import os

import requests
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from geopy.geocoders import Nominatim


class Weather:
    """This class manages weather info through the OpenWeatherMap API"""

    api_key = os.environ.get('OPENWEATHERMAP_ID')
    speech_config = SpeechConfig(subscription=os.environ.get('AZURE_TTS_ID'), region='westeurope')

    def __init__(self, city):
        self.city = city

    def getCity(self):
        return self.city

    def getLocation(self):
        logging.info(f'Getting coordinates for {self.city}')
        geolocator = Nominatim(user_agent='weatherapp')
        return geolocator.geocode(self.city).latitude, geolocator.geocode(self.city).longitude

    def getWeatherInfo(self):

        location = self.getLocation()
        url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (
            location[0], location[1], self.api_key)

        response = requests.get(url)
        return json.loads(response.text)

    def getCurrentWeatherText(self):
        data = self.getWeatherInfo()
        logging.info('Creating sentence for TTS interface...')
        text = "It's currently " + str(data["current"]["temp"]) + " degrees, but it feels like " + str(
            data["current"]["feels_like"]) + " degrees outside. Expect " + str(
            data["current"]["weather"][0]["main"]) + " weather. Wind speed is " + str(
            data["current"]["wind_speed"]) + " kilometers an hour."
        return text

    def synthesise(self, path):
        logging.info('Synthesising speech')
        audio_config = AudioOutputConfig(filename=path)
        synthesizer = SpeechSynthesizer(speech_config=self.speech_config, audio_config=audio_config)
        synthesizer.speak_text_async(self.getCurrentWeatherText())
