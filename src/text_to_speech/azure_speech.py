import logging
import os

import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer
from azure.cognitiveservices.speech.audio import AudioOutputConfig

from src.text_to_speech.speech import Speech


class AzureSpeech(Speech):
    """"Class for generating and synthesising speech"""

    def __init__(self, voice, language):
        super().__init__()
        self.logger = logging.getLogger(__name__)

        speech_config = SpeechConfig(
            subscription=os.environ.get('AZURE_TTS_ID'),
            region='westeurope')
        speech_config.speech_synthesis_language = language
        speech_config.speech_synthesis_voice_name = voice
        self.speech_synthesizer = SpeechSynthesizer(speech_config=speech_config,
            audio_config=AudioOutputConfig(use_default_speaker=True))
        self.setup = True

    def synthesize(self, input_text):
        self.logger.info('Synthesising speech...')
        for item in input_text:
            result = self.speech_synthesizer.speak_text(item)
            if result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                self.logger.error(f"Speech synthesis canceled: {cancellation_details.reason}")
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    if cancellation_details.error_details:
                        self.logger.error(f"Error details: {cancellation_details.error_details}")
                break
