import time

from myradio.src import weather
from myradio.src.client import Client


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


weatherApp = weather.Weather('Budapest')
weatherApp.synthesise(r"D:\Data\ProjectLaboratory\myradio\src\weather.wav", 'hu-HU', 'hu-HU-NoemiNeural')

username = 'dewarhun'
client = Client(username)

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
print(f'Username: {name}')
print(f'Followers: {client.getFollowersNum(user)}')

# Main loop

while True:

    loopMsg()

    choice = input("Enter your choice: ")

    # Search for artist
    if choice == '0':

        searchQuery = input("Ok, what's their name?:")
        # Get search results
        searchResults = client.search(searchQuery, 1, 0, 'artist')
        # Print artist details
        artist = searchResults['artists']['items'][0]

        info(artist)

        artist_id = artist['id']

        all_tracks = client.get_tracks_by_artist(artist_id)

        selected = []
        while True:
            selected.append(client.select_song(all_tracks))
            if selected is None:
                break
            else:
                # Start playback
                client.start_playback(None, selected)
                # Wait 10 seconds
                time.sleep(10)
                # Get info about the current track
                current_track = client.current_track()
                progress_ms = current_track['progress_ms']
                name = current_track['item']['name']
                # Stop playback
                print(f"Stopping last track: {name}")
                # Play sample audio
                client.pause_playback()

                client.simulate_speech()

                print(f"Continuing last track: {name}")

                client.start_playback(context_uri=None, uris=selected, progress_ms=progress_ms)

                selected.pop()

    if choice == '1':
        break
