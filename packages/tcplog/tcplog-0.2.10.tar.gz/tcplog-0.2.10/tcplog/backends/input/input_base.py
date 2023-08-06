# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from ..backend_base import BackendBase

class InputBase(BackendBase, metaclass=ABCMeta):
    """
    Base template for all input backends.
    """

    @abstractmethod
    def retrieveNewSamples(self):
        """
        Returns list of new samples.
        """
        pass
