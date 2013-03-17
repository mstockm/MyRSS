import os
import time
from heapq import merge
from rss.models.feed import Feed
from rss.db.user_dbi import UserDBI


class User(object):

    MAX_STREAM_SIZE = 2000
    DBI = UserDBI()

    def __init__(self, id, email, **kwargs):
        self._id = id
        self.email = email
        self.feeds = kwargs.get('feeds', [])
        self.stream = kwargs.get('stream', [])
        self.feed_indices = kwargs.get('feed_indices', {})
        self.updated_at = time.time()

    @classmethod
    def create(cls, email):
        id = os.urandom(8).encode('hex')
        user = cls(id, email)
        user.save()
        return user

    def save(self):
        pass

    def add_feed(self, feed_link):
        self.feeds.append(Feed(feed_link))

    def update_stream(self):
        new_streams = []

        for feed in self.feeds:
            index = self.feed_indices.get(feed.link)
            new_items = feed.items_after_id(index)

            try:
                self.feed_indices[feed.link] = new_items[0].id
            except IndexError:
                pass

            new_streams.append(new_items)

        new_stream = list(merge(*new_streams))
        new_stream.extend(self.stream)
        self.stream = new_stream

        if len(self.stream) > self.MAX_STREAM_SIZE:
            self.stream = self.stream[:self.MAX_STREAM_SIZE]

        self.updated_at = time.time()
