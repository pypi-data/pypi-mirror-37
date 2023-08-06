# -*- coding: utf-8 -*-

import socket
import threading
import time
from collections import deque

SERVER_ADDRESS = ""
THREAD_STOPFLAG_WAIT = 0.000001 # in seconds

class BroadcastLogServer(object):
    """Broadcasts log data to each client connected via socket"""

    def __init__(self, options, logSamples, infoRegistry):
        """Initializes data structures"""
        self.options = options
        self.infoRegistry = infoRegistry
        self.__stopped = threading.Event()

        self.__logSamples = logSamples
        self.__clients = {} #queue per client
        self.__host = SERVER_ADDRESS
        self.__port = self.options.logPort

        self.__updateClientQueuesThread = threading.Thread(target=self.updateClientQueues)
        self.__updateClientQueuesThread.daemon = True
        self.__updateClientQueuesThread.start()

        self.__sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.__sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0) # use dual-stack sockt (IPv4+IPv6)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 512)
        self.__sock.bind((self.__host, self.__port))

    def initTearDown(self):
        self.__stopped.set()

    def appendNewSample(self, newSample):
        self.__logSamples.append(newSample)

    def updateClientQueues(self):
        """Update output-queue for each socket-client"""
        while(not self.__stopped.wait(0.0001)):
            try:
                sampleObject = self.__logSamples.popleft()
            except IndexError:
                time.sleep(0.0001)
            else:
                for clientID in self.__clients:
                    self.__clients[clientID].append(sampleObject)


    def getNumberOfClients(self):
        """Returns number of clients currently connected"""
        return len(self.__clients)

    def listen(self):
        """Listen for new clients on IPv4- & IPv6-Socket"""

        while(not self.__stopped.wait(0.0001)):
            self.listenSocket()

    def listenSocket(self):
        """Listens for new clients. Starts thread to send data for each new client"""
        self.__sock.listen(50)

        try:
            client, address = self.__sock.accept()

            if(self.options.debug):
                print(str(client))
                print(str(address))
        except:
            pass
        else:
            ip, port, x, y = address
            clientID = str(ip) + ":" + str(port)
            self.__clients[clientID] = deque()
            threading.Thread(target = self.sendToClient, args = (client,address, clientID), daemon=True).start()


    def initTearDown(self):
        self.__stopped.set()

    def sendToClient(self, client, address, clientID):
        """Performs the actual send operation of log data"""

        if(self.options.debug):
            print("New client connected: " + str(clientID))

        while(not self.__stopped.wait(0.0001)):
            try:
                sampleObject = self.__clients[clientID].popleft()
            except IndexError:
                self.__stopped.wait(THREAD_STOPFLAG_WAIT)
            else:
                try:
                    valueList = []
                    for val in self.options.valuesToLog:
                        valueList.append(str(getattr(sampleObject, val, None)))
                    logLine = ' '.join(valueList)
                    client.sendall(bytes(logLine + "\n", 'UTF-8'))
                    self.__stopped.wait(THREAD_STOPFLAG_WAIT)
                except:
                    if(self.options.debug):
                        print("Client disconnected or timedout: " + str(clientID))
                    del self.__clients[clientID]
                    client.close()
                    return False
        client.close()
