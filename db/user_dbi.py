from rss.db import get_connection


class UserDBI(object):
    def __init__(self):
        self.connection = get_connection()
