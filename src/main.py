from client import Client

username = 'dewarhun'

client = Client(username)

# Devices
devices = client.getActiveDevices()
# Set primary device
client.setPrimaryDeviceId(devices, 0)
# Current track information
current_track = client.getCurrentTrack()
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

        print()
        searchQuery = input("Ok, what's their name?:")
        print()
        # Get search results
        searchResults = client.search(searchQuery, 1, 0, 'artist')
        # Print artist details
        artist = searchResults['artists']['items'][0]
        print(artist['name'])
        print(str(artist['followers']['total']) + " followers")
        print(artist['genres'][0])
        print()

        artist_id = artist['id']

        all_tracks = client.getTracksOfArtist(artist_id)

        selected = []
        while True:
            selected.append(client.selectSong(all_tracks))
            if selected == None:
                break
            else:
                client.start_playback(None, selected)
                selected.pop()

    if choice == '1':
        break