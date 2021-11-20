import logging
import time

import spotipy
from spotipy.oauth2 import SpotifyOAuth

logging.basicConfig(level=logging.WARNING)


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
        self.current_track = self.get_current_track()

    def active_devices(self):
        """
        Get active devices

        :return: active device ids.
        """

        logging.debug('ACTIVE DEVICES:')
        devices = self.spotifyObject.devices()
        logging.debug(devices)
        if not devices:
            logging.error('No active device')
            raise RuntimeError('No active devices available')
        return devices

    def set_primary_device(self, devices, idx):
        """"
        Set the primary device id
        """

        self.device = devices['devices'][idx]['id']

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

    def restart_playback(self):
        uri = [self.current_track['item']['uri']]
        progress_ms = self.current_track['progress_ms']
        context = self.current_track['context']
        if context is None:
            album = self.current_track['item']['album']['uri']
            self.spotifyObject.start_playback(device_id=self.device, offset={"uri": uri[0]}, context_uri=album, position_ms=progress_ms)
        else:
            context = context['uri']
            self.spotifyObject.start_playback(device_id=self.device, offset={"uri": uri[0]}, context_uri=context,
                                          position_ms=progress_ms)

    def get_current_track(self):
        return self.spotifyObject.current_user_playing_track()

    def pause_playback(self):
        """
        Pauses playback and returns stopped track
        """
        stopped_track = self.current_track
        name = stopped_track['item']['name']
        self.spotifyObject.pause_playback(self.device)
        logging.info(f"Stopping last track: {name}")
        self.current_track = stopped_track

    def bbc_minute(self):
        query = self.search("BBC Minute", 1, 0, 'show')
        podcast = self.spotifyObject.show_episodes(show_id=query['shows']['items'][0]['uri'])
        self.start_playback(context_uri=None, uris=[podcast['items'][0]['uri']], progress_ms=0)

        time.sleep(62)


if __name__ == "__main__":
    client = Client('dewarhun')
    client.set_primary_device(client.active_devices(), 0)

    client.pause_playback()
    time.sleep(3)
    client.restart_playback()
