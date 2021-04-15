import spotipy
from spotipy.oauth2 import SpotifyOAuth


class Client:
    """A wrapper class for Spotipy"""

    def __init__(self,
                 username,
                 scope='user-read-private user-read-playback-state user-modify-playback-state'
                 ):
        self.username = username
        self.spotifyObject = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    def active_devices(self):
        print('ACTIVE DEVICES:')
        devices = self.spotifyObject.devices()
        for device in devices['devices']:
            print('name: ' + device['name'])
        return devices

    def set_primary_device(self, devices, idx):
        """"Set the primary device id"""

        self.device = devices['devices'][idx]['id']

    def get_primary_device(self):
        return self.device

    def current_track(self, verbose=None):
        track = self.spotifyObject.current_user_playing_track()
        if track is None:
            print('No track is playing')
        elif verbose == 'v':
            print(f"Currently playing track: -- {track['item']['name']} by {track['item']['artists'][0]['name']}")
        return track

    def get_artist(self, track):
        return track['item']['artists'][0]['name']

    def get_tracks_by_artist(self, artist_id):
        trackURIs = []
        idx = 0

        albums = self.spotifyObject.artist_albums(artist_id)
        albums = albums['items']

        for item in albums:
            print(f"Album: {item['name']}")
            albumId = item['id']

            trackResults = self.spotifyObject.album_tracks(albumId)
            trackResults = trackResults['items']

            for item in trackResults:
                print(str(idx) + ": " + item['name'])
                trackURIs.append(item['uri'])
                idx += 1
            print()

        return trackURIs

    def user(self):
        user = self.spotifyObject.current_user()
        return user

    def search(self, query, limit, offset, searchType='track'):
        return self.spotifyObject.search(query, limit, offset, searchType)

    def start_playback(self, context_uri, uris, progress_ms=None):
        self.spotifyObject.start_playback(device_id=self.device, context_uri=context_uri, uris=uris, offset=None,
                                          position_ms=progress_ms)

    def select_song(self, from_tracks):
        selection = input("Enter a song number: ")
        if selection == 'x':
            return None
        return from_tracks[int(selection)]

    def pause_playback(self):
        self.spotifyObject.pause_playback(self.device)
