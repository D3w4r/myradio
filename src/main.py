import os
import time

import multitimer
from azure.cognitiveservices.speech import SpeechConfig

from myradio.src import weather
from myradio.src.client import Client
from myradio.src.mail import Gmail
from myradio.src.mythread import MusicThread
from myradio.src.speech import Speech


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


def main():
    # App setup
    # Weather
    username = 'dewarhun'
    weather_app = weather.Weather('Budapest')
    # Speech
    speech = Speech(speechconfig=SpeechConfig(subscription=os.environ.get('AZURE_TTS_ID'), region='westeurope'),
                    language='hu-HU', voice='hu-HU-NoemiNeural')
    # Spotify
    client = Client(username)
    # Gmail
    gmail = Gmail()
    # Devices
    devices = client.active_devices()
    # Set primary device
    client.set_primary_device(devices, 0)
    # Current track information
    current_track = client.current_track('v')
    artist = client.get_artist(current_track)
    print(artist)
    # User info
    user = client.user()
    name = user['display_name']
    followers = user['followers']['total']
    print()
    print(f'Username: {name}')
    print(f'Followers: {followers}')

    # Main loop
    while True:

        loopMsg()

        choice = input("Enter your choice: ")

        # Search for artist
        if choice == '0':

            search_query = input("Ok, what's their name?: ")
            # Get search results
            search_results = client.search(search_query, 1, 0, 'artist')
            # Print artist details
            artist = search_results['artists']['items'][0]

            info(artist)

            artist_id = artist['id']

            all_tracks = client.get_tracks_by_artist(artist_id)

            selected = []
            while True:

                selection = client.select_song(all_tracks)
                print(selection)
                if selection is None:
                    break
                else:
                    selected.append(selection)
                    # Start playback
                    client.start_playback(None, selected)
                    # Wait 10 seconds
                    time.sleep(10)
                    current_track = client.current_track()
                    progress_ms = current_track['progress_ms']
                    name = current_track['item']['name']
                    # Stop playback
                    print(f"Stopping last track: {name}")
                    # if difference == 10:
                    client.pause_playback()
                    # Synthesize speech
                    text = [
                        speech.generate_text_hello(),
                        speech.generate_text_weather(weather_app.weather_info())
                    ]
                    text = text + speech.generate_text_news('https://telex.hu/rss', how_many=6)
                    for i in speech.generate_text_email(
                            gmail.get_emails(how_many=5, by_labels=['UNREAD', 'CATEGORY_PERSONAL'])):
                        text.append(i)
                    speech.synthesize(text)
                    # Continue playback
                    print(f"Continuing last track: {name}")
                    client.start_playback(context_uri=None, uris=selected, progress_ms=progress_ms)
                    # Delete selected song
                    selected.pop()

        if choice == '1':
            break


def speak(client: Client):
    weather_app = weather.Weather('Budapest')
    # Speech
    speech = Speech(speechconfig=SpeechConfig(subscription=os.environ.get('AZURE_TTS_ID'), region='westeurope'),
                    language='hu-HU', voice='hu-HU-NoemiNeural')
    gmail = Gmail()

    current_track = client.current_track()
    progress_ms = current_track['progress_ms']
    name = current_track['item']['name']
    # Stop playback
    print(f"Stopping last track: {name}")
    # if difference == 10:
    client.pause_playback()
    # Synthesize speech
    text = [
        speech.generate_text_hello()
        # speech.generate_text_weather(weather_app.weather_info())
    ]
    # text = text + speech.generate_text_news('https://telex.hu/rss', how_many=6)
    # for i in speech.generate_text_email(
    #         gmail.get_emails(how_many=5, by_labels=['UNREAD', 'CATEGORY_PERSONAL'])):
    #     text.append(i)
    speech.synthesize(text)
    print(f"Continuing last track: {name}")
    uris = [current_track['item']['uri']]
    client.start_playback(context_uri=None, uris=uris, progress_ms=progress_ms)


def main2():
    client = Client('dewarhun')
    t1 = MusicThread(client=client, threadName='music-thread', threadID=1)

    t1.start()
    timer = multitimer.MultiTimer(interval=10.0, function=speak, args=[client], runonstart=False)
    timer.start()


if __name__ == "__main__":
    main2()
