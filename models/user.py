import os
import time
from heapq import merge
from rss.models.feed import Feed
from rss.db.user_dbi import UserDBI
from rss.db.stream_dbi import StreamDBI


class User(object):

    DBI = UserDBI()

    def __init__(self, id, email, **kwargs):
        self._id = id
        self.email = email
        self.feeds = kwargs.get('feeds', [])
        self.updated_at = time.time()

    @classmethod
    def create(cls, email):
        id = os.urandom(8).encode('hex')
        user = cls(id, email)
        user.save()
        return user

    def save(self):
        self.DBI.save(self)

    def add_feed(self, feed_link):
        self.feeds.append(Feed(feed_link))
        self.save()

    def get_stream(self, before_item=None, unread_only=True):
        stream_dbi = StreamDBI(self)
        stream.update_stream()
        return stream.get_stream(before_item, unread_only)
