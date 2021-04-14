import logging
import os
import time
import venv
from json.decoder import JSONDecodeError

import spotipy
import vlc
from mutagen.wave import WAVE

from spotipy.oauth2 import SpotifyOAuth


class Client:

    def __init__(self,
                 username,
                 scope='user-read-private user-read-playback-state user-modify-playback-state'
                 ):
        self.username = username
        self.spotifyObject = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
        self.audio_info = {
            "file": r"D:\Data\ProjectLaboratory\myradio\src\weather.wav",
            "length": WAVE(r"D:\Data\ProjectLaboratory\myradio\src\weather.wav").info.length
        }

    def getActiveDevices(self):
        print('ACTIVE DEVICES:')
        devices = self.spotifyObject.devices()
        for device in devices['devices']:
            print('name: ' + device['name'] + ' id: ' + device['id'])
        return devices

    def setPrimaryDeviceId(self, devices, idx):
        self.device = devices['devices'][idx]['id']

    def getPrimaryDeviceId(self):
        return self.device

    def getCurrentTrack(self, verbose=None):
        track = self.spotifyObject.current_user_playing_track()
        if track is None:
            print('No track is playing')
        elif verbose == 'v':
            print(f"Current playing track: -- {track['item']['name']} by {track['item']['artists'][0]['name']}")
        return track

    def getArtistOfTrack(self, track):
        return track['item']['artists'][0]['name']

    def getTracksOfArtist(self, artist_id):
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

    def getUserInfo(self):
        user = self.spotifyObject.current_user()
        return user

    def getUserName(self, user):
        return user['display_name']

    def getFollowersNum(self, user):
        return user['followers']['total']

    def loopMsg(self):
        print()
        print("0 - Search for an artist")
        print("1 - exit")
        print()

    def search(self, query, limit, offset, searchType='track'):
        return self.spotifyObject.search(query, limit, offset, searchType)

    def start_playback(self, context_uri, uris, progress_ms=None):
        self.spotifyObject.start_playback(device_id=self.device, context_uri=context_uri, uris=uris, offset=None,
                                          position_ms=progress_ms)

    def selectSong(self, from_tracks):
        selection = input("Enter a song number to see the album art: ")
        if selection == 'x':
            return None
        return from_tracks[int(selection)]

    def simulate_speech(self):
        print(f"Audio length: {round(self.audio_info['length'])}")
        vlc.MediaPlayer(self.audio_info['file']).play()
        time.sleep(self.audio_info['length'])

    def pause_playback(self):
        self.spotifyObject.pause_playback(self.device)
