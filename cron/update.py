import sys, os

sys.path.append(os.path.abspath('../..'))

from rss.models.user import User
from pprint import pprint


def update():
    users = User.list()
    for user in users:
        user.update_stream()


if __name__ == '__main__':
    update()
