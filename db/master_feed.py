from rss.db import get_connection
from rss.models.item import Item


class MasterFeed(object):
    def __init__(self):
        self._connection = get_connection
        self._db = self._connection.rss
        self._collection = self._db.items

    def get_latest_from_feed(self, feed):
        item_dict = self._collection.find({
            'feed_link': feed.link}).sort(
            'date', DESCENDING).limit(1).next()

        return Item(item_dict)

    def update_with_feed(self, feed):
        pass
