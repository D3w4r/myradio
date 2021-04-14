import json
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

    def current_weather_generate_text(self, language=None):
        data = self.weather_info()
        print('Creating sentence for TTS interface...')
        if language is None:
            raise RuntimeError("Please specify a language!")
        if language == 'en-EN':
            text = "It's currently " + str(data["current"]["temp"]) + " degrees, but it feels like " + str(
                data["current"]["feels_like"]) + " degrees outside. The description of the weather is " + str(
                data["current"]["weather"][0]["description"]) + ". Wind speed is " + str(
                data["current"]["wind_speed"]) + " kilometers an hour."
            return text
        if language == 'hu-HU':
            text = "Jelenleg " + str(data["current"]["temp"]) + "fok van, ami " + str(
                data["current"]["feels_like"]) + " foknak érződik. Az időjárás leírása: " + str(
                data["current"]["weather"][0]["description"]) + ". A szél sebessége " + str(
                data["current"]["wind_speed"]) + " kilóméter per óra."
            return text

    def synthesise(self, path, language, voice):
        print('Synthesising speech...')
        audio_config = AudioOutputConfig(filename=path)
        self.speech_config.speech_synthesis_language = language
        self.speech_config.speech_synthesis_voice_name = voice
        synthesizer = SpeechSynthesizer(speech_config=self.speech_config, audio_config=audio_config)
        synthesizer.speak_text_async(self.current_weather_generate_text(language))
