import json
import logging

import google.cloud.texttospeech as tts
import multitimer

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
            language = basic_config['azure']['language']
            voice = language + '-' + basic_config['azure']['voice']
            speech = azure_speech.AzureSpeech(language=language, voice=voice)
        elif basic_config['speech']['resource'] == 'google':
            language = basic_config['google']['language']
            name = language + '-' + basic_config['google']['voice']
            speech = google_speech.GoogleSpeech(voice_params=tts.VoiceSelectionParams(name=name, language_code=language))
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
