import json
import logging
from datetime import datetime, date

from src.dataprovider.rss import Feed

logging.basicConfig(level=logging.INFO)


class Speech:
    """
    General class for speech synthesising.
    """

    def __init__(self, language):
        self.language = language
        with open('basicconfig/basic_config.json') as config:
            self.config = json.load(config)

    def generate_text_hello(self):
        logging.info('Generating hello message')
        today = self.getCurrentDate()
        current_time = self.getCurrentTime()
        return "Üdvözlöm! Ma " + today + " van, az idő " + current_time + "."

    def getCurrentDate(self):
        today = date.today().strftime("%Y.%m.%d.")
        return today

    def getCurrentTime(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        return current_time

    def generate_text_weather(self, data):
        logging.info('Generating text for weather...')
        if self.language == 'en-EN':
            return "It's currently " + str(round(data["current"]["temp"])) + " degrees outside. The weather is " + str(
                data["current"]["weather"][0]["description"]) + ". Wind speed is " + str(
                round(data["current"]["wind_speed"])) + " km/h."

        if self.language == 'hu-HU':
            return "Jelenleg " + str(round(data["current"]["temp"])) + " fok van. Az időjárás " + str(
                data["current"]["weather"][0]["description"]) + ". A szél sebessége " + str(
                round(data["current"]["wind_speed"])) + " km/h."

    def generate_text_news(self):
        logging.info('Generating text from RSS feed')
        feed = Feed(url=self.config['news']['source'], heading=self.config['news']['category'])
        data = feed.get_news(howmany=self.config['news']['how_many'])
        source = feed.source()
        logging.info('From source: ' + source)
        return_data = []
        if data:
            for sentence in data:
                return_data.append(sentence + ". ")
        else:
            return_data = ['Egyelőre nem történt új hír értékű esemény.']
        return return_data

    def generate_text_email(self, data: list):
        logging.info("Generating text from incoming emails")
        repository = 'basicconfig/repository.json'
        text = [
            "A következő üzenetei érkeztek. "
        ]
        with open(repository, mode='r', encoding='utf-8') as file:
            dict_elem = json.load(file)
            for item in data[:]:
                if item in dict_elem:
                    data.remove(item)
                else:
                    dict_elem.append(item)
        with open(repository, 'w', encoding='utf-8') as file:
            json.dump(dict_elem, file, ensure_ascii=False)
        logging.debug(f"New messages: {data}")
        if len(data) == 0:
            text = ['Nem érkezett új üzenete.']
        for item in data:
            text.append(
                "Érkezett: " + item['date'] + " napon, feladó: " + item['sender'] + ", téma: " + item['subject'] + ". ")
        return text

    def synthesize(self, text):
        pass

