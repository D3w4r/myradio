import feedparser


class Feed:
    """Class for getting RSS feed from desired URL"""

    def __init__(self, url=None):
        print('Initializing RSS feed parser...')
        if url is None:
            raise RuntimeError('Invalid URL!')
        self.feed = feedparser.parse(url)

    def all_titles(self):
        print('Getting all entries from RSS feed...')
        data = []
        for item in self.feed['entries']:
            data.append(item['title'])
        return data

    def top_five_entries(self):
        print('Getting top five entries from RSS feed...')
        data = []
        for item in self.feed['entries'][:5]:
            data.append(item['title'])
        return data


if __name__ == "__main__":
    # TESTS #
    feed = Feed('https://telex.hu/rss')
    data = feed.top_five_entries()
    print(data)
