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
                    'https://telex.hu/rss/archivum?filters={%22superTagSlugs%22%3A[%22' + item[
                        'name'] + '%22]%2C%22parentId'
                                  '%22%3A['
                                  '%22null%22]}'))

    def get_titles(self, howmany: int = None):
        """
        :param howmany: how many you want to get
        :return: titles of feed entries
        """
        logging.info('Getting entries from RSS feed...')

        title_data = []
        if howmany is None:
            howmany = 0
            for item in self.feed:
                howmany += len(item['entries'])
        for item in self.feed:
            for i in item['entries'][:howmany]:
                title_data.append(i['title'])
        self.persist(title_data)
        return title_data

    def source(self):
        """
        :return: the source of the rss feed
        """
        logging.info('Getting RSS sources')
        href = self.feed[0]['href']
        return href.split('/')[2]

    def persist(self, input: list):
        path = Constants.RSS_REPOSITORY.value
        if not os.path.exists(path):
            f = open(path, 'w')
            f.close()
        input = list(map(lambda item: hashlib.sha256(str(item).encode('utf-8')).hexdigest(), input))
        with open(path, 'rb') as file:
            if os.stat(path).st_size != 0:
                persisted: list = pickle.load(file)
                for input_item in input:
                    if input_item not in persisted:
                        persisted.append(input_item)
                        logging.debug('Appended ' + str(input_item) + ' to list')
        with open(path, 'wb') as file:
            pickle.dump(input, file)


if __name__ == "__main__":
    # TESTS #
    with open(Constants.INTERESTS.value, 'r') as file:
        headings = json.load(file)
    feed = Feed('https://telex.hu/rss', heading=headings)
    data = feed.get_titles(1)
    logging.info(data)
