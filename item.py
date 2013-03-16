from calendar import timegm


class Item(object):
    def __init__(self, item_dict):
        self.date = timegm(item_dict['published_parsed'])
        self.title = item_dict['title']
        self.content = item_dict['content'][0]['value']
        self.link = item_dict['link']
        self.author = item_dict['author']
        self.id = item_dict['id']
