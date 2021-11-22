import json
import logging
from datetime import datetime, date

from src.data.enums import Time, Constants
from src.data.mail import Gmail
from src.text_to_speech.rss import Feed
from src.data.weather import Weather


def get_current_time_str():
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    return current_time


def get_current_date_str():
    today = date.today().strftime("%Y.%m.%d.")
    return today


def get_part_of_day():
    now = datetime.now()
    if now.hour < 12:
        return Time.BREAKFAST
    elif 12 <= now.hour <= 13:
        return Time.LUNCH
    else:
        return Time.DINNER


class TextGenerator:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        with open('src/config/' + 'basic_config.json', mode='r', encoding='utf-8') as config:
            self.config = json.load(config)
        self.weather_app = Weather(self.config['weather']['city'])
        self.gmail_app = Gmail()
        self.feed = Feed(url=self.config['news']['source'])

    def generate_greeting(self):
        self.logger.info('Generating hello message')
        current_time = get_current_time_str()
        return ["Hi. The time is " + current_time + "! "]

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
        news = self.feed.get_news_titles(howmany=self.config['news']['how_many'])
        return_data = news
        if not news:
            return_data = ["There are no new news which you haven't heard yet."]
        return return_data

    def generate_text_email(self):
        input: list = self.gmail_app.get_emails_by_labels(how_many=5, by_labels=['UNREAD'])
        self.logger.info("Generating text from incoming emails")
        text = ["You've got mail from: "]
        repository_path = Constants.MAIL_REPOSITORY.value
        with open(repository_path, mode='r', encoding='utf-8') as file:
            persisted_emails = json.load(file)
            for item in input[:]:
                if item in persisted_emails:
                    input.remove(item)
                else:
                    persisted_emails.append(item)
        with open(repository_path, 'w', encoding='utf-8') as file:
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

    def generate_feed(self):
        part_of_day = get_part_of_day()
        text = []
        if part_of_day == Time.BREAKFAST:
            text += self.generate_morning_greeting()
            text += self.generate_text_weather()
            text += self.generate_text_news()
        elif part_of_day == Time.LUNCH:
            text += self.generate_greeting()
            text += self.generate_text_email()
        else:
            text += self.generate_greeting()
            text += self.generate_text_news()
        return text


if __name__ == "__main__":
    generator = TextGenerator()
    text = generator.generate_feed()
    print(text)
