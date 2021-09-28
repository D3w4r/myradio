import logging
import os

import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer
from azure.cognitiveservices.speech.audio import AudioOutputConfig

import myradio.src.speech
from myradio.src.dataprovider.mail import Gmail

logging.basicConfig(level=logging.INFO)


class Speech(myradio.src.speech.Speech):
    """"Class for generating and synthesising speech"""

    def __init__(self, speechconfig: SpeechConfig, voice, language):
        super().__init__(language)
        if voice is None:
            logging.error('There is no voice specified')
            raise RuntimeError('Please specify a voice')
        if language is None:
            raise RuntimeError('Please specify a language')
        self.language = language
        speech_config = speechconfig
        speech_config.speech_synthesis_language = language
        speechconfig.speech_synthesis_voice_name = voice
        self.speech_synthesizer = SpeechSynthesizer(speech_config=speech_config,
                                                    audio_config=AudioOutputConfig(use_default_speaker=True))
        self.setup = True

    def synthesize(self, text):
        logging.info('Synthesising speech...')
        for item in text:
            result = self.speech_synthesizer.speak_text(item)
            if result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                logging.error(f"Speech synthesis canceled: {cancellation_details.reason}")
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    if cancellation_details.error_details:
                        logging.error(f"Error details: {cancellation_details.error_details}")
                break


# TESTS #
if __name__ == "__main__":
    speech = Speech(speechconfig=SpeechConfig(subscription=os.environ.get('AZURE_TTS_ID'), region='westeurope'),
                    language='hu-HU', voice='hu-HU-NoemiNeural')
    gmail = Gmail()

    text = [
        speech.generate_text_hello()
    ]
    speech.synthesize(text)
