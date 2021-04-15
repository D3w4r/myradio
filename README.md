# myradio

This project is for Project Laboratory (VITMAL01) on BME 6th semester.

# About

MyRadio uses [spotipy](https://spotipy.readthedocs.io/en/2.18.0/), [OpenWeatherMap](https://openweathermap.org/api)
and [Azure TTS](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/index-text-to-speech) (Free
License!) to simulate an everyday radio broadcast. The project utilizes Neural Networks to select intresting topics for
the user, through an RSS feed from [telex.hu](https://telex.hu/)

# Python packages used in this project
> These are not included by default
* spotipy
* geopy
* azure-cognitiveservices-speech
* python-vlc
* feedparser
* oogle-api-python-client 
* google-auth-httplib2
* google-auth-oauthlib

**Please note, that you need to use your own API keys for Azure TTS and OpenWeatherMap**