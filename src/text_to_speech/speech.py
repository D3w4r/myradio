import json
import logging
from datetime import datetime, date

from data.mail import Gmail
from data.rss import Feed
from data.weather import Weather


def get_current_time_str():
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    return current_time


def get_current_date_str():
    today = date.today().strftime("%Y.%m.%d.")
    return today

config_path = 'src/config/'


class Speech:
    """
    General class for speech synthesising.
    """

    def __init__(self, language):
        self.logger = logging.getLogger(__name__)
        self.language = language
        with open(config_path + 'basic_config.json', mode='r', encoding='utf-8') as config:
            self.config = json.load(config)
        self.weather_app = Weather(self.config['weather']['city'])
        self.gmail_app = Gmail()

    def generate_greeting(self):
        self.logger.info('Generating hello message')
        current_time = get_current_time_str()
        return ["Hi. It's " + current_time + " o'clock! Here is some information from the world! "]

    def generate_morning_greeting(self):
        self.logger.info('Generating hello message')
        today = get_current_date_str()
        current_time = get_current_time_str()
        return ["Good morning! Its " + today + ", the current time is " + current_time + ". "]

    def generate_text_weather(self):
        self.logger.info('Generating text for weather...')
        weather = Weather(self.config['weather']['city'])
        data = weather.weather_info()
        return ["Its " + str(round(data["main"]["temp"])) + " degrees outside." + " The wind speed is " + str(
            round(data["wind"]["speed"])) + " km/h."]

    def generate_text_news(self):
        self.logger.info('Generating text from RSS feed')
        feed = Feed(url=self.config['news']['source'], heading=self.config['news']['category'])
        news = feed.get_news_titles(howmany=self.config['news']['how_many'])
        self.logger.info('From source: ' + feed.source())
        return_data = []
        if news:
            for headline in news:
                return_data.append(headline + ". ")
        else:
            return_data = ['Nothing new has happened yet.']
        return return_data

    def generate_text_email(self):
        input: list = self.gmail_app.get_emails_by_labels(how_many=5, by_labels=['UNREAD'])
        self.logger.info("Generating text from incoming emails")
        repository = 'cache/repository.json'
        text = [
            "You've got mail from: "
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
        self.logger.debug(f"New messages: {input}")
        if len(input) == 0:
            text = ["You've got no new messages!"]
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
