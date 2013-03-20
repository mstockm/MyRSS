from rss.db import get_connection
from bson.objectid import ObjectId


class ItemDBI(object):
    def __init__(self, user):
        self._connection = get_connection()
        self._db = self._connection.rss
        self._collection = self._db['items_%s' % user._id]
        self.user = user

    def get(self, item_id):
        try:
            object_id = ObjectId(item_id)
            item_dict = self._collection.find(
                {'_id': object_id}).next()
        except StopIteration:
            return None

        return item_dict

    def save(self, item):
        item_dict = item.serialize()
        self._collection.save(item_dict)
