import feedparser


class Feed:
    """Class for getting RSS feed from desired URL"""

    def __init__(self, url=None, heading: list = None):
        """
        This method is specialized for www.telex.hu!
        """
        print('Initializing RSS feed parser...')
        self.feed = []
        if url is None:
            raise RuntimeError('Invalid URL!')
        if not heading:
            self.feed = [feedparser.parse(url)]
        elif heading:
            for item in heading:
                self.feed.append(feedparser.parse(
                    'https://telex.hu/rss/archivum?filters={%22superTagSlugs%22%3A[%22' + item + '%22]%2C%22parentId%22%3A[%22null%22]}'))

    def titles(self, howmany: int = None):
        """
        :param howmany: how many you want to get
        :return: titles of feed entries
        """
        print('Getting entries from RSS feed...')

        data = []
        if howmany is None:
            howmany = 0
            for item in self.feed:
                howmany += len(item['entries'])
        for item in self.feed:
            for i in item['entries'][:howmany]:
                data.append(i['title'])
        return data

    def source(self):
        """
        :return: the source of the rss feed
        """
        print('Getting RSS sources...')
        href = self.feed[0]['href']
        return href.split('/')[2]


if __name__ == "__main__":
    # TESTS #
    feed = Feed('https://telex.hu/rss', heading=['belfold', 'kult'])
    data = feed.titles(1)
    print(data)
