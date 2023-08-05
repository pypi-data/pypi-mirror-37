class Item(object):

    def __init__(self, item_data):
        self._item_data = item_data

    @property
    def lat(self):
        return self._item_data['lat']

    @property
    def long(self):
        return self._item_data['long']

    @property
    def link(self):
        return self._item_data['link']

