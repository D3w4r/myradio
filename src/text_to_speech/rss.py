import json
import logging

import feedparser

from src.data.enums import Constants
from src.data.repository import Repository
from src.dnn.model import CustomDnn

with open(Constants.CONFIG.value, 'r') as file:
    config = json.load(file)


class Feed:
    """Class for getting RSS feed from desired URL"""

    def __init__(self, url=None):

        self.feed = []
        if url is None:
            raise RuntimeError('Invalid URL!')
        self.feed = [feedparser.parse(url)]
        self.neural_net = CustomDnn()
        self.repository = Repository()
        self.logger = logging.getLogger(__name__)
        logging.info('Initializing RSS feed parser...')

    def get_news_titles(self, howmany: int = None):
        """
        :param howmany: how many you want to get
        :return: titles of feed entries
        """
        self.logger.debug('Getting entries from RSS feed...')

        input_news = []

        if howmany is None:
            howmany = 0
            for item in self.feed:
                howmany += len(item['entries'])
        for item in self.feed:
            for i in item['entries'][:howmany]:
                if i['title'][-1] is not ('?' or '!' or '.'):
                    input_news.append(i['title'] + '. ' + i['summary'])
                else:
                    input_news.append(i['title'] + ' ' + i['summary'])

        if input_news:
            predictions = self.neural_net.predict(input_news)
            return_data = []
            for category in predictions:
                if category in config['news']['interests']:
                    return_data.append(predictions[category])
                    self.logger.debug('Found matching category: ' + category)
            input_news = return_data

        input_news = self.repository.persist_and_filter_list(input_list=input_news,
                                                             path=Constants.RSS_REPOSITORY.value)

        self.logger.debug(input_news)
        return input_news

    def source(self):
        """
        :return: the source of the rss feed
        """
        self.logger.info('Getting RSS sources')
        href = self.feed[0]['href']
        return href.split('/')[2]
