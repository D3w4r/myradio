import json
import logging

import feedparser

import src.persistence.repository
from src.enums.enums import Constants

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

    def get_news_titles(self, howmany: int = None):
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

        repo = src.persistence.repository.Repository()
        title_data = repo.persist_and_filter_list(input_list=title_data,
                                                  path=Constants.RSS_REPOSITORY.value)
        return title_data

    def source(self):
        """
        :return: the source of the rss feed
        """
        logging.info('Getting RSS sources')
        href = self.feed[0]['href']
        return href.split('/')[2]


if __name__ == "__main__":
    # TESTS #
    with open(Constants.CONFIG.value, 'r') as file:
        config = json.load(file)
    feed = Feed('https://telex.hu/rss', heading=config['news']['category'])
    data = feed.get_news_titles(1)
    logging.info(data)
