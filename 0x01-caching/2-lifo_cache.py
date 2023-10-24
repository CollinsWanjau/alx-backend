#!/usr/bin/python3
""" LIFO Caching
"""
BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """ LIFO Caching
    """

    def __init__(self):
        super().__init__()

    def put(self, key, item):
        """ Discard the last item put in cache (LIFO algorithm)
        """
        if key is None or item is None:
            pass
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS \
                    and key not in self.cache_data.keys():
                last_key, last_item = self.cache_data.popitem()
                print('DISCARD: {}'.format(last_key))
            self.cache_data[key] = item

    def get(self, key):
        """ Must return the value in self.cache_date linked to key
        """
        if key not in self.cache_data(keys) or key is None:
            return None
        else:
            return self.cache_data.get(key)
