import os
from json.decoder import JSONDecodeError

import spotipy
import spotipy.util as util


class Client:

    def __init__(self,
                 username,
                 scope='user-read-private user-read-playback-state user-modify-playback-state',
                 redirect_uri='http://localhost:8080/'
                 ):
        self.username = username
        self.scope = scope
        self.redirect_uri = redirect_uri
        # THESE ARE NOT TO BE MODIFIED NOR TO BE REVEALED TO ANYONE #
        self.client_id = '62faefbbb3f84ccf8a2c8626a3f2f89e'
        self.client_secret = 'cfd44c47314f4d6795d32ab78d78297f'
        # THESE ARE NOT TO BE MODIFIED NOR TO BE REVEALED TO ANYONE #

        try:
            print('Accessing API with user token')
            print()
            token = util.prompt_for_user_token(
                self.username,
                self.scope,
                self.client_id,
                self.client_secret,
                self.redirect_uri
            )
        except (AttributeError, JSONDecodeError):
            os.remove(f'.cache-{username}')
            token = util.prompt_for_user_token(
                self.username,
                self.scope,
                self.client_id,
                self.client_secret,
                self.redirect_uri
            )
        self.spotifyObject = spotipy.Spotify(auth=token)

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

    def getCurrentTrack(self):
        track = self.spotifyObject.current_user_playing_track()
        if track is None:
            print('No track is playing')
        else:
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

    def start_playback(self, context_uri, uris):
        self.spotifyObject.start_playback(self.device, context_uri, uris)

    def selectSong(self, from_tracks):
        selection = input("Enter a song number to see the album art: ")
        if selection == 'x':
            return None
        return from_tracks[int(selection)]
