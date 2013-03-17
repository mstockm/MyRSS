from calendar import timegm


class Item(object):
    def __init__(self, item_dict, feed_name, feed_link):
        self.feed_name = feed_name
        self.feed_link = feed_link
        self.date = timegm(item_dict['published_parsed'])
        self.title = item_dict['title']
        self.link = item_dict['link']
        self.author = item_dict['author']
        self.id = item_dict['id']
        self.new = True

        try:
            self.content = item_dict['content'][0]['value']
        except KeyError:
            self.content = item_dict['summary']

    def __repr__(self):
        return "Item<%s, %s (%s)>" % (
            self.id.encode('utf-8'),
            self.title.encode('utf-8'),
            self.feed_name.encode('utf-8')
        )

    def __lt__(self, other):
        return self.date > other.date

    def __eq__(self, other):
        if type(other) == type(u''):
            return self.id == other
        return self.id == other.id

    def mark_as_read(self):
        self.new = False
