from rss.db import get_connection


class UserDBI(object):
    def __init__(self):
        self._connection = get_connection()
        self._db = self._connection.rss
        self._collection = self._db.users

    def save(self, user):
        self._collection.save(user.serialize())

    def get(self, id):
        cursor = self._collection.find({'_id': id})
        try:
            return cursor.next()
        except:
            return None

    def get_by_email(self, email):
        cursor = self._collection.find({'email': email})
        try:
            return cursor.next()
        except:
            return None

    def list(self):
        return self._collection.find()
