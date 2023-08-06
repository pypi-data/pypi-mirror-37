# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class BackendBase(metaclass=ABCMeta):
    """
    Base template for all backends
    """

    @abstractmethod
    def startupCheck():
        """
        Every backend must be able to determine if all of their necessary dependencies are met
        """
        pass

    @abstractmethod
    def startUp():
        """
        Initialize backend's dependencies (eg: file opening...)
        """
        pass

    @abstractmethod
    def tearDown():
        """
        Executed at programme shutdown: Every backend must perform a cleanup (eg: close files...)
        """
        pass
