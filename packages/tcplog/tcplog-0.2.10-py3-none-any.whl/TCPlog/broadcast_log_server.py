# -*- coding: utf-8 -*-

# Copyright (c) 2016,
# Karlsruhe Institute of Technology, Institute of Telematics
#
# This code is provided under the BSD 2-Clause License.
# Please refer to the LICENSE.txt file for further information.
#
# Author: Michael König
# Author: Mario Hock


import socket
import threading
import time

class BroadcastLogServer(object):
    """Broadcasts log data to each client connected via socket"""

    def __init__(self, host, port, log, msgQueue):
        """Initializes data structures"""
        self.__log = log #reference to global log-queue
        self.__clients = {} #queue per client
        self.__host = host
        self.__port = port
        self.__msgQueue = msgQueue

        self.__updateClientQueuesThread = threading.Thread(target=self.updateClientQueues)
        self.__updateClientQueuesThread.daemon = True
        self.__updateClientQueuesThread.start()

        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 512)
        self.__sock.bind((self.__host, self.__port))

    def updateClientQueues(self):
        """Update output-queue for each socket-client"""
        global shutdownFlag
        while not shutdownFlag:
            try:
                sampleObject = self.__log.popleft()
            except IndexError:
                time.sleep(0.0001)
            else:
                for clientID in self.__clients:
                    self.__clients[clientID].append(sampleObject)


    def getNumberOfClients(self):
        """Returns number of clients currently connected"""
        return len(self.__clients)

    def listen(self):
        """Listens for new clients. Starts thread to send data for each new client"""
        self.__sock.listen(50)
        global shutdownFlag
        while not shutdownFlag:
            try:
                client, address = self.__sock.accept()
            except:
                pass
            else:
                ip, port = address
