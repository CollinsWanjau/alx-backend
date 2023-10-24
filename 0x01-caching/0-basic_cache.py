#!/usr/bin/python3
""" Basic dictionary
"""
BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """ A child class for BaseCaching
    """

    
    def __init__(self):
        """ Class initializer for parent class
        """
        super().__init__()

    def put(self, key, item):
        """ Assign to the dictionary the item value for the key
        """
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        """ Must return the value in self.cache_date linked to key
        """
        if key not in self.cache_data or key is None:
            return None
        else:
            return self.cache_data[key]
