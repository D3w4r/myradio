import json
import logging
import os
import time

import google.cloud.texttospeech as tts
import multitimer
from azure.cognitiveservices.speech import SpeechConfig

from src.azure import azure_speech
from src.google import google_speech
from src.spotify.spotipy_client import Client

logging.basicConfig(level=logging.INFO)


def load_config():
    with open('basicconfig/basic_config.json') as basic:
        basic_config = json.load(basic)
    if basic_config['speech']['resource'] == 'azure':
        with open('azure/config/azure_config.json') as azure_config:
            config = json.load(azure_config)
            speech = azure_speech.Speech(
                speechconfig=SpeechConfig(
                    subscription=os.environ.get('AZURE_TTS_ID'),
                    region=config['region']),
                language=config['language'],
                voice=config['voice'])
    elif basic_config['speech']['resource'] == 'google':
        with open('google/config/google_config.json') as google_config:
            config = json.load(google_config)
            voice_params = config['voice_params']
            speech = google_speech.Speech(
                voice_params=tts.VoiceSelectionParams(
                    name=voice_params['name'],
                    language_code=voice_params['language_code']),
                audio_config=tts.AudioConfig(audio_encoding=tts.AudioEncoding.MP3))
    return speech, basic_config


def stop_track(client: Client):
    stopped_track = client.current_track()
    name = stopped_track['item']['name']
    logging.info(f"Stopping last track: {name}")
    client.pause_playback()
    return stopped_track


def bbc_minute(client):
    bbc_minute = client.search("BBC Minute", 1, 0, 'show')
    podcast = client.spotifyObject.show_episodes(show_id=bbc_minute['shows']['items'][0]['uri'])
    client.start_playback(context_uri=None, uris=[podcast['items'][0]['uri']], progress_ms=0)

    time.sleep(60)
    client.restart_playback()


def demo(client: Client):
    speech, basic_config = load_config()

    client.pause_playback()

    text = []
    text += speech.generate_greeting()
    # text += speech.generate_text_weather()
    text += speech.generate_text_email()
    text += speech.generate_text_news()

    speech.synthesize(text)

    bbc_minute(client)


def main():
    client = Client('dewarhun')
    client.set_primary_device(client.active_devices(), 0)
    timer = multitimer.MultiTimer(interval=5.0, function=demo, args=[client], runonstart=False)
    timer.start()


if __name__ == "__main__":
    main()
