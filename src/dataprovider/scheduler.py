import logging
from datetime import date, datetime

from src.constants.constats import Time
from src.speech import Speech


logging.basicConfig(level=logging.INFO)


class Scheduler:

    def get_current_time_str(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        return current_time

    def get_current_date_str(self):
        today = date.today().strftime("%Y.%m.%d.")
        return today

    def get_part_of_day(self):
        now = datetime.now()
        if now.hour < 12:
            return Time.BREAKFAST
        elif 12 <= now.hour <= 13:
            return Time.LUNCH
        else:
            return Time.DINNER

    def generate_feed(self, speech_client: Speech):
        part_of_day = self.get_part_of_day()
        return_text = []
        if part_of_day == Time.BREAKFAST:
            return_text += speech_client.generate_greeting()
            return_text += speech_client.generate_text_weather()
        elif part_of_day == Time.LUNCH:
            return_text += speech_client.generate_text_email()
        else:
            pass
        return return_text



if __name__ == "__main__":
    s = Scheduler()
    s.get_part_of_day()

