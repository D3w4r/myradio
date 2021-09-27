import logging
import os

import multitimer
from azure.cognitiveservices.speech import SpeechConfig

from weather import Weather
from spotipy_client import Client
from mail import Gmail
from mythread import MusicThread
from speech import Speech

logging.basicConfig(level=logging.INFO)


def speak(client: Client):
    # Weather
    weather_app = Weather('Budapest')
    # Speech
    speech = Speech(speechconfig=SpeechConfig(subscription=os.environ.get('AZURE_TTS_ID'), region='westeurope'),
                    language='hu-HU', voice='hu-HU-NoemiNeural')
    # Mail
    # gmail = Gmail()

    current_track = client.current_track()
    progress_ms = current_track['progress_ms']
    name = current_track['item']['name']
    logging.info(f"Stopping last track: {name}")
    client.pause_playback()
    # Synthesise
    text = [
        speech.generate_text_hello(),
        speech.generate_text_weather(weather_app.weather_info())
    ]
    text = text + speech.generate_text_news('https://telex.hu/rss', how_many=2)
    # for i in speech.generate_text_email(
    #         gmail.get_emails(how_many=5, by_labels=['UNREAD'])):
    #     text.append(i)
    speech.synthesize(text)
    # Restart track
    logging.info(f"Continuing last track: {name}")
    uris = [current_track['item']['uri']]
    client.start_playback(context_uri=None, uris=uris, progress_ms=progress_ms)


def main():
    client = Client('dewarhun')
    client.set_primary_device(client.active_devices(), 0)
    logging.info(client.active_devices())
    # t1 = MusicThread(client=client, threadName='music-thread', threadID=1)
    # t1.start()
    timer = multitimer.MultiTimer(interval=5.0, function=speak, args=[client], runonstart=False)
    timer.start()

    # t1.join()
    # timer.stop()
    # timer.join()


if __name__ == "__main__":
    main()
