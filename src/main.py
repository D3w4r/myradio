import json
import logging

import google.cloud.texttospeech as tts
import multitimer

from data.enums import Constants
from music.spotipy_client import Client
from src.text_to_speech import azure_speech
from text_to_speech import google_speech
from text_to_speech.speech import Speech
from text_to_speech.text_generator import TextGenerator

logging.basicConfig(level=logging.INFO)


def initialize():
    interval = None
    with open(Constants.CONFIG.value) as basic:
        basic_config = json.load(basic)
        if basic_config['speech']['resource'] == 'azure':
            language = basic_config['azure']['language']
            voice = language + '-' + basic_config['azure']['voice']
            speech = azure_speech.AzureSpeech(language=language, voice=voice)
        elif basic_config['speech']['resource'] == 'google':
            language = basic_config['google']['language']
            name = language + '-' + basic_config['google']['voice']
            speech = google_speech.GoogleSpeech(
                voice_params=tts.VoiceSelectionParams(name=name, language_code=language))
        interval = basic_config['news']['interval']
    return speech, interval


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
    speech, interval = initialize()

    timer = multitimer.MultiTimer(interval=interval, function=demonstrate, args=[client, generator, speech],
                                  runonstart=False)
    timer.start()


if __name__ == "__main__":
    main()
