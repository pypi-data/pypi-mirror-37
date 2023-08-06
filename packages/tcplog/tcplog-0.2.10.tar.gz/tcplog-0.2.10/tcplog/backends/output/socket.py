# -*- coding: utf-8 -*-

import threading
from collections import deque

from .output_base import OutputBase
from .socket_broadcast_log_server import BroadcastLogServer

THREAD_JOIN_TIMEOUT = 1 # in seconds

class SocketOutput(OutputBase):
    def __init__(self, options, infoRegistry):
        self.options = options
        self.infoRegistry = infoRegistry
        self.tmpSampleQueue = deque()
        self.__socketServer = None

    def setSampleQueue(self, sampleQueue):
        self.sampleQueue = sampleQueue

    def setValuesToLog(self, valuesToLog):
        self.valuesToLog = valuesToLog

    def startUp(self):
        pass

    def startupCheck(self):
        pass

    def tearDown(self):
        if self.__socketServer is not None:
            self.__socketServer.initTearDown()
        self.__initSocketServerThread.join(THREAD_JOIN_TIMEOUT)

    def preLogging(self):
        self.__initSocketServerThread = threading.Thread(target=self.initSocketServer)
        self.__initSocketServerThread.daemon = True
        self.__initSocketServerThread.start()

    def initSocketServer(self):
        self.__socketServer = BroadcastLogServer(self.options, self.tmpSampleQueue, self.infoRegistry).listen()

    def logSample(self):
        try:
            sampleObject = self.sampleQueue.popleft()
        except IndexError:
            pass
        else:
            self.tmpSampleQueue.append(sampleObject)

    def postLogging(self):
        self.tearDown()


