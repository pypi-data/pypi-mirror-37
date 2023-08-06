# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from ..backend_base import BackendBase

class GuiBase(BackendBase, metaclass=ABCMeta):
    @abstractmethod
    def repaint(self):
        """
        Repaints gui with all elements.
        """
        pass

    @abstractmethod
    def refresh(self):
        """
        Processes user input and calls rapaint if need be.
        """
        pass

    @abstractmethod
    def initTearDown(self):
        """
        Initializes a teardown and alerts user if need be.
        """
        pass
