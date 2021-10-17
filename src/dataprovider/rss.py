import json
import logging
import os.path
import pickle
import hashlib

import feedparser

from src.constants.constats import Constants

logging.basicConfig(level=logging.INFO)


class Feed:
    """Class for getting RSS feed from desired URL"""

    def __init__(self, url=None, heading: list = None):
        """
        This method is specialized for www.telex.hu!
        """

        logging.info('Initializing RSS feed parser...')
        self.feed = []
        if url is None:
            raise RuntimeError('Invalid URL!')
        if not heading:
            self.feed = [feedparser.parse(url)]
        elif heading:
            for item in heading:
                self.feed.append(feedparser.parse(
                    'https://telex.hu/rss/archivum?filters={%22superTagSlugs%22%3A[%22' + item + '%22]%2C%22parentId'
                                                                                                 '%22%3A['
                                                                                                 '%22null%22]}'))

    def get_news(self, howmany: int = None):
        """
        :param howmany: how many you want to get
        :return: titles of feed entries
        """
        logging.debug('Getting entries from RSS feed...')

        title_data = []
        if howmany is None:
            howmany = 0
            for item in self.feed:
                howmany += len(item['entries'])
        for item in self.feed:
            for i in item['entries'][:howmany]:
                title_data.append(i['title'])
        title_data = self.persist_and_filter(title_data)
        logging.info(title_data)
        return title_data

    def source(self):
        """
        :return: the source of the rss feed
        """
        logging.info('Getting RSS sources')
        href = self.feed[0]['href']
        return href.split('/')[2]

    def persist_and_filter(self, input: list):
        path = Constants.RSS_REPOSITORY.value
        to_return = []
        if not os.path.exists(path):
            f = open(path, 'w')
            f.close()
        if os.stat(path).st_size != 0:
            with open(path, 'rb') as file:
                news_store: list = pickle.load(file)
            logging.info('Persisted news store found')
            input = list(map(lambda item: hashlib.sha256(str(item).encode('utf-8')).hexdigest(), input))
            for input_item in input:
                if input_item not in news_store:
                    news_store.append(input_item)
                    with open(path, 'wb') as out:
                        pickle.dump(news_store, out)
                    to_return.append(input_item)
                    logging.info('Appended ' + str(input_item) + ' to return list')
        else:
            logging.info('No persisted news found')
            with open(path, 'wb') as file:
                pickle.dump(input, file)
            to_return = input
        return to_return


if __name__ == "__main__":
    # TESTS #
    with open(Constants.INTERESTS.value, 'r') as file:
        headings = json.load(file)
    feed = Feed('https://telex.hu/rss', heading=headings)
    data = feed.get_news(1)
    logging.info(data)
