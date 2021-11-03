import json
import logging

from data.mail import Gmail
from data.weather import Weather


class Speech:
    """
    General class for speech synthesising.
    """

    def __init__(self, language):
        self.logger = logging.getLogger(__name__)

    def synthesize(self, text):
        pass
