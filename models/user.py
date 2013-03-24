import os
from rss.models.feed import Feed
from rss.db.user_dbi import UserDBI
from rss.db.stream_dbi import StreamDBI


class User(object):

    DBI = UserDBI()

    def __init__(self, **kwargs):
        self._id = kwargs['_id']
        self.email = kwargs.get('email', '')
        self.feed_links = kwargs.get('feed_links', set())
        self.feed_names = kwargs.get('feed_names', {})

    def __repr__(self):
        return "User <%s, %s>" % (self.email, self._id)

    @classmethod
    def create(cls, email):
        _id = os.urandom(8).encode('hex')
        user = cls(_id=_id, email=email)
        user.save()
        return user

    @classmethod
    def list(cls):
        user_data = cls.DBI.list()
        return [cls(**user) for user in user_data]

    @classmethod
    def get_by_email(cls, email):
        data = cls.DBI.get_by_email(email)
        if not data:
            return None

        data['feed_names'] = dict(
            (k.replace('#', '.'), v) for k, v in data['feed_names'].items()
        )

        return cls(**data)

    @classmethod
    def get(cls, id):
        data = cls.DBI.get(id)
        if not data:
            return None

        data['feed_names'] = dict(
            (k.replace('#', '.'), v) for k, v in data['feed_names'].items()
        )

        data['feed_links'] = set(data['feed_links'])

        return cls(**data)

    def save(self):
        self.DBI.save(self)

    def add_feed(self, feed_link):
        self.feed_links.add(feed_link)
        self.save()

    def remove_feed(self, feed_link):
        changed = False
        try:
            self.feed_links.remove(feed_link)
            changed = True
            del self.feed_names[feed_link]
        except (ValueError, KeyError) as e:
            pass

        if changed:
            self.save()
            stream_dbi = StreamDBI(self)
            stream_dbi.remove_feed(feed_link)

    def get_starred_stream_with_count(self):
        stream_dbi = StreamDBI(self)
        stream = stream_dbi.get_stream(
            before_time=None,
            unread_only=False,
            starred=True
        )
        count = stream_dbi.get_unread_count()
        return stream, count

    def get_stream_with_count(self, unread_only=True):
        stream_dbi = StreamDBI(self)
        stream = stream_dbi.get_stream(
            before_time=None,
            unread_only=unread_only
        )
        count = stream_dbi.get_unread_count()
        return stream, count

    def get_stream(self, before_time=None, unread_only=True):
        stream_dbi = StreamDBI(self)
        return stream_dbi.get_stream(before_time, unread_only)

    def update_stream(self):
        StreamDBI(self).update_stream()
        self.save()

    def serialize(self):
        data = dict(self.__dict__)
        data['feed_names'] = dict(
            (k.replace('.', '#'), v) for k, v in data['feed_names'].items()
        )

        data['feed_links'] = list(data['feed_links'])
        return data
