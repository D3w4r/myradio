import logging.config
import vlc
import time

from data.enums import Constants

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def play_audio(path: str):
    player = vlc.MediaPlayer()
    media = vlc.Media(Constants.CACHE_PATH.value + '/' + path)
    player.set_media(media)
    player.play()
    time.sleep(1)
    time.sleep(player.get_length() / 1000)