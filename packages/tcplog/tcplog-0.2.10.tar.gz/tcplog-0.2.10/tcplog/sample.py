# -*- coding: utf-8 -*-

import time

class Sample(object):
    """Data structure ro represent a single log sample object"""

    def __init__(self, srcIp, srcPort, dstIp, dstPort):
        """Initializes a new sample object"""

        self.absoluteTimestamp = time.time()
        self.srcIp = srcIp
        self.srcPort = srcPort
        self.dstIp = dstIp
        self.dstPort = dstPort
        self.src = str(self.srcIp) + ":" + str(self.srcPort)
        self.dst = str(self.dstIp) + ":" + str(self.dstPort)
        self.seq = 0
        self.sst = 0

    def getFlowIdentifier(self):
        return self.src + "-" + self.dst

