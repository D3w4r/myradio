import json
import logging

import feedparser

import data.repository
from data.enums import Constants
from data.repository import Repository
from dnn.model import RoBERTa

logging.basicConfig(level=logging.INFO)

with open(Constants.CONFIG.value, 'r') as file:
    config = json.load(file)


class Feed:
    """Class for getting RSS feed from desired URL"""

    def __init__(self, url=None):
        """
        This method is specialized for www.telex.hu!
        """

        logging.info('Initializing RSS feed parser...')
        self.feed = []
        if url is None:
            raise RuntimeError('Invalid URL!')
        self.feed = [feedparser.parse(url)]
        self.neural_net = RoBERTa()
        self.repository = Repository()

    def get_news_titles(self, howmany: int = None):
        """
        :param howmany: how many you want to get
        :return: titles of feed entries
        """
        logging.debug('Getting entries from RSS feed...')

        input_news = []

        if howmany is None:
            howmany = 0
            for item in self.feed:
                howmany += len(item['entries'])
        for item in self.feed:
            for i in item['entries'][:howmany]:
                if i['title'][-1] is not ('?' or '!' or '.'):
                    input_news.append(i['title'] + '. ' + i['description'])
                else:
                    input_news.append(i['title'] + ' ' + i['description'])

        if input_news:
            predictions = self.neural_net.predict(input_news)
            return_data = []
            for category in predictions:
                if category in config['news']['interests']:
                    return_data.append(predictions[category])
                    logging.info('Found matching category: ' + category)
            input_news = return_data

        input_news = self.repository.persist_and_filter_list(input_list=input_news,
                                                             path=Constants.RSS_REPOSITORY.value)
        return input_news

    def source(self):
        """
        :return: the source of the rss feed
        """
        logging.info('Getting RSS sources')
        href = self.feed[0]['href']
        return href.split('/')[2]


if __name__ == "__main__":
    # TESTS #
    feed = Feed(
        'https://telex.hu/rss/archivum?filters=%7B%22flags%22%3A%5B%22english%22%5D%2C%22parentId%22%3A%5B%22null%22%5D%7D')
    data = feed.get_news_titles(5)
    logging.info(data)
