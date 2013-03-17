import os
import time
from heapq import merge
from feed import Feed


class User(object):

    MAX_STREAM_SIZE = 2000

    def __init__(self):
        self.id = os.urandom(8).encode('hex')
        self.feeds = []
        self.stream = []
        self.feed_indices = {}
        self.updated_at = time.time()

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
