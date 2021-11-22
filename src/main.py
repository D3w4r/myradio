import json
import logging
import sys

import google.cloud.texttospeech as tts
import multitimer
from pynput import keyboard

from src.data.enums import Constants
from src.music.spotipy_client import Client
from src.text_to_speech import azure_speech
from src.text_to_speech import google_speech
from src.text_to_speech.speech import Speech
from src.text_to_speech.text_generator import TextGenerator


def get_interval():
    with open(Constants.CONFIG.value) as config:
        _config = json.load(config)
        return _config['news']['interval_sec']


def initialize_speech():
    with open(Constants.CONFIG.value) as config:
        _config = json.load(config)
        if _config['speech']['resource'] == 'azure':
            language = _config['azure']['language']
            voice = language + '-' + _config['azure']['voice']
            speech = azure_speech.AzureSpeech(language=language, voice=voice)
        elif _config['speech']['resource'] == 'google':
            language = _config['google']['language']
            name = language + '-' + _config['google']['voice']
            speech = google_speech.GoogleSpeech(
                voice_params=tts.VoiceSelectionParams(name=name, language_code=language))
    return speech


client = Client('dewarhun')
generator = TextGenerator()
speech = initialize_speech()


def on_press(key):
    try:
        demonstrate(client, generator, speech)
        logging.info(f'Test key {key} pressed!')
    except AttributeError:
        logging.error(f'Special key {key} pressed')


def demonstrate(spotify: Client, generator: TextGenerator, speech: Speech):
    logging.info('Demonstrate method called')
    text = generator.generate_feed()
    spotify.pause_playback()
    speech.synthesize(text)
    spotify.bbc_minute()
    spotify.restart_playback()


def main():
    interval = get_interval()

    listener = keyboard.Listener(
        on_press=on_press
    )

    timer = multitimer.MultiTimer(interval=interval, function=demonstrate, args=[client, generator, speech],
                                  runonstart=False)
    timer.start()
    logging.info(f'Started countdown from {interval}')
    listener.start()
    logging.info(f'Started keyboard listener')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
