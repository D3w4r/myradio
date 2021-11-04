import json
import logging
import os

import google.cloud.texttospeech as tts
import multitimer
from azure.cognitiveservices.speech import SpeechConfig

from music.spotipy_client import Client
from src.text_to_speech import azure_speech
from text_to_speech import google_speech
from text_to_speech.speech import Speech
from text_to_speech.text_generator import TextGenerator

logging.basicConfig(level=logging.INFO)

config_path = 'src/config/'


def initialize():
    with open(config_path + 'basic_config.json') as basic:
        basic_config = json.load(basic)
    if basic_config['speech']['resource'] == 'azure':
        with open(config_path + 'azure_config.json') as azure_config:
            config = json.load(azure_config)
            speech = azure_speech.AzureSpeech(
                speechconfig=SpeechConfig(
                    subscription=os.environ.get('AZURE_TTS_ID'),
                    region=config['region']),
                language=config['language'],
                voice=config['voice'])
    elif basic_config['speech']['resource'] == 'google':
        with open(config_path + 'google_config.json') as google_config:
            config = json.load(google_config)
            voice_params = config['voice_params']
            speech = google_speech.GoogleSpeech(
                voice_params=tts.VoiceSelectionParams(
                    name=voice_params['name'],
                    language_code=voice_params['language_code']),
                audio_config=tts.AudioConfig(audio_encoding=tts.AudioEncoding.MP3))
    return speech


def demonstrate(spotify: Client, generator: TextGenerator, speech: Speech):
    text = generator.generate_feed()
    spotify.pause_playback()
    speech.synthesize(text)
    spotify.bbc_minute()
    spotify.restart_playback()


def main():
    client = Client('dewarhun')
    client.set_primary_device(client.active_devices(), 0)
    generator = TextGenerator()
    speech = initialize()

    timer = multitimer.MultiTimer(interval=5.0, function=demonstrate, args=[client, generator, speech],
                                  runonstart=False)
    timer.start()


# todo spotify playlists, weights path fix

if __name__ == "__main__":
    main()
