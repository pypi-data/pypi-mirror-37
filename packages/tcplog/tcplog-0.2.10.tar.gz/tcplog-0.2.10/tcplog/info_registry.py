# -*- coding: utf-8 -*-

class InfoRegistry(object):
    """Holds global information to be shared between threads"""

    def __init__(self):
        """Does nothing"""
        self.__registry = {}

    def save(self, key, value):
        self.__registry[key] = value

    def load(self, key):
        if key in self.__registry:
            return self.__registry[key]
        else:
            return None
