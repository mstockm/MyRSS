from rss.db import get_connection


class UserDBI(object):
    def __init__(self):
        self._connection = get_connection()
        self._db = self._connection.rss
        self._collection = self._db.users

    def save(self, user):
        self._collection.save(user.serialize())

