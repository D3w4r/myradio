# MyRadio

This project is for Project Laboratory (VITMAL01) on BME 6th semester.

***

# About

MyRadio uses [Spotipy](https://spotipy.readthedocs.io/en/2.18.0/), [OpenWeatherMap](https://openweathermap.org/api)
and [Azure TTS](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/index-text-to-speech) (Free
License!) to simulate an everyday radio broadcast. The project in the future may utilize Neural Networks to select
intresting topics for the user, through an RSS feed from [telex.hu](https://telex.hu/)

***

# Python packages

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

```commandline
pip install -r requirements.txt
```

**Important:** ``requirements.txt`` contains every dependency of the packages listed above!

**Please note, that you need to use your own API keys for Azure TTS and OpenWeatherMap**

***

# Installation Guide

*If you want to test a module, simply run it!*

You can create an environmental variable on `Linux` with:

```
export VARIABLE_NAME='value'
```

or on `Windows`:

```
SET VARIABLE_NAME='value'
```

You may have to restart your computer after this!

> If you are using PyCharm simply go to --> `Edit Configurations..` --> `Environmental variables` and set the values.

> Please make sure the project working directory is set to the `src` folder in your IDE, otherwise the code will not recognize the given paths for specific files.

### Spotify

You can find custom functions in `client.py`. This code uses the Spotipy API. You can find the documentation under
the `About` section of this document.

For this module to work, you need to create the following environmental variables:
`SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, `SPOTIFY_REDIRECT_URI` each with the value of the coresponding secret key
for your Spotify Web Application. The `SPOTIFY_REDIRECT_URI` is `http://localhost:8080/`

***Please note that User Playback State modification only works with PREMIUM accounts***

> You can find your API keys at [this link](https://developer.spotify.com/dashboard/applications).

### Gmail API

For this part you will be needing the `credentails.json` file to be copied into `src/auth`. After that, please authorize
the application to use the Gmail profile of your choice. If you see the following
sentence: `The authentication flow has completed. You may close this window.` the authorization was succesful.

### Azure

For this code to work please create an environmental variable called `AZURE_TTS_ID`, with the matching API key.

### OpenWeatherMap

Lastly please create an environmental variable `OPENWEATHERMAP_ID` with your API key.

### OpenSSL

If you encounter an OpenSSL error on `Linux` follow
this [guide](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/how-to-configure-openssl-linux?pivots=programming-language-csharp).