#!/usr/bin/env python3
"""
Hypermedia pagination
"""
from typing import Tuple, List
import csv
import math


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    '''
    Finds the correct indexes to paginate the dataset correctly and return the
    appropriate page of the dataset.
    The function should return a tuple of size two containing a start index and
    an end index corresponding to the range of indexes to return in a list for
    those particular pagination parameters.
    '''
    return ((page - 1) * page_size, page * page_size)


class Server:
    """Server class to prepare a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initialize"""
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """get page"""
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        # get the data from the csv
        data = self.dataset()

        try:
            # The method calls the index range function to calculate the start
            # and end indexes
            [start, end] = index_range(page, page_size)
            # Finally the method returns a slice of the dataset using the start
            # and end indexes
            return self.dataset()[start:end]
        except IndexError:
            return []

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """ returns a dictionary containing key-value pairs
        """
        data = self.get_page(page, page_size)
        # calculate total_pages using the length of dataset and page_size
        total_pages = math.ceil(len(self.dataset()) / page_size)
        # next page
        next_page = page + 1 if page < total_pages else None
        # prev page
        prev_page = page - 1 if page >= total_pages else None
        return {
            "page_size": page_size,
            "page": page,
            "data": data,
            "next_page": next_page,
            "prev_page": prev_page,
            "total_pages": total_pages
        }
