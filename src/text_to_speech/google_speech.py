import logging

import os.path

import google.cloud.texttospeech as tts


from src.text_to_speech.speech import Speech
from src.data.enums import Constants
from src.text_to_speech import play_audio


class GoogleSpeech(Speech):

    def __init__(self, voice_params: tts.VoiceSelectionParams):
        super().__init__()
        self.client = tts.TextToSpeechClient()
        self.voice_params = voice_params
        self.audio_config: tts.AudioConfig = tts.AudioConfig(audio_encoding=tts.AudioEncoding.MP3)
        self.logger = logging.getLogger(__name__)

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
            self.logger.info(f'Generated speech saved to "{filename}"')

        play_audio(filename)


if __name__ == "__main__":
    speech = GoogleSpeech(voice_params=tts.VoiceSelectionParams(name="en-GB-Wavenet-B", language_code='en-GB'),
                          audio_config=tts.AudioConfig(audio_encoding=tts.AudioEncoding.MP3))

    speech.list_languages()
