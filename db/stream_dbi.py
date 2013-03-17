from rss.db import get_connection
from rss.models.item import Item


class StreamDBI(object):

    PAGE_SIZE = 20

    def __init__(self, user):
        self._connection = get_connection
        self._db = self._connection.rss
        self._collection = self._db['%s-items' % user._id]
        self.user = user

    def get_latest_from_feed(self, feed_link):
        try:
            item_dict = self._collection.find({
                'feed_link': feed_link}).sort(
                'date', DESCENDING).limit(1).next()
        except StopIteration:
            return None

        return Item(item_dict)

    def _update_with_feed(self, feed):
        latest = self.get_latest_from_feed(feed)
        new_items = feed.items_after_item(latest)

        if new_items:
            self._collection.insert(new_items)

    def get_stream(self, before_item=None, unread_only=True):
        query = {'feed_link': {'$in': [feed.link for link in self.user.feeds]}}
        if before_item:
            query['date'] = {'$lt': before_item.date}
        if unread_only:
            query['new'] = True

        items = self._collection.find(query).sort('date', DESCENDING).limit(
            self.PAGE_SIZE)
        return list(items)

    def update_stream(self):
        for link in self.user.feed_links:
            self._update_with_feed(link)
