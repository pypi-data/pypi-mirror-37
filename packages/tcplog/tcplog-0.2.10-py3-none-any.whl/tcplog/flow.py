# -*- coding: utf-8 -*-

import time

DERIVED_VALUES = ['minRtt', 'maxRtt', 'avgRtt', 'smoothedRtt', 'throughput', 'smoothedThroughput', 'assumedLosses', 'transferedData']
DERIVED_VALUES_UNITS = ['ms', 'ms', 'ms', 'ms', 'byte/s', 'byte/s', '#', 'byte']
ACTIVITY_THRESHOLD = 10 # seconds
SMOOTHED_THROUGHPUT_TIME_DELTA = 0.5 #second
EPHEMERAL_THRESHOLD = 2 # number of samples

class Flow(object):
    """Data structure to represent a filtered flow"""

    def __init__(self, flowIdentifier, srcIp, srcPort, dstIp, dstPort, sample):
        """Initializes new flow"""
        self.flowIdentifier = flowIdentifier
        self.srcIp = srcIp
        self.srcPort = srcPort
        self.dstIp = dstIp
        self.dstPort = dstPort
        self.srcHostname = None
        self.dstHostname = None
        # self.flowDirection = "in"
        # self.flowDirection = "out"
        self.timestampOfFirstActivity = time.time()
        self.timestampOfLastActivity = self.timestampOfFirstActivity
        self.currentSample = sample
        self.previousSample = sample
        self.timeBetweenCurrentAndPreviousSample = 0
        self.minRtt = sample.rtt
        self.maxRtt = sample.rtt
        self.avgRtt = sample.rtt
        self.smoothedRtt = sample.rtt
        self.transferedData = 0
        self.throughput = 0
        self.throughput_1 = 0 # t(x-1)
        self.throughput_2 = 0 # t(x-2)
        self.throughput_3 = 0 # t(x-3)
        self.smoothedThroughput = 0
        self.assumedLosses = 0
        self.numberOfSamples = 1
        self.logStatus = False
        self.timestampOfLastThroughputCalc = sample.relativeTimestamp
        self.seqLastThroughputCalc = sample.seq
        self.seqOfFirstActivity = sample.seq
        self.ignoreFlag = False

    def updateFlow(self, newSample):
        self.logStatus = False
        self.numberOfSamples += 1
        self.timestampOfLastActivity = time.time()
        self.previousSample = self.currentSample
        self.currentSample = newSample
        self.timeBetweenCurrentAndPreviousSample = self.currentSample.absoluteTimestamp - self.previousSample.absoluteTimestamp
        self.updateDerivedValues()
        self.appendDerivedValuesToCurrentSample()

    def updateDerivedValues(self):
        # calculate misc rtt-vals
        self.minRtt = min(self.minRtt, self.currentSample.rtt)
        self.maxRtt = max(self.maxRtt, self.currentSample.rtt)
        self.avgRtt = 0.5 * self.currentSample.rtt + 0.5 * self.avgRtt
        self.smoothedRtt = 0.01 * self.currentSample.rtt + 0.99 * self.smoothedRtt

        # NOTE: Packet loss is assumed, when SSThresh is decreased (significantly)
        # --> It was observed that TCP-Vegas repeatedly reduces SSThresh by a small amount, e.g. after Slow-Start (under some circumstances)
        if(self.previousSample.sst > (self.currentSample.sst + min(int(self.previousSample.sst) * 0.2, 10)) ):
            self.assumedLosses += 1

        # calculate throughput
        self.throughput = (self.currentSample.seq - self.previousSample.seq) if (self.currentSample.seq - self.previousSample.seq) >= 0 \
            else (int("0xffffffff",0) - self.previousSample.seq + self.currentSample.seq)
        self.throughput /= self.timeBetweenCurrentAndPreviousSample  # byte/s
        self.throughput *= 8 / 1000 / 1000 # mbit/s

        ## variant 1: wma
        # self.smoothedThroughput = 0.025 * self.throughput + 0.975 * self.smoothedThroughput

        ## variant 2: exponential smoothing
        # self.smoothedThroughput = self.smoothedThroughput + (0.005 * (self.throughput - self.smoothedThroughput))

        ## variant 3 (old): calc smoothed throughput once each intervall (SMOOTHED_THROUGHPUT_TIME_DELTA)
        # self.smoothedThroughput = self.throughput
        # calculate smoothed throughput (to minify burst fragments)
        # tpCalcDelta = self.currentSample.relativeTimestamp - self.timestampOfLastThroughputCalc
        # if(tpCalcDelta >= SMOOTHED_THROUGHPUT_TIME_DELTA):
        #     throughput = (self.currentSample.seq - self.seqLastThroughputCalc) if (self.currentSample.seq - self.seqLastThroughputCalc) >= 0 \
        #         else (int("0xffffffff",0) - self.seqLastThroughputCalc + self.currentSample.seq)
        #     throughput /= tpCalcDelta  # byte/s
        #     throughput *= 8 / 1000 / 1000 # mbit/s
        #     # self.smoothedThroughput = throughput
        #     self.timestampOfLastThroughputCalc = self.currentSample.relativeTimestamp
        #     self.seqLastThroughputCalc = self.currentSample.seq
        #     self.smoothedThroughput = 0.05 * throughput + 0.95 * self.smoothedThroughput

        # variant 4: Savitzky-Golay + wma
        # Savitzky-Golay:
        smoothedThroughput_sgFilter = 0.7 * self.throughput + 0.4 * self.throughput_1 + 0.1 * self.throughput_2 - 0.2 * self.throughput_3
        self.throughput_3 = self.throughput_2
        self.throughput_2 = self.throughput_1
        self.throughput_1 = self.throughput
        # now wma:
        self.smoothedThroughput = 0.7 * self.smoothedThroughput + 0.3 * smoothedThroughput_sgFilter

        self.transferedData = self.currentSample.seq - self.seqOfFirstActivity
        # TODO:
        # IN- vs OUT-data
        # self.transferedOutData = self.currentSample.seq - self.seqOfFirstActivity
        # self.transferedInData = self.currentSample.bytesAcked - self.seqOfFirstActivity


    def appendDerivedValuesToCurrentSample(self):
        for val in DERIVED_VALUES:
            valueContent = (getattr(self, val, "_"))
            setattr(self.currentSample, val, valueContent)

    def timeSinceLastActivity(self):
        return (time.time() - self.timestampOfLastActivity)

    def totalActiveTime(self):
        return (self.timestampOfLastActivity - self.timestampOfFirstActivity)

    def getListOfDerivedValues(self):
        return DERIVED_VALUES

    def getListOfDerivedValuesUnits(self):
        return DERIVED_VALUES_UNITS

    def isActive(self):
        return (self.timeSinceLastActivity() < ACTIVITY_THRESHOLD)

    def isEphemeral(self):
        """
        If there is only a single sample (yet) count flow as short-lived.
        """
        return (self.numberOfSamples < EPHEMERAL_THRESHOLD)

    # TODO: move into Flows
    def getLogStatus(self):
        return self.logStatus

    # TODO: move into Flows
    def setLogStatus(self, logStatus):
        self.logStatus = logStatus

    def isIngressFlow(self):
        return (self.flowDirection == "in")

    def isEgressFlow(self):
        return (self.flowDirection == "out")

    # TODO: move into Flows
    def hasIgnoreFlag(self):
        return self.ignoreFlag

    # TODO: move into Flows
    def activateIgnoreFlag(self):
        self.ignoreFlag = True

    def setIgnoreFlagByMinThroughput(self, minThroughput):
        if(self.smoothedThroughput <= minThroughput or self.smoothedThroughput is None):
            self.ignoreFlag = True # ignore this flow due low throughput
        else:
            self.ignoreFlag = False

