import time

from myradio.src import weather
from myradio.src.client import Client


def print_artist_info(artist):
    print(artist['name'])
    print(str(artist['followers']['total']) + " followers")
    print(artist['genres'][0])
    print()


weatherApp = weather.Weather('Budapest')
weatherApp.synthesise(r"D:\Data\ProjectLaboratory\myradio\src\weather.wav")

username = 'dewarhun'
client = Client(username)

# Devices
devices = client.getActiveDevices()
# Set primary device
client.setPrimaryDeviceId(devices, 0)
# Current track information
current_track = client.getCurrentTrack('v')
artist = client.getArtistOfTrack(current_track)
print(artist)
# User info
user = client.getUserInfo()
name = client.getUserName(user)

print(f'Username: {name}')
print(f'Followers: {client.getFollowersNum(user)}')

# Main loop

while True:

    client.loopMsg()

    choice = input("Enter your choice: ")

    # Search for artist
    if choice == '0':

        searchQuery = input("Ok, what's their name?:")
        # Get search results
        searchResults = client.search(searchQuery, 1, 0, 'artist')
        # Print artist details
        artist = searchResults['artists']['items'][0]

        print_artist_info(artist)

        artist_id = artist['id']

        all_tracks = client.getTracksOfArtist(artist_id)

        selected = []
        while True:
            selected.append(client.selectSong(all_tracks))
            if selected is None:
                break
            else:
                # Start playback
                client.start_playback(None, selected)
                # Wait 10 seconds
                time.sleep(10)
                # Get info about the current track
                current_track = client.getCurrentTrack()
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
