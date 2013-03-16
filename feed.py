import feedparser
import time
from item import Item


class Feed(object):

    MAX_ITEMS = 100

    def __init__(self, feed_link):
        self.link = feed_link

        feed = feedparser.parse(feed_link)
        self.title = feed['feed'].get('title')

    def items_after_id(self, seek_id):
        feed = feedparser.parse(self.link)

        new_items = [Item(it, self.title, self.link) for it in feed['items']]

        if seek_id is None:
            return new_items

        try:
            overlap = new_items.index(seek_id)
            new_items = new_items[:overlap]
        except ValueError:
            pass

        return new_items
