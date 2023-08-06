# -*- coding: utf-8 -*-

# TODO move logic from tcplog.py to here

class Flows(object):
    """
    Holds all flow objects and provides meta-stats about them.
    """

    def __init__(self):
        self.flows = {}

    def addFlow(self, flowIdentifier, flow):
        self.flows[flowIdentifier] = flow

    def getFlow(self, flowIdentifier):
        return self.flows[flowIdentifier]

    def getFlows(self):
        return self.flows

    def numberOfActiveFlows(self):
        numberOfActiveFlows = 0
        for flowIdentifier in self.flows:
            if self.flows[flowIdentifier].isActive():
                numberOfActiveFlows += 1

        return numberOfActiveFlows

    def getActiveFlows(self):
        # TODO
        pass

    def getLongLivingFlows(self):
        # TODO
        # {k: v for k, v in points.items() if v[0] < 5 and v[1] < 5}
        pass
