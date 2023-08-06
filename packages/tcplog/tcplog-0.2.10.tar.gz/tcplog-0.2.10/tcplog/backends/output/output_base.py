# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from ..backend_base import BackendBase

class OutputBase(BackendBase, metaclass=ABCMeta):
    """
    Base template for all output backends.
    """

    @abstractmethod
    def preLogging(self):
        """
        Executed before any samples are logged (usage example: write meta-data about log)
        """
        pass

    @abstractmethod
    def logSample(self):
        """
        Logs a single sample from the sample queue.
        """
        pass

    @abstractmethod
    def postLogging(self):
        """
        Executed after all samples are logged (usage example: write summary about logging-session)
        """
        pass
