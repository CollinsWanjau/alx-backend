#!/usr/bin/python3
""" FIFO caching
"""
BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """Fifo caching"""

    def __init__(self):
        """ Initializer """
        super().__init__()

    def put(self, key, item):
        """Discarding the first item put in cache(FIFO algorithm)"""
        if key is None or item is None:
            pass
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS \
                    and key not in self.cache_data.keys():
                first_key = next(iter(self.cache_data.keys()))
                self.cache_data.pop(first_key)
                print('DISCARD: {}'.format(first_key))
            self.cache_data[key] = item

    def get(self, key):
        """ Must return the value in self.cache_date linked to key
        """
        if key not in self.cache_data or key is None:
            return None
        else:
            return self.cache_data[key]
