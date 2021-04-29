# MyRadio

This project is for Project Laboratory (VITMAL01) on BME 6th semester.

# About

MyRadio uses [Spotipy](https://spotipy.readthedocs.io/en/2.18.0/), [OpenWeatherMap](https://openweathermap.org/api)
and [Azure TTS](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/index-text-to-speech) (Free
License!) to simulate an everyday radio broadcast. The project in the future may utilize Neural Networks to select
intresting topics for the user, through an RSS feed from [telex.hu](https://telex.hu/)

# Python packages used in this project

> These may not be included by default

* spotipy
* geopy
* azure-cognitiveservices-speech
* feedparser
* google-api-python-client
* google-auth-httplib2
* google-auth-oauthlib
* pprint
* pickle

Or just use

```
pip install -r requirements.txt
```

**Important:** ``requirements.txt`` contains every dependency of the packages listed above!

**Please note, that you need to use your own API keys for Azure TTS and OpenWeatherMap**

# Installation Guide

### Spotify

