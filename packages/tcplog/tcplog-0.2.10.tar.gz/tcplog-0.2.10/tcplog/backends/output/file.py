# -*- coding: utf-8 -*-

import sys
import os
import datetime

from ...utils.utilty import Utility
from .output_base import OutputBase

TCP_LOG_FORMAT_VERSION = "2"

# TODO: get global info from tcplog

class FileOutput(OutputBase):
    def __init__(self, options, infoRegistry):
        self.options = options
        self.infoRegistry = infoRegistry
        self.startTime = self.infoRegistry.load('startTime')
        self.__loggedSampleCounter = 0
        self.__logFileHandler = None

    def setSampleQueue(self, sampleQueue):
        self.sampleQueue = sampleQueue

    def setValuesToLog(self, valuesToLog):
        self.valuesToLog = valuesToLog

    def startUp(self):
        try:
            self.__logFileHandler = open(self.options.logFilePath, 'w')
        except:
            Utility.eprint("Error: while opening log file: " + self.options.logFilePath)
            sys.exit(1)

    def startupCheck(self):
        pass

    def tearDown(self):
        self.__logFileHandler.close()
        pass

    def preLogging(self):
        # open file and clear content (if there is any)
        os.chmod(self.options.logFilePath, 0o644)
        self.__logFileHandler.truncate(0)

        startTime = str(self.startTime)
        timeAsString = datetime.datetime.fromtimestamp(self.startTime).strftime('%Y-%m-%d %H:%M:%S')

        # write connections-stats
        self.__logFileHandler.write("#TCPLOG\n")
        self.__logFileHandler.write("#VERSION: " + str(self.infoRegistry.load("logFormatVersion")) + "\n")
        self.__logFileHandler.write("#DATE: " + timeAsString + "\n")
        self.__logFileHandler.write("#TIMESTAMP: " + startTime + "\n")
        self.__logFileHandler.write("#RESOLUTION: " + str(self.options.logResolution) + "s" + "\n")
        self.__logFileHandler.write("#FORMAT: " + " ".join(map(str, self.options.valuesToLog)) +"\n")
        # self.__logFileHandler.write("#UNITS: " + " ".join(map(str, VALUES_TO_LOG_UNITS)) +"\n")
        self.__logFileHandler.write("#END_HEADER\n\n")



        # logLine = "###" + ' '.join(self.valuesToLog)
        #print(logLine)
        pass

    def logSample(self):
        try:
            sampleObject = self.sampleQueue.popleft()
        except IndexError:
            pass
        else:
            valueList = []
            for val in self.valuesToLog:
                valueList.append(str(getattr(sampleObject, val, "_")))
            logLine = ' '.join(valueList)
            self.__logFileHandler.write(logLine + "\n")
            self.__loggedSampleCounter = self.__loggedSampleCounter + 1
        pass

    def postLogging(self):
        self.__logFileHandler.close()
        #print("### samples logged: " + str(self.__loggedSampleCounter))
        pass
