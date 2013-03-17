from pymongo import MongoClient


_connection = None


def get_connection():
    global _connection

    if not _connection:
        _connection = MongoClient()

    return _connection
