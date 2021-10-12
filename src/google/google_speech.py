import logging
import os.path
import time

import google.cloud.texttospeech as tts
import vlc

import src.azure.azure_speech

from src.constants.constats import Constants

logging.basicConfig(level=logging.INFO)


class Speech(src.speech.Speech):

    def __init__(self, voice_params: tts.VoiceSelectionParams, audio_config: tts.AudioConfig):
        super().__init__(voice_params.language_code)
        self.client = tts.TextToSpeechClient()
        self.voice_params = voice_params
        self.audio_config: tts.AudioConfig = audio_config

    def unique_languages_from_voices(self, voices):
        language_set = set()
        for voice in voices:
            for language_code in voice.language_codes:
                language_set.add(language_code)
        return language_set

    def list_languages(self):
        response = self.client.list_voices()
        languages = self.unique_languages_from_voices(response.voices)

        print(f" Languages: {len(languages)} ".center(60, "-"))
        for i, language in enumerate(sorted(languages)):
            print(f"{language:>10}", end="\n" if i % 5 == 4 else "")

    def list_voices(self, language_code=None):
        response = self.client.list_voices(language_code=language_code)
        voices = sorted(response.voices, key=lambda voice: voice.name)

        print(f" Voices: {len(voices)} ".center(60, "-"))
        for voice in voices:
            languages = ", ".join(voice.language_codes)
            name = voice.name
            gender = tts.SsmlVoiceGender(voice.ssml_gender).name
            rate = voice.natural_sample_rate_hertz
            print(f"{languages:<8} | {name:<24} | {gender:<8} | {rate:,} Hz")

    def synthesize(self, text):
        text_input = tts.SynthesisInput(text=' '.join(text))
        voice_params = self.voice_params
        audio_config = self.audio_config
        client = self.client

        response = client.synthesize_speech(
            input=text_input, voice=voice_params, audio_config=audio_config
        )

        filename = f"hu-HU.mp3"
        with open(os.path.join(Constants.CACHE_PATH.value, filename), "wb") as out:
            out.write(response.audio_content)
            logging.info(f'Generated speech saved to "{filename}"')

        player = vlc.MediaPlayer()
        media = vlc.Media(Constants.CACHE_PATH.value + '\hu-HU.mp3')
        player.set_media(media)
        player.play()
        time.sleep(1)
        time.sleep(player.get_length() / 1000)


if __name__ == "__main__":
    speech = Speech(voice_params=tts.VoiceSelectionParams(name="hu-HU-Wavenet-A", language_code='hu-HU'),
                    audio_config=tts.AudioConfig(audio_encoding=tts.AudioEncoding.MP3))

    speech.synthesize(text=["Milyen nap van ma? Ez egy teszt"])
