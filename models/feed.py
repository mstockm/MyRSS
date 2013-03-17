import feedparser
import time
from item import Item


class Feed(object):

    MAX_ITEMS = 100

    def __init__(self, feed_link):
        self.link = feed_link

    def items_after_item(self, seek):
        feed = feedparser.parse(self.link)
        title = feed['feed'].get('title')

        new_items = [Item.create(item, title, self.link) for item in feed['items']]

        if seek is None:
            return new_items

        try:
            overlap = new_items.index(seek)
            new_items = new_items[:overlap]
        except ValueError:
            pass

        return new_items
