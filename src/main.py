import json
import logging
import os


import google.cloud.texttospeech as tts
import multitimer
from azure.cognitiveservices.speech import SpeechConfig

from src.azure import azure_speech
from src.google import google_speech
from src.spotify.spotipy_client import Client
from src.dataprovider.scheduler import Scheduler

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


def demo(spotify: Client):
    speech, basic_config = load_config()
    scheduler = Scheduler()

    text = scheduler.generate_feed(speech, spotify)

    speech.synthesize(text)
    spotify.bbc_minute()


def main():
    client = Client('dewarhun')
    client.set_primary_device(client.active_devices(), 0)
    timer = multitimer.MultiTimer(interval=5.0, function=demo, args=[client], runonstart=False)
    timer.start()


if __name__ == "__main__":
    main()
