# -*- coding: utf-8 -*-

import sys
import threading
import time
# import netifaces
# from netifaces import AF_INET, AF_INET6
from collections import deque
from collections import OrderedDict

from .flow import Flow

THREAD_STOPFLAG_WAIT = 0.000001 # in seconds
THREAD_JOIN_TIMEOUT = 1 # in seconds
THREAD_TESTTIMEOUTS_WAIT = 0.5 # in seconds
THREAD_MISC_WAIT = 2 # in seconds

class TcpLog():
    def __init__(self, inputBackend, outputBackend, guiBackend, options, infoRegistry):
        self.inputBackend = inputBackend
        self.outputBackend = outputBackend
        self.guiBackend = guiBackend
        self.options = options
        self.infoRegistry = infoRegistry

    def run(self):
        """Initializes data structures and start worker-threads"""

        self.__stopped = threading.Event()

        self.startTimestamp = self.infoRegistry.load('startTime')
        self.timestampLastSample = 0
        self.numberOfLoggedSamples = 0

        # self.ownIpAdresses = self.determineOwnIpAdresses()
        # self.infoRegistry.save('ownIpAdresses', self.ownIpAdresses)
        self.flows = OrderedDict()

        self.__processInputThread = None
        self.__processOutputThread = None
        self.__processGuiThread = None
        self.__autoStopControlThread = None
        # self.__processMiscThread = None

        # init threads
        self.__processInputThread = threading.Thread(target=self.processInput)
        self.__processInputThread.daemon = True
        self.__processOutputThread = threading.Thread(target=self.processOutput)
        self.__processOutputThread.daemon = True

        # process misc. stuff --> utility thread
        # self.__processMiscThread = threading.Thread(target=self.processMisc)
        # self.__processMiscThread.daemon = True

        if(self.options.quiet != True and self.options.outputBackend != "stdout"):
            self.__processGuiThread = threading.Thread(target=self.processGui)
            self.__processGuiThread.daemon = True
            self.__processGuiThread.start()

        if(self.options.inActivityTimeout > 0 or self.options.hardTimeout > 0):
            self.__autoStopControlThread = threading.Thread(target=self.testAutoTimeouts)
            self.__autoStopControlThread.daemon = True
            self.__autoStopControlThread.start()

        self.__processInputThread.start()
        self.__processOutputThread.start()
        # self.__processMiscThread.start()

        while(not self.__stopped.wait(THREAD_STOPFLAG_WAIT)):
            self.__stopped.wait(0.5)

        if(self.options.debug):
            print("End of main thread reached.")

    def processInput(self):
        while(not self.__stopped.wait(THREAD_STOPFLAG_WAIT)):
            newSamples = self.inputBackend.retrieveNewSamples()
            for sampleCandidate in newSamples:
                if(sampleCandidate is not None):
                    flowIdentifier = sampleCandidate.getFlowIdentifier()
                    if flowIdentifier in self.flows:
                        # known flow
                        thisFlow = self.flows[flowIdentifier]
                        if (sampleCandidate.absoluteTimestamp - thisFlow.currentSample.absoluteTimestamp) > self.options.logResolution:
                            # log sample
                            self.flows[flowIdentifier].updateFlow(sampleCandidate)
                            if(self.options.minThroughputThreshold > 0):
                                self.flows[flowIdentifier].setIgnoreFlagByMinThroughput(self.options.minThroughputThreshold)
                            self.updateGlobalStats(sampleCandidate)
                        else:
                            # got already a sample within logRes-timespan: skip sample
                            pass
                    else:
                        # flow not yet tracked: add to list of flows
                        self.flows[flowIdentifier] = Flow(flowIdentifier, sampleCandidate.srcIp, sampleCandidate.srcPort, sampleCandidate.dstIp, sampleCandidate.dstPort, sampleCandidate)
                        if(self.options.minThroughputThreshold > 0):
                            self.flows[flowIdentifier].activateIgnoreFlag()
                        self.updateGlobalStats(sampleCandidate)
                        pass

            # wakeup several times within a logRes-timespan --> try not to miss new samples and to "flush" tcpprobe
            self.__stopped.wait(self.options.samplePollWait)
        pass

    def updateGlobalStats(self, sample):
        if(sample.absoluteTimestamp > self.timestampLastSample):
            self.timestampLastSample = sample.absoluteTimestamp
        self.numberOfLoggedSamples += 1

    def processOutput(self):
        if(self.outputBackend is None):
            return
        sampleOutputQueue = deque()
        self.outputBackend.setSampleQueue(sampleOutputQueue)
        self.outputBackend.setValuesToLog(self.options.valuesToLog)

        self.outputBackend.preLogging()

        while(not self.__stopped.wait(THREAD_STOPFLAG_WAIT)):
            for flow in self.flows:
                thisFlow = self.flows[flow]
                if(thisFlow.isActive() and not thisFlow.hasIgnoreFlag()):
                    if(self.options.fillSampleGaps or not thisFlow.getLogStatus()):
                        sampleOutputQueue.append(thisFlow.currentSample)
                        thisFlow.setLogStatus(True)

            self.outputBackend.logSample()

            if(self.options.fillSampleGaps):
                self.__stopped.wait(self.options.logResolution)

        self.outputBackend.postLogging()

    def processGui(self):
        if(self.options.guiBackend == "curses"):
            self.guiBackend.setFlows(self.flows)

        self.__stopped.wait(1) # loading...

        while(not self.__stopped.wait(THREAD_STOPFLAG_WAIT)):
            self.guiBackend.refresh()
            if(self.guiBackend.isUnloadingRequested()):
                self.initTearDown()
                self.guiBackend.tearDown()
                return

        if(self.options.guiBackend is not None):
            self.guiBackend.tearDown()

    def testAutoTimeouts(self):
        # TODO: print info about timeout-event --> IF not stdout/quiet
        while(not self.__stopped.wait(THREAD_STOPFLAG_WAIT)):
            currentTimestamp = time.time()
            if(self.options.hardTimeout > 0):
                elapsedTime = currentTimestamp - self.startTimestamp
                self.infoRegistry.save("hardTimeout_elapsedTime", elapsedTime)
                if(elapsedTime >= self.options.hardTimeout):
                    # hard-timeout reached --> exiting
                    self.initTearDown()
                    print("Hard-Timeout reached: Auto exiting.")
                    return

            elif(self.options.inActivityTimeout > 0):
                if(self.timestampLastSample > 0):
                    timeSinceLastFlowActivity = currentTimestamp - self.timestampLastSample
                else:
                    timeSinceLastFlowActivity = -1
                self.infoRegistry.save("softTimeout_timeSinceLastFlowActivity", timeSinceLastFlowActivity)
                if(timeSinceLastFlowActivity > self.options.inActivityTimeout):
                    if(self.timestampLastSample > 0):
                        # all flows inactive for at leaset "inActivityTimeout" --> exiting
                        self.initTearDown()
                        print("InActivity-Timeout reached: Auto exiting.")
                        return

            else:
                self.__stopped.wait(THREAD_TESTTIMEOUTS_WAIT)

    # def processMisc(self):
    #     while(not self.__stopped.wait(THREAD_STOPFLAG_WAIT)):
    #         # determine FQDN outside of main-threads b/c lookup can take a while
    #         if(self.options.translateIp2Hostname):
    #             for flow in self.flows:
    #                 thisFlow = self.flows[flow]
    #                 if(thisFlow.srcHostname is None):
    #                     thisFlow.srcHostname = socket.getfqdn(thisFlow.srcIp)
    #                 if(thisFlow.dstHostname is None):
    #                     thisFlow.dstHostname = socket.getfqdn(thisFlow.dstIp)
    #         self.__stopped.wait(THREAD_MISC_WAIT)

    # def determineOwnIpAdresses(self):
    #     ownIpAdresses = []
    #     for interface in netifaces.interfaces():
    #         try:
    #             ip4addr = netifaces.ifaddresses(interface)[AF_INET][0]['addr']
    #         except KeyError:
    #             pass
    #         else:
    #             if(len(ip4addr) > 0):
    #                 ownIpAdresses.append(ip4addr)
    #
    #         try:
    #             tmpIp6addr = netifaces.ifaddresses(interface)[AF_INET6][0]['addr']
    #             # returns for example:  e20::123:d9bb:feca:6353%wlp3s0
    #         except KeyError:
    #             pass
    #         else:
    #             if(len(tmpIp6addr) > 0):
    #                 if("%" in tmpIp6addr):
    #                     ip6addr, seperator, interface = tmpIp6addr.rpartition("%")
    #                     if(len(ip6addr) > 0):
    #                         ownIpAdresses.append(ip6addr)
    #                 else:
    #                     ownIpAdresses.append(tmpIp6addr)
    #     return ownIpAdresses

    def handleSignals(self, signal, frame):
        """Callback handler for signals"""
        if(not self.options.quiet and not self.options.outputBackend == 'stdout'):
            print("Exiting...")
        self.initTearDown()
        self.tearDown()
        raise SystemExit
        sys.exit(0)

    def initTearDown(self):
        self.__stopped.set()

    def tearDown(self):
        """Performs the cleanup at programm termination."""

        if(self.inputBackend is not None):
            self.inputBackend.tearDown()
        if(self.outputBackend is not None):
            self.outputBackend.tearDown()

        self.__processInputThread.join(THREAD_JOIN_TIMEOUT)
        self.__processOutputThread.join(THREAD_JOIN_TIMEOUT)
        if(self.__processGuiThread is not None):
            self.guiBackend.tearDown()
            self.__processGuiThread.join(THREAD_JOIN_TIMEOUT)
        if(self.__autoStopControlThread is not None):
            self.__autoStopControlThread.join(THREAD_JOIN_TIMEOUT)

        raise SystemExit
        sys.exit(0)
