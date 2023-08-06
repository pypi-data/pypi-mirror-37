# -*- coding: utf-8 -*-

from .output_base import OutputBase

class StdoutOutput(OutputBase):
    def __init__(self, options, infoRegistry):
        self.options = options
        self.infoRegistry = infoRegistry
        self.__loggedSampleCounter = 0

    def setSampleQueue(self, sampleQueue):
        self.sampleQueue = sampleQueue

    def setValuesToLog(self, valuesToLog):
        self.valuesToLog = valuesToLog

    def tearDown(self):
        pass

    def startUp(self):
        pass

    def startupCheck(self):
        pass

    def preLogging(self):
        logLine = "###" + ' '.join(self.valuesToLog)
        print(logLine)

    def logSample(self):
        """Print log data to stdout"""
        try:
            sampleObject = self.sampleQueue.popleft()
        except IndexError:
            pass
        else:
            valueList = []
            for val in self.valuesToLog:
                valueList.append(str(getattr(sampleObject, val, "_")))
            logLine = ' '.join(valueList)
            print(logLine)
            self.__loggedSampleCounter = self.__loggedSampleCounter + 1

    def postLogging(self):
        print("### samples logged: " + str(self.__loggedSampleCounter))
