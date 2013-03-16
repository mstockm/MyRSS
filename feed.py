import feedparser
from item import Item


class Feed(object):
    def __init__(self, feed_link):
        self.link = feed_link

        feed = feedparser.parse(feed_link)
        self.title = feed['feed'].get('title')
        self.items = [Item(item_dict) for item_dict in feed['items']]
