import os
import json
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
        self.setup = True

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

    def generate_text_news(self, url, how_many: int):
        print('Generating text from RSS feed')
        headings = []
        if self.setup:
            print()
            print('Please choose which headings are you interested in (e.g. 1 2 3): ')
            print('1. -- Belföld')
            print('2. -- Gazdaság')
            print('3. -- Külföld')
            print('4. -- Kult')
            print('5. -- Tech')
            options = input('Your choice: ')
            options = options.split(" ")
            for item in options:
                if item == 1:
                    headings.append('belfold')
                if item == 2:
                    headings.append('gazdasag')
                if item == 3:
                    headings.append('kulfold')
                if item == 4:
                    headings.append('kult')
                if item == 5:
                    headings.append('tech')
                else:
                    raise Exception('Wrong input!')
            self.setup = False
        feed = Feed(url, heading=headings)
        data = feed.titles(howmany=how_many)
        source = feed.source()
        print('From source: ' + source)
        return_data = [" A legfrissebb hírek következnek, a " + source + " jóvoltából. "]
        for sentence in data:
            return_data.append(sentence + ". ")
        return return_data

    def generate_text_email(self, data: list):
        print("Generating text from incoming emails")
        text = [
            "A következő üzenetei érkeztek. "
        ]
        with open('repository.json', mode='r', encoding='utf-8') as file:
            dict_elem = json.load(file)
            for item in data[:]:
                if item in dict_elem:
                    data.remove(item)
                else:
                    dict_elem.append(item)
        with open('repository.json', 'w', encoding='utf-8') as file:
            json.dump(dict_elem, file, ensure_ascii=False)
        print(f"New messages: {data}, len: {len(data)}")
        if len(data) == 0:
            text = ['Nem érkezett új üzenete.']
        for item in data:
            text.append(
                "Érkezett: " + item['date'] + " , feladó: " + item['sender'] + ", téma: " + item['subject'] + ". ")
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
        speech.generate_text_hello()
    ]
    text = text + speech.generate_text_news('https://telex.hu/rss', how_many=6)
    for i in speech.generate_text_email(gmail.get_emails(how_many=5, by_labels=['UNREAD'])):
        text.append(i)
    speech.synthesize(text)
