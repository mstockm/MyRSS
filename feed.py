import feedparser
import time
from item import Item


class Feed(object):

    MAX_ITEMS = 100

    def __init__(self, feed_link):
        self.link = feed_link

        feed = feedparser.parse(feed_link)
        self.title = feed['feed'].get('title')
        self.updated = time.time()

    def get_items(self):
        feed = feedparser.parse(self.link)

        new_items = [Item(item_dict) for item_dict in feed['items']]

        if self.items == []:
            self.items = new_items
            return new_items

        try:
            overlap = new_items.index(self.items[0])
            new_items = new_items[:overlap]
        except ValueError:
            pass

        new_items.extend(self.items)
        self.items = new_items

        if len(self.items) > MAX_ITEMS:
            self.items = self.items[:MAX_ITEMS]

        self.updated = time.time()
        return self.items
