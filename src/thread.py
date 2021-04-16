import os
import random
import sys
import threading
import time
from pprint import pprint
from threading import Lock

from azure.cognitiveservices.speech import SpeechConfig

from myradio.src.client import Client
from myradio.src.mail import Gmail
from myradio.src.weather import Weather

from speech import Speech


class LockThread(threading.Thread):
    # Weather
    weather_app = Weather('Budapest')
    # Speech
    speech = Speech(speechconfig=SpeechConfig(subscription=os.environ.get('AZURE_TTS_ID'), region='westeurope'),
                    language='hu-HU', voice='hu-HU-NoemiNeural')
    gmail = Gmail()

    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        threading.Event().wait()
        print(f'Starting {self.name}')
        # Get lock to synchronize threads
        text = [
            self.speech.generate_text_hello()
            # self.speech.generate_text_weather(self.weather_app.weather_info()),
            # self.speech.generate_text_news('https://telex.hu/rss')
        ]
        for i in self.speech.generate_text_email(self.gmail.get_emails()):
            text.append(i)
        self.speech.synthesize(text)


def info(subject):
    print(subject['name'])
    print(str(subject['followers']['total']) + " followers")
    print(subject['genres'][0])
    print()


def loopMsg():
    print()
    print("0 - Search for an artist")
    print("1 - exit")
    print()


class SimpleThread(threading.Thread):
    client = Client('dewarhun')
    devices = client.active_devices()
    client.set_primary_device(devices, 0)
    selected = []

    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        with threading.Lock():
            print(f'Starting {self.name}')

            loopMsg()

            choice = input("Enter your choice: ")

            # Search for artist
            if choice == '0':

                search_query = input("Ok, what's their name?: ")
                # Get search results
                search_results = self.client.search(search_query, 1, 0, 'artist')
                # Print artist details
                artist = search_results['artists']['items'][0]

                info(artist)

                artist_id = artist['id']

                all_tracks = self.client.get_tracks_by_artist(artist_id)

                while True:
                    self.selected.append(self.client.select_song(all_tracks))

                    if self.selected is None:
                        break
                    else:
                        # Get info about the current track
                        self.client.start_playback(context_uri=None, uris=self.selected)

                        current_track = self.client.current_track()
                        # progress_ms = current_track['progress_ms']
                        name = current_track['item']['name']
                        # Start playback
                        print(f'Starting song: {name}')
                        # self.client.start_playback(context_uri=None, uris=selected, progress_ms=progress_ms)
                        self.selected.clear()
