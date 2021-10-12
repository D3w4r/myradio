# Thesis Demonstration App

This project is for Project Laboratory (VITMAL01) on BME 6th semester, which was carried on to be a demonstrator app for
my thesis demonstration in the 7th semester.

***

# About

The project uses [Spotipy](https://spotipy.readthedocs.io/en/2.18.0/), [OpenWeatherMap](https://openweathermap.org/api)
and different TTS interfaces ([Azure TTS](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/index-text-to-speech), [Google TTS](https://cloud.google.com/text-to-speech)) to simulate an everyday radio broadcast with custom information elements.

-- TODO
***

# Python packages

There are too many dependencies regarding the used packages, therefore I included my whole list of packages on my
device.

*Use this command to import:*

```commandline
pip install -r requirements.txt
```

---

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

The OS does not recognize changes in environmental variables immediately, if you want your changes to take effect please
restart your device.

> If you are using PyCharm (JetBrains IDE) simply go to --> `Edit Configurations..` --> `Environmental variables` and set the values.

> If there are import errors in the source files please make sure to set the `working directory` to `{project_root}/src`.

### Secrets

-- TODO

### Spotify

For this module to work, you need to create the following environmental variables:
`SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, `SPOTIFY_REDIRECT_URI` each with the value of the coresponding secret key
for your Spotify Web Application. The `SPOTIFY_REDIRECT_URI` is `http://localhost:8080/`

***User Playback State modification only works with PREMIUM accounts***

> You can find more things about your API keys [here](https://developer.spotify.com/dashboard/applications).

Please use your own username in the code.

### Gmail API

For this part you will be needing the `credentails.json` file to be copied into `src/secrets`. After that, please authorize
the application to use the Gmail profile of your choice. If you see the following
sentence: `The authentication flow has completed. You may close this window.` the authorization was successful.

### Azure

For this code to work please create an environmental variable called `AZURE_TTS_ID`, with the matching API key.

### OpenWeatherMap

Lastly please create an environmental variable `OPENWEATHERMAP_ID` with your API key.

### OpenSSL

If you encounter an OpenSSL error on `Linux` follow
this [guide](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/how-to-configure-openssl-linux?pivots=programming-language-csharp)
.