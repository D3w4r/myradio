from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer
from rss import Feed


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
        self.speech_synthesizer = SpeechSynthesizer(speech_config=speech_config)

    def generate_text_weather(self, data):
        print('Generating text for weather...')
        if self.language == 'en-EN':
            text = "It's currently " + str(data["current"]["temp"]) + " degrees, but it feels like " + str(
                data["current"]["feels_like"]) + " degrees outside. The description of the weather is " + str(
                data["current"]["weather"][0]["description"]) + ". Wind speed is " + str(
                data["current"]["wind_speed"]) + " kilometers an hour."
            return text
        if self.language == 'hu-HU':
            text = "Jelenleg " + str(data["current"]["temp"]) + " fok van, ami " + str(
                data["current"]["feels_like"]) + " foknak érződik. Az időjárás leírása: " + str(
                data["current"]["weather"][0]["description"]) + ". A szél sebessége " + str(
                data["current"]["wind_speed"]) + " kilóméter per óra."
            return text

    def generate_text_news_top(self, url):
        feed = Feed(url)
        data = feed.top_five_entries()
        text = "A jelenlegi hírek a következőek: " + data[0] + ". " + data[1] + ". " + data[2] + ". " + data[3] + ". " + \
               data[4] + "."
        return text

    def generate_text_breaking(self, data):
        pass

    def generate_text_email(self, data):
        pass

    def synthesize(self, text: list):
        print('Synthesising speech...')
        for item in text:
            self.speech_synthesizer.speak_text(item)
