# Thesis Demonstration App

This project is for Project Laboratory (VITMAL01) on BME 6th semester, which was carried on to be a demonstrator app for
my thesis demonstration in the 7th semester.

***

# About

***

# Python packages

Please use the command below to import dependencies used by this project.

```commandline
pip install -r requirements.txt
```

---

# Installation Guide

### Environmental variables

First please import the environment variables, which are crucial to the project. I've included them in `project.zip`

You can set an environmental variable on `Linux` with:

```
export VARIABLE_NAME='value'
```

or on `Windows`:

```
SET VARIABLE_NAME='value'
```

If you are running the code on CLI and you set the variables using the commands above don't restart your console,
because the changes will be lost.

> If you are using PyCharm (JetBrains IDE) simply go to > `Edit Configurations..` > `Environmental variables` and set the values. \
> If you are running the code via CLI these might not be recognized.

### Secrets and cache

Please create a folder named secrets under ``src/``. Place the files I've sent you here.
Please create a folder named ``src/cache``.

### Spotify

For this module to work, you need to create the following environmental variables:
`SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, `SPOTIFY_REDIRECT_URI` each with the value of the corresponding secret key
for your Spotify Web Application. The `SPOTIFY_REDIRECT_URI` is `http://localhost:8080/`

***User Playback State modification only works with PREMIUM accounts***

> You can find more things about your API keys [here](https://developer.spotify.com/dashboard/applications).

Please use your own username in the code.

### Gmail API

> You will need to retake the following steps each time your acces token expires.

For this part you will be needing the `credentails.json` file to be copied into `src/secrets/`. After that, please
authorize the application to use the Gmail profile of your choice. Please choose `Continue` on the appearing broswer
window. The next steps are trivial.

If you see the following sentence: `The authentication flow has completed. You may close this window.` the authorization
was successful.

After some time the code will raise an Excpetion from the Gmail API. If you encounter this, please
delete `src/secrets/token.pickle`.

### Azure and Google TTS

For Azure to work please create an environmental variable called `AZURE_TTS_ID`, with the matching API key (included in the zip).

For Google please copy `google_tts_credentials.json` to `src/secrets`.

### OpenWeatherMap

Lastly please create an environmental variable `OPENWEATHERMAP_ID` with your API key (included in the zip).

### OpenSSL

If you encounter an OpenSSL error on `Linux` follow
this [guide](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/how-to-configure-openssl-linux?pivots=programming-language-csharp)
.

# RUN

Run this command from project root, after you've set your own preferences in `src/config/basic_config.json`

````
python -m src.main
````

