# coding=utf-8
"""
this version punches hole on the cache_line_list,
which is not efficient(5% loss compared to the other version of Random),
but fits in the whole framework and
_evictElement can be called by external functions
"""


import random

from PyMimircache.cache.abstractCache import Cache


class Random(Cache):
    def __init__(self, cache_size=1000, **kwargs):
        super().__init__(cache_size, **kwargs)
        self.cache_dict = dict()  # key -> linked list node (in reality, it should also contains value)
        self.cache_line_list = [] # to save all the keys, otherwise needs to populate from cache_set every time

    def has(self, req_id, **kwargs):
        """
        :param **kwargs:
        :param req_id: the key of cache request
        :return: whether the given key is in the cache or not
        """
        if req_id in self.cache_dict:
            return True
        else:
            return False

    def _update(self, req_item, **kwargs):
        """ the given element is in the cache, when it is requested again,
         usually we need to update it to new location, but in random, we don't need to do that
        :param **kwargs:
        :param req_item: the key of cache request
        :return: None
        """

        pass

    def _insert(self, req_item, **kwargs):
        """
        the given element is not in the cache, now insert it into cache
        :param **kwargs:
        :param req_item: the key of cache request
        :return: None
        """
        if len(self.cache_dict) >= self.cache_size:
            # must use cache_dict here, cache_line_list cannot be used
            # because of the punched holes
            self.evict()
        self.cache_dict[req_item] = ""
        self.cache_line_list.append(req_item)

    def _printCacheLine(self):
        for i in self.cache_dict:
            try:
                print(i.content, end='\t')
            except:
                print(i.content)

        print(' ')

    def evict(self, **kwargs):
        """
        evict one element from the cache line
        if we delete one element from list every time, it would be O(N) on
        every request, which is too expensive, so we choose to access a hole
        on the list every time we delete it, when there are too many holes
        we re-generate the cache line list
        :param **kwargs:
        :return: None
        """
        rand_num = random.randrange(0, len(self.cache_line_list))
        element = self.cache_line_list[rand_num]
        count = 0
        while not element:
            rand_num = random.randrange(0, len(self.cache_line_list))
            element = self.cache_line_list[rand_num]
            count += 1

        # mark this element as deleted, put a hole on it
        self.cache_line_list[rand_num] = None

        if count > 10:
            # if there are too many holes, then we need to resize the list
            new_list = [e for e in self.cache_line_list if e]
            del self.cache_line_list
            self.cache_line_list = new_list

        del self.cache_dict[element]

    def access(self, req_item, **kwargs):
        """
        :param **kwargs: 
        :param req_item: the key of cache request, it can be in the cache, or not in the cache
        :return: True if element in the cache
        """
        if self.has(req_item, ):
            self._update(req_item, )
            return True
        else:
            self._insert(req_item, )
            return False

    def __repr__(self):
        return "Random Replacement, given size: {}, current size: {}".format(self.cache_size,
                                                                             len(self.cache_dict),
                                                                             super().__repr__())
