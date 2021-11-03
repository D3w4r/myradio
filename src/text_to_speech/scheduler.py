import logging
from datetime import datetime

import music.spotipy_client
from data.enums import Time
from text_to_speech.speech import Speech

logging.basicConfig(level=logging.INFO)


class Scheduler:

    def get_part_of_day(self):
        now = datetime.now()
        if now.hour < 12:
            return Time.BREAKFAST
        elif 12 <= now.hour <= 13:
            return Time.LUNCH
        else:
            return Time.DINNER

    def generate_feed(self, speech_client: Speech, spotify_client: music.spotipy_client.Client):
        spotify_client.pause_playback()
        part_of_day = self.get_part_of_day()
        text = []
        if part_of_day == Time.BREAKFAST:
            text += speech_client.generate_morning_greeting()
            text += speech_client.generate_text_weather()
            text += speech_client.generate_text_news()
        elif part_of_day == Time.LUNCH:
            text += speech_client.generate_greeting()
            text += speech_client.generate_text_weather()
            text += speech_client.generate_text_email()
        else:
            text += speech_client.generate_greeting()
            text += speech_client.generate_text_news()
        return text


if __name__ == "__main__":
    s = Scheduler()
    s.get_part_of_day()
