from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer
from azure.cognitiveservices.speech.audio import AudioOutputConfig

from myradio.src.text-topic import TextTopic

class Speech:

    def __init__(self, speech_config):
        self.speech_config = speech_config

    # def generate_text(self, data, topic=None):
        # if topic is None:
        # if topic is

