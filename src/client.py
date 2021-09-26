import spotipy
import logging
from spotipy.oauth2 import SpotifyOAuth

logging.basicConfig(level=logging.INFO)


class Client:
    """
    A wrapper class for Spotipy
    """

    def __init__(self,
                 username,
                 scope='user-read-private user-read-playback-state user-modify-playback-state'
                 ):
        self.username = username
        self.spotifyObject = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    def active_devices(self):
        """
        Get active devices

        :return: active device ids.
        """

        logging.info('ACTIVE DEVICES:')
        devices = self.spotifyObject.devices()
        if not devices:
            logging.error('No active device')
            raise RuntimeError('No active devices available')
        for device in devices['devices']:
            logging.info(device['name'])
        return devices

    def set_primary_device(self, devices, idx):
        """"
        Set the primary device id
        """

        self.device = devices['devices'][idx]['id']

    def get_primary_device(self):
        """
        Get primary device

        :return: The device used to modify playback state
        """

        return self.device

    def current_track(self, verbose=None):
        """
        Get current track information

        :param verbose: if set, it prints the info on the console.
        :return: the currently playing track
        """

        track = self.spotifyObject.current_user_playing_track()
        if track is None:
            print('No track is playing')
        elif verbose == 'v':
            print(f"Currently playing track: -- {track['item']['name']} by {track['item']['artists'][0]['name']}")
        return track

    def get_artist(self, track):
        """
        Get the artist of the given track.

        :param track: the track, of which artist you want to get.
        :return: the artist
        """
        return track['item']['artists'][0]['name']

    def get_tracks_by_artist(self, artist_id):
        """
        Get tracks of the given artist.

        :param artist_id: the artist, whom tracks you want to get.
        :return: every track of that artist
        """
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
        """
        Get current user info

        :return: the currently active user.
        """
        user = self.spotifyObject.current_user()
        return user

    def search(self, query, limit, offset, searchType='track'):
        """
        Search query using Spotipy API

        Check the official documentation for further info

        :return: response for the query
        """
        return self.spotifyObject.search(query, limit, offset, searchType)

    def start_playback(self, context_uri, uris, progress_ms=None):
        """
        Starts playback
        """
        self.spotifyObject.start_playback(device_id=self.device, context_uri=context_uri, uris=uris, offset=None,
                                          position_ms=progress_ms)

    def select_song(self, from_tracks):
        """
        Selects track uri from the given list of tracks
        :param from_tracks:
        :return: uri of the selected track
        """
        selection = input("Enter a song number: ")
        if selection == 'x':
            return None
        return from_tracks[int(selection)]

    def pause_playback(self):
        """
        Pauses playback
        """
        self.spotifyObject.pause_playback(self.device)
