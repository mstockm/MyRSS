import sys
from os.path import (
    join,
    realpath,
    dirname
)

path = realpath(join(dirname(realpath(__file__)), '../..'))
sys.path.append(path)


from rss.models.user import User
from pprint import pprint


def update():
    users = User.list()
    for user in users:
        user.update_stream()


if __name__ == '__main__':
    update()
