import json
import logging
import os
import time

import google.cloud.texttospeech as tts
import multitimer
from azure.cognitiveservices.speech import SpeechConfig

from src.azure import azure_speech
from src.dataprovider.mail import Gmail
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
    current_track = client.current_track()
    name = current_track['item']['name']
    logging.info(f"Stopping last track: {name}")
    client.pause_playback()
    return current_track


def bbc_minute(client, track):
    bbc_minute = client.search("BBC Minute", 1, 0, 'show')
    podcast = client.spotifyObject.show_episodes(show_id=bbc_minute['shows']['items'][0]['uri'])
    client.start_playback(context_uri=None, uris=[podcast['items'][0]['uri']])

    restart_playback(client, podcast, track)


def restart_playback(client, podcast, track):
    progress_ms = track['progress_ms']
    name = track['item']['name']

    time.sleep(podcast['items'][0]['duration_ms'] / 1000)

    logging.info(f"Continuing last track: {name}")
    uris = [track['item']['uri']]
    client.start_playback(context_uri=None, uris=uris, progress_ms=progress_ms)


def demo(client: Client):
    speech, basic_config = load_config()

    gmail = Gmail()

    current = stop_track(client)

    # TODO: idősávok!!!
    text = []
    text += speech.generate_greeting()
    text += speech.generate_text_weather(basic_config)
    text += speech.generate_text_email(gmail.get_emails(how_many=5, by_labels=['UNREAD']))
    text += speech.generate_text_news()

    speech.synthesize(text)

    bbc_minute(client, current)


def main():
    client = Client('dewarhun')
    client.set_primary_device(client.active_devices(), 0)
    timer = multitimer.MultiTimer(interval=5.0, function=demo, args=[client], runonstart=False)
    timer.start()


if __name__ == "__main__":
    main()
