import time

import vlc

from src.data.enums import Constants

config_path = 'src/config/'

def play_audio(path: str):
    player = vlc.MediaPlayer()
    media = vlc.Media(Constants.CACHE_PATH.value + '/' + path)
    player.set_media(media)
    player.play()
    time.sleep(1)
    time.sleep(player.get_length() / 1000)