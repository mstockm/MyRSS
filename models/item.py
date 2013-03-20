from calendar import timegm
from rss.db.item_dbi import ItemDBI


class NoUserError(Exception):
    pass


class Item(object):
    def __init__(self, item_dict, DBI=None):
        try:
            self.feed_name = item_dict['feed_name']
            self.feed_link = item_dict['feed_link']
            self.date = item_dict['date']
            self.title = item_dict['title']
            self.link = item_dict['link']
            self.author = item_dict['author']
            self.id = item_dict['id']
            self.new = item_dict['new']
            self.content = item_dict['content']
        except KeyError:
            return None

        try:
            self._id = item_dict['_id']
        except:
            pass

        if DBI:
            self.DBI = DBI

    @classmethod
    def get_for_user(cls, item_id, user):
        DBI = ItemDBI(user)
        item_dict = DBI.get(item_id)
        if not item_dict:
            return None

        return cls(item_dict, DBI)

    def save(self):
        try:
            self.DBI.save(self)
        except AttributeError:
            raise NoUserError()

    @classmethod
    def create(cls, item_dict, feed_name, feed_link):
        value_dict = {}
        value_dict['feed_name'] = feed_name
        value_dict['feed_link'] = feed_link
        value_dict['date'] = timegm(item_dict['published_parsed'])
        value_dict['title'] = item_dict['title']
        value_dict['link'] = item_dict['link']
        value_dict['author'] = item_dict.get('author')
        value_dict['id'] = item_dict['id']
        value_dict['new'] = True

        try:
            value_dict['content'] = item_dict['content'][0]['value']
        except KeyError:
            value_dict['content'] = item_dict['summary']

        return cls(value_dict)

    def __repr__(self):
        return "Item<%s, %s (%s)>" % (
            self._id.encode('utf-8'),
            self.title.encode('utf-8'),
            self.feed_name.encode('utf-8')
        )

    def __lt__(self, other):
        return self.date > other.date

    def __eq__(self, other):
        if type(other) == type(u''):
            return self._id == other
        return self._id == other._id

    def mark_as_read(self):
        self.new = False

    def star(self):
        self.starred = True

    def unstar(self):
        self.starred = False

    def serialize(self):
        item_dict = dict(self.__dict__)
        if 'DBI' in item_dict:
            del item_dict['DBI']

        return item_dict
