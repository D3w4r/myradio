import os
from datetime import datetime, date

import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer
from azure.cognitiveservices.speech.audio import AudioOutputConfig

from myradio.src.mail import Gmail
from myradio.src.rss import Feed


class Speech:
    """"Class for generating and synthesising speech"""

    def __init__(self, speechconfig: SpeechConfig, voice, language):
        if voice is None:
            raise RuntimeError('Please specify a voice')
        if language is None:
            raise RuntimeError('Please specify a language')
        self.language = language
        speech_config = speechconfig
        speech_config.speech_synthesis_language = language
        speechconfig.speech_synthesis_voice_name = voice
        self.speech_synthesizer = SpeechSynthesizer(speech_config=speech_config,
                                                    audio_config=AudioOutputConfig(use_default_speaker=True))

    def generate_text_hello(self):
        print('Hello TTS!')
        today = date.today().strftime("%Y.%m.%d.")
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        return "Üdvözlöm! Ma " + today + " van, az idő " + current_time + "."

    def generate_text_weather(self, data):
        print('Generating text for weather...')
        if self.language == 'en-EN':
            return "It's currently " + str(data["current"]["temp"]) + " degrees, but it feels like " + str(
                data["current"]["feels_like"]) + " degrees outside. The description of the weather is " + str(
                data["current"]["weather"][0]["description"]) + ". Wind speed is " + str(
                data["current"]["wind_speed"]) + " kilometers an hour."

        if self.language == 'hu-HU':
            return "Jelenleg " + str(data["current"]["temp"]) + " fok van, ami " + str(
                data["current"]["feels_like"]) + " foknak érződik. Az időjárás leírása: " + str(
                data["current"]["weather"][0]["description"]) + ". A szél sebessége " + str(
                data["current"]["wind_speed"]) + " kilóméter per óra."

    def generate_text_news(self, url):
        print('Generating text from RSS feed')
        feed = Feed(url)
        data = feed.titles(howmany=5)
        source = feed.source()
        print('From source: ' + source)
        return "A legújabb hírek következnek, a " + source + " jóvoltából. " + data[0] + ". " + data[1] + ". " + data[
            2] + ". " + data[3] + ". " + \
               data[4] + "."

    def generate_text_breaking(self, data):
        pass

    def generate_text_email(self, data: list):
        print("Generating text from incoming emails")
        text = [
            "A következő üzenetei érkeztek. "
        ]
        for item in data:
            text.append(
                "Feladó: " + item['sender'] + ", téma: " + item['subject'] + "."
            )
        return text

    def synthesize(self, text_list: list):
        print('Synthesising speech...')
        for item in text_list:
            result = self.speech_synthesizer.speak_text(item)
            if result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                print(f"Speech synthesis canceled: {cancellation_details.reason}")
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    if cancellation_details.error_details:
                        print(f"Error details: {cancellation_details.error_details}")
                break


# TESTS #
if __name__ == "__main__":
    speech = Speech(speechconfig=SpeechConfig(subscription=os.environ.get('AZURE_TTS_ID'), region='westeurope'),
                    language='hu-HU', voice='hu-HU-NoemiNeural')
    gmail = Gmail()

    text = [
        speech.generate_text_hello(),
        speech.generate_text_news('https://telex.hu/rss')
    ]
    for i in speech.generate_text_email(gmail.get_emails()):
        text.append(i)

    speech.synthesize(text)
