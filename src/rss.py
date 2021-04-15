import feedparser


class Feed:
    """Class for getting RSS feed from desired URL"""

    def __init__(self, url=None):
        print('Initializing RSS feed parser...')
        if url is None:
            raise RuntimeError('Invalid URL!')
        self.feed = feedparser.parse(url)

    def titles(self, howmany: int = None):
        print('Getting entries from RSS feed...')
        data = []
        if howmany is None:
            howmany = len(self.feed['entries'])
        for item in self.feed['entries'][:howmany]:
            data.append(item['title'])
        return data

    def source(self):
        print('Getting RSS sources...')
        href = self.feed['href']
        return href.split('/')[2]


if __name__ == "__main__":
    # TESTS #
    feed = Feed('https://telex.hu/rss')
    data = feed.titles(5)
    print(data)
