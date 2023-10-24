#!/usr/bin/python3
""" Basic dictionary
"""
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    def put(self, key, item):
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        if key not in self.cache_data or key is None:
            return None
        else:
            return self.cache_data[key]
