import json
import logging
from datetime import datetime, date

from src.dataprovider.mail import Gmail
from src.dataprovider.rss import Feed
from src.dataprovider.weather import Weather

logging.basicConfig(level=logging.INFO)


class Speech:
    """
    General class for speech synthesising.
    """

    def __init__(self, language):
        self.language = language
        with open('basicconfig/basic_config.json', mode='r', encoding='utf-8') as config:
            self.config = json.load(config)
        self.weather_app = Weather(self.config['weather']['city'])
        self.gmail_app = Gmail()

    def get_current_time_str(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        return current_time

    def get_current_date_str(self):
        today = date.today().strftime("%Y.%m.%d.")
        return today

    def generate_greeting(self):
        logging.info('Generating hello message')
        today = self.get_current_date_str()
        current_time = self.get_current_time_str()
        return ["Szia! " + current_time + " órai jelentésem következik! "]

    def generate_morning_greeting(self):
        logging.info('Generating hello message')
        today = self.get_current_date_str()
        current_time = self.get_current_time_str()
        return ["Jó reggelt! Ma " + today + " van, az óra " + current_time + "-t mutat. "]

    def generate_text_weather(self):
        logging.info('Generating text for weather...')
        weather = Weather(self.config['weather']['city'])
        data = weather.weather_info()
        return ["Jelenleg " + str(round(data["current"]["temp"])) + " fok van." + " A szél ma várhatóan " + str(
            round(data["current"]["wind_speed"])) + " km/h sebességgel fog fújni."]

    def generate_text_news(self):
        logging.info('Generating text from RSS feed')
        feed = Feed(url=self.config['news']['source'], heading=self.config['news']['category'])
        news = feed.get_news(howmany=self.config['news']['how_many'])
        logging.info('From source: ' + feed.source())
        return_data = []
        if news:
            for headline in news:
                return_data.append(headline + ". ")
        else:
            return_data = ['Egyelőre nem történt új hír értékű esemény.']
        return return_data

    def generate_text_email(self):
        input: list = self.gmail_app.get_emails(how_many=5, by_labels=['UNREAD'])
        logging.info("Generating text from incoming emails")
        repository = 'basicconfig/repository.json'
        text = [
            "A következő feladóktól üzeneteid érkeztek: "
        ]
        with open(repository, mode='r', encoding='utf-8') as file:
            persisted_emails = json.load(file)
            for item in input[:]:
                if item in persisted_emails:
                    input.remove(item)
                else:
                    persisted_emails.append(item)
        with open(repository, 'w', encoding='utf-8') as file:
            json.dump(persisted_emails, file, ensure_ascii=False)
        logging.debug(f"New messages: {input}")
        if len(input) == 0:
            text = ['Nem érkezett új üzeneted.']
        senders = []
        for item in input[:]:
            if item['sender'] not in senders:
                senders.append(item['sender'])
        for sender in senders:
            if sender == senders[-1]:
                text.append(sender + '. ')
            else:
                text.append(" " + sender + ", ")
        return text

    def synthesize(self, text):
        pass

