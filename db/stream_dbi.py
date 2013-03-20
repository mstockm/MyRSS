from rss.db import get_connection
from rss.models.item import Item
from rss.models.feed import Feed
from pymongo import DESCENDING
from bson.objectid import ObjectId
from BeautifulSoup import BeautifulSoup


class StreamDBI(object):

    PAGE_SIZE = 5

    def __init__(self, user):
        self._connection = get_connection()
        self._db = self._connection.rss
        self._collection = self._db['items_%s' % user._id]
        self.user = user

    def get_latest_from_feed(self, feed_link):
        try:
            item_dict = self._collection.find({
                'feed_link': feed_link}).sort(
                'date', DESCENDING).limit(1).next()
        except StopIteration:
            return None

        return Item(item_dict)

    def _update_with_feed(self, feed_link):
        latest = self.get_latest_from_feed(feed_link)
        feed = Feed(feed_link)
        new_items = feed.items_after_item(latest)

        # Update user's feed name map
        self.user.feed_names[feed_link] = feed.name

        if new_items:
            mongo_items = [item.serialize() for item in new_items]
            self._collection.insert(mongo_items)

    def get_stream(self, before_time=None, unread_only=True):
        query = {}
        if before_time:
            query['date'] = {'$lt': int(before_time)}
        if unread_only:
            query['new'] = True

        items = self._collection.find(query).sort('date', DESCENDING).limit(
            self.PAGE_SIZE)
        output = []
        for item in items:
            content = BeautifulSoup(item['content']).prettify()
            item['content'] = unicode(content, 'utf-8')
            output.append(item)
        return output

    def get_unread_count(self):
        return self._collection.find({'new': True}).count()

    def remove_feed(self, feed_link):
        self._collection.remove({'feed_link': feed_link})

    def get_item_by_id(self, item_id):
        try:
            object_id = ObjectId(item_id)
            item_dict = self._collection.find(
                {'_id': item_id}).next()
        except StopIteration:
            return None

        return Item(item_dict)

    def update_stream(self):
        for link in self.user.feed_links:
            self._update_with_feed(link)
