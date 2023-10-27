#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""


import csv
import math
from typing import List, Dict


class Server:
    """
    Server class to paginate a db of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset for future use
        - The method first checks if the dataset is already cached in the
        attribute.If it is, the cached dataset is returned.
        - If the dataset is not cached, the method reads the CSV file using
        open() and csv.reader().
        - It then creates a list of lists called dataset by iterating over
        the rows in the CSV using a list comprehension.
        - Finally, the method assigns the sliced dataset(excluding the header
        row) to the __dataset attribute and returns it.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting posistion, starting at 0
        - Dict indicates that a function should return a dict with integer
        keys and list.
        - If indexed dataset is None, the code retrieves the dataset() and
        creates a truncated version of the dataset containing the first 1000
        rows.
        - the code then creates a new dictionary called __indexed_dataset using
        a dictionary comprehension.
        - This allows for faster access to specific rows in the dataset, as the
        row number can be used as a keyto retrieve the corresponding row from
        the dictionary.
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """Get hyper index"""
        if index is None:
            index = 0

        assert isinstance(index, int)
        assert 0 <= index < len(self.indexed_dataset())
        assert isinstance(page_size, int) and page_size > 0

        data = []
        next_index = index + page_size

        for value in range(index, next_index):
            if self.indexed_dataset().get(value):
                data.append(self.indexed_dataset()[value])
            else:
                value += 1
                next_index += 1

        return {
            'index': index,
            'data': data,
            'page_size': page_size,
            'next_index': next_index
        }
