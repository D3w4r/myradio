import threading

from myradio.src.client import Client


def info(subject):
    print(subject['name'])
    print(str(subject['followers']['total']) + " followers")
    print(subject['genres'][0])
    print()


def loopMsg():
    print()
    print("0 - Search for an artist")
    print("1 - Exit program")
    print("X - Exit current submenu")
    print()


class MusicThread(threading.Thread):

    def __init__(self, client: Client, threadName, threadID):
        threading.Thread.__init__(self)
        self.name = threadName
        self.id = threadID
        self.client = client
        self.flag = False

    def run(self):
        print(f'Started thread - {self.id} :: {self.name}')
        # Set devices
        devices = self.client.active_devices()
        self.client.set_primary_device(devices, 0)
        # Info of current track
        current_track = self.client.current_track('v')
        artist = self.client.get_artist(current_track)
        print(artist)
        # User info
        user = self.client.user()
        username = self.client.user()['display_name']
        followers = user['followers']['total']
        print()
        print(f'Username: {username}')
        print(f'Followers: {followers}')

        # Main loop
        while True:
            loopMsg()
            choice = input("Enter your choice: ")
            # Search for artist
            if choice == '0':
                search_query = input("Ok, what's their name?: ")
                if search_query.lower() == 'x':
                    exit(0)
                # Get search results
                search_results = self.client.search(search_query, 1, 0, 'artist')
                # Print artist details
                artist = search_results['artists']['items'][0]
                info(artist)

                artist_id = artist['id']
                all_tracks = self.client.get_tracks_by_artist(artist_id)

                selected = []

                while True:
                    selection = self.client.select_song(all_tracks)
                    if selection is None:
                        break
                    else:
                        self.flag = True
                        selected.append(selection)
                        self.client.start_playback(None, selected)

                        selected.pop()

            elif choice == '1':
                break

    def getFlag(self):
        return self.flag
