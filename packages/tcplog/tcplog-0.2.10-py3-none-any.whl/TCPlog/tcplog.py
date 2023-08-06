#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2016,
# Karlsruhe Institute of Technology, Institute of Telematics
#
# This code is provided under the BSD 2-Clause License.
# Please refer to the LICENSE.txt file for further information.
#
# Author: Michael König
# Author: Mario Hock

import time
import datetime
import os
import sys
import subprocess
import argparse
import signal
import threading
import select
import curses
import math
import queue
from collections import deque
from ipaddress import ip_address

from .sample import Sample
from .flow import Flow
from .broadcast_log_server import BroadcastLogServer

import tcpinfo

#  format of "/proc/net/tcpprobe"
#
#  11.30814 192.168.123.42:35120 193.99.144.87:80 1472 0x259a6f5 0x259a6f5 10 2147483647 19840 36604 150784
#  ^        ^                    ^                ^    ^         ^         ^  ^          ^     ^     ^
#  |        |                    |                |    |         |         |  |          |     |     +-------- [10] RWND
#  |        |                    |                |    |         |         |  |          |     +--------------  [9] sRTT (!) µs
#  |        |                    |                |    |         |         |  |          +--------------------  [8] Send window
#  |        |                    |                |    |         |         |  +-------------------------------  [7] Slow start threshold
#  |        |                    |                |    |         |         +----------------------------------  [6] Congestion window
#  |        |                    |                |    |         +--------------------------------------------  [5] Unacknowledged sequence #
#  |        |                    |                |    +------------------------------------------------------  [4] Next send sequence #
#  |        |                    |                +-----------------------------------------------------------  [3] Bytes in packet
#  |        |                    +----------------------------------------------------------------------------  [2] Receiver address:port
#  |        +-------------------------------------------------------------------------------------------------  [1] Sender address:port
#  +----------------------------------------------------------------------------------------------------------  [0] Time seconds
TCP_PROBE_FORMAT = ['time', 'src', 'dst', 'packetSize', 'seq', 'unackSeq', 'cwnd', 'sst', 'swnd', 'rtt', 'rwnd']
TCP_INFO_FORMAT = ['state', 'src', 'dst', 'NA_packetSize', 'bytesAcked', 'NA_unackSeq', 'cwnd', 'sst', 'NA_swnd', 'rtt', 'rwnd']
# <-- parse tcpInfo-line as tcpProbe-line (w/ faked relative-timestamp)

TCP_LOG_VERSION = "0.1.0"
TCP_LOG_FORMAT_VERSION = "2"
TCP_PROBE_POLL_TIMEOUT = 0.1
DEFAULT_FILTER_PORT = 5001
PATH_TO_TCP_PROBE = "/proc/net/tcpprobe"
TCP_INFO_BINARY_NAME = "tcpinfo"
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
PATH_TO_TCP_INFO = os.path.join(SCRIPT_DIR,"tcpinfo",TCP_INFO_BINARY_NAME)
PID_FILE = "/tmp/tcplog.pid"
SERVER_ADDRESS = "0.0.0.0"
STATS_TO_PRINT = ['dTime', 'srcIp', 'srcPort', 'dstIp', 'dstPort', 'cwnd', 'sst', 'rtt', 'minRtt', 'maxRtt', 'avgRtt', 'bw', 'loss']
STATS_TO_PRINT_UNITS = ['s', 'ip', 'port', 'ip', 'port', 'packets', 'packets', 'ms', 'ms', 'ms', 'ms', 'mbit/s', '#']
VALUES_TO_LOG = ['time', 'srcIp', 'srcPort', 'dstIp', 'dstPort', 'cwnd', 'rwnd', 'sst', 'rtt', 'bw', 'loss']
VALUES_TO_LOG_UNITS = ['s', 'ip', 'port', 'ip', 'port', 'packets', 'packets', 'packets', 'ms', 'mbit/s', '#']
NUMBER_OF_DECIMAL_POINTS = 4
FLOW_CLEAR_TIMEOUT = 10 # in seconds
REFRESH_RATE_LIVE_STATS = 1 # in seconds
BANDWIDTH_SAMPLE_DELTA = 1 # in seconds

shutdownFlag = False
lock = threading.Lock()

class TcpLog:
    def init(self):
        """Initializes data structures and starts needed tasks"""

        # register signals
        signal.signal(signal.SIGINT, self.handleSignals)
        signal.signal(signal.SIGTERM, self.handleSignals)

        if(len(args.filterPorts) < 1):
            args.filterPorts.append(DEFAULT_FILTER_PORT)

        self.__start_time = None
        self.__timestampLastSample = 0
        self.__log = deque(maxlen = args.bufferLength)
        self.__flows = {}
        self.__linesProccessed = 0
        self.__matchesProccessed = 0
        self.__msgQueue = queue.Queue() # msg queue for threads
        self.__numberOfClients = 0
        self.__stopped = threading.Event()
        self.__processTcpProbeThread = threading.Thread(target=self.processTcpProbe)
        self.__printStatsThread = threading.Thread(target=self.printStats)
        self.__autologgingControlThread = threading.Thread(target=self.autologgingControl)
        self.__processTcpProbeThread.daemon = True
        self.__printStatsThread.daemon = True
        self.__autologgingControlThread.daemon = True
        self.__processTcpProbeThread.start()

        if(args.quiet != True and args.logType != "stdout"):
            self.__printStatsThread.start()
        if(args.killswitchTimeout > 0):
            self.__autologgingControlThread.start()


        self.processLogData()
        self.tearDown()



    def reading_from_regular_file(self):
        ## TODO(mario) we could optimize this by just checking this once and write the result to bool variable
        return not args.inputFile.startswith("/proc")


    # @profile
    def processTcpProbe(self):
        """Read from TCP_PROBE file and log if matches filter."""

        ## TODO(mario):
        #    for regular files, we could make a nice/informing "progress" output,
        #    rater than using the "live" curses GUI or just -q
        try:
            if(not args.useTcpInfo and not args.useNativeTcpInfo):
                self.__tcpProbeFileHandler = open(args.inputFile, 'r')

                ## Try to read a timestamp, if it's a regular file
                if ( self.reading_from_regular_file() ):
                    pos = 0
                    line = self.__tcpProbeFileHandler.readline()
                    while ( line.startswith("#") ):
                        if ( line.startswith("#TIMESTAMP: ") ):
                            self.__start_time = float(line.strip().split(" ")[1])

                        pos = self.__tcpProbeFileHandler.tell()
                        line = self.__tcpProbeFileHandler.readline()

                    ## If there is no timestamp in the file, set __start_time to False
                    #    (to distinguish the value from "not read/opened, yet")
                    if ( self.__start_time == None ):
                        self.__start_time = False

                    ## After we read the first non-header line, "put this line back" into to reading iterator
                    self.__tcpProbeFileHandler.seek(pos)
                else:
                    self.__start_time = time.time()

            ## Otherwise, remember the current time as the start time
            else:
                self.__start_time = time.time()


        except:
            print("Error: while parsing " + args.inputFile)
            sys.exit(1)
            return
        else:
            if(args.useTcpInfo):
                fakeRelativeTimestamp_start = time.time()
                lastTimestamp = 0
                while(not self.__stopped.wait(0.000001)):
                    if(time.time() - lastTimestamp < args.logResolution):
                        time.sleep(args.logResolution/1000)
                        continue;
                    lastTimestamp = time.time()
                    fakeRelativeTimestamp = time.time() - fakeRelativeTimestamp_start
                    command = PATH_TO_TCP_INFO
                    tcpInfoOutput = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
                    tcpInfoOutputAsBytes = bytes(tcpInfoOutput.communicate()[0])
                    tcpInfoOutputAsString = tcpInfoOutputAsBytes.decode('utf-8')
                    tcpInfoLines = tcpInfoOutputAsString.split("\n")
                    for line in tcpInfoLines:
                        if(line is ''):         # skip empty lines
                            continue

                        tmpLine = line.strip().split(" ")
                        if(str(tmpLine[0]) != 'ESTABLISHED'): # only parse ESTABLISHED connections
                             continue
                        tmpLine[0] = str(fakeRelativeTimestamp) # inject relative timestamp (like TcpProbe has)
                        lineToParse = " ".join(tmpLine)
                        self.processLogLine(lineToParse, TCP_PROBE_FORMAT) # to reuse processLogLine use same format as TcpProbe

            elif(args.useNativeTcpInfo):
                fakeRelativeTimestamp_start = time.time()
                lastTimestamp = 0
                while(not self.__stopped.wait(0.000001)):
                    if(time.time() - lastTimestamp < args.logResolution):
                        time.sleep(args.logResolution/1000)
                        continue;
                    lastTimestamp = time.time()
                    fakeRelativeTimestamp = time.time() - fakeRelativeTimestamp_start
                    for flowSample in tcpinfo.getTcpInfoList():
                        tmpLine = str(fakeRelativeTimestamp) # inject relative timestamp (like TcpProbe has)

                        try:
                            if(flowSample['state'] != 'ESTABLISHED'): # only parse ESTABLISHED connections
                                continue
                        except KeyError:
                                continue

                        # print(flowSample)

                        for value in TCP_PROBE_FORMAT:
                            if(value is "time"):
                                continue
                            elif(value is "src"):
                                tmpLine = tmpLine + " " + str(flowSample['srcIp']) + ":" + str(flowSample['srcPort'])
                            elif(value is "dst"):
                                tmpLine = tmpLine + " " + str(flowSample['dstIp']) + ":" + str(flowSample['dstPort'])
                            elif(value is "packetSize"):
                                tmpLine = tmpLine + " 0"
                            elif(value is "seq"):
                                tmpLine = tmpLine + " " + str(flowSample['bytes_acked'])
                            elif(value is "unackSeq"):
                                tmpLine = tmpLine + " 0"
                            elif(value is "swnd"):
                                tmpLine = tmpLine + " 0"
                            elif(value is "rwnd"):
                                tmpLine = tmpLine + " 0"
                            elif(value is "sst"):
                                tmpLine = tmpLine + " " + str(flowSample['snd_ssthresh'])
                            # elif(value is "sst"):
                            #     tmpLine = tmpLine + " " + str(flowSample['snd_ssthresh'])
                            else:
                                tmpLine = tmpLine + " "  + str(flowSample[value])

                        # print(tmpLine)

                        self.processLogLine(tmpLine, TCP_PROBE_FORMAT) # to reuse processLogLine use same format as TcpProbe


            else:
                while(not self.__stopped.wait(0.0001)):
                    inputready,outputready,exceptready = select.select([self.__tcpProbeFileHandler.fileno()],[],[], TCP_PROBE_POLL_TIMEOUT)
                    for s in inputready:
                        if(s == self.__tcpProbeFileHandler.fileno()):
                            try:
                                line = self.__tcpProbeFileHandler.readline()
                                if self.__stopped.isSet():
                                    return
                                self.processLogLine(line, TCP_PROBE_FORMAT)

                            except IOError:
                                pass


                            ## End of file is reached
                            if ( self.reading_from_regular_file() ):
                                self.__stopped.set()

    # @profile
    def processLogLine(self, line, inputFormat):
        self.__linesProccessed += 1
        processLine = False
        tmpData = line.strip().split(" ")
        data = dict(zip(inputFormat, tmpData))

        srcIp, separator, srcPort = data['src'].rpartition(':')
        assert separator
        srcPort = int(srcPort)
        srcIp = ip_address(srcIp.strip("[]"))
        src = str(srcIp) + ":" + str(srcPort)

        dstIp, separator, dstPort = data['dst'].rpartition(':')
        assert separator
        dstPort = int(dstPort)
        dstIp = ip_address(dstIp.strip("[]"))
        dst = str(dstIp) + ":" + str(dstPort)

        # srcIp:srcPort-dstIp:dstPot
        flowIdentifer = src + "-" + dst

        if(args.noFilter):
            processLine = True

        if(dstPort in args.filterPorts):
            processLine = True

        if(processLine):
            # line matches - continue processing
            self.__matchesProccessed += 1

            # update timestamp of last sample (flow independent)
            self.__timestampLastSample = time.time()

            # time since opening of tcp-probe file
            relativeTimestamp = float(data['time'])
            #timestamp = round(timestamp, NUMBER_OF_DECIMAL_POINTS)
            seq = int(data['seq'], 0)
            rtt = float(data['rtt']) / 1000 # now rtt is in ms
            #rtt = round(rtt, NUMBER_OF_DECIMAL_POINTS)

            # calculate bandwidth
            if(flowIdentifer in self.__flows):
                flow = self.__flows[flowIdentifer]

                lastTimestamp = flow.relativeTimestamp

                #   Note: Packet loss is assumed, when SSThresh is decreased (significantly)
                #     --> It was observed that TCP-Vegas repeatedly reduces SSThresh by a small amount, e.g. after Slow-Start (under some circumstances)
                new_sst = int(data['sst'])
                if ( flow.sst > new_sst + min(flow.sst*0.2, 10) ):
                    flow.loss += 1
                    loss_detected = True
                else:
                    loss_detected = False
                flow.sst = new_sst

                if(not args.useTcpInfo and not args.useNativeTcpInfo):
                    if(relativeTimestamp - lastTimestamp < args.logResolution):
                        # make an exception from the regular sampling rate, if packet loss is assumed
                        if ( not loss_detected ):
                            # FIXME: "reactivate" exception
                            return
                    else:
                        pass


                if(time.time() - flow.timestampLastBandwidthCalc >= BANDWIDTH_SAMPLE_DELTA):
                    bandwidth = (seq - flow.seqLastBandwidthCalc) if (seq - flow.seqLastBandwidthCalc) >= 0 \
                        else (int("0xffffffff",0) - flow.seqLastBandwidthCalc + seq)
                    bandwidth /= BANDWIDTH_SAMPLE_DELTA  # byte/s
                    bandwidth *= 8 / 1000 / 1000 # mbit/s
                    flow.lastBandwidth = bandwidth
                    flow.timestampLastBandwidthCalc = time.time()
                    flow.seqLastBandwidthCalc = seq
                else:
                    bandwidth = flow.lastBandwidth

            # create Flow object if not present
            else:
                flow = Flow(flowIdentifer)
                self.__flows[flowIdentifer] = flow

                flow.lastBandwidth = 0
                flow.seqLastBandwidthCalc = seq # ~ bytesAcked
                flow.timestampLastBandwidthCalc = time.time()
                flow.sst = int(data['sst'])
                flow.minRtt = rtt
                flow.maxRtt = rtt
                flow.avgRtt = rtt  ## Note: Calculate the average seems not practicable,
                #    therefore some kind strong smoothing is used. But this means the name is very misleading!!

                bandwidth = 0




            absoluteTimestamp = time.perf_counter()

            # create ne sample object and add it to queue
            sample = Sample(absoluteTimestamp)

            sample.time = relativeTimestamp
            sample.srcIp = srcIp
            sample.srcPort = srcPort
            sample.dstIp = dstIp
            sample.dstPort = dstPort
            sample.cwnd = data['cwnd']
            sample.rwnd = data['rwnd']
            sample.sst = data['sst']
            sample.rtt = rtt
            sample.bw = bandwidth
            sample.loss = flow.loss

            self.__log.append(sample)

            ## FIXME(mario):
            #   for regular files, the deque most certainly overflows regularly..
            #
            #   --> either just write the data to the output-file in this thread,
            #       or use a larger queue _and_ wait for the out output thread to empty the buffer!
            ##
            # add read data to global ouput queue

            # TODO: Reference SampleObject i/o copy values?
            # update flow-object w/ new values
            flow.seq = seq
            flow.absoluteTimestamp = absoluteTimestamp
            flow.relativeTimestamp = relativeTimestamp
            flow.srcIp = srcIp
            flow.srcPort = srcPort
            flow.dstIp = dstIp
            flow.dstPort = dstPort
            flow.cwnd = data['cwnd']
            flow.rwnd = data['rwnd']
            #flow.sst = data['sst']
            flow.rtt = rtt
            flow.bw = bandwidth
            flow.packetSize = data['packetSize']


            flow.minRtt = min(rtt, flow.minRtt)
            flow.maxRtt = max(rtt, flow.maxRtt)
            flow.avgRtt = 0.01 * rtt + 0.99 * flow.avgRtt


    def processLogData(self):
        """Macro to initialize logging to logType-destination"""
        if(args.logType == "socket"):
            self.processSocketLog()
        elif(args.logType == "file"):
            self.processFileLog()
        elif(args.logType == "stdout"):
            self.processStdLog()
        else:
            print("Logging type invalid.")
            self.tearDown()

    def processSocketLog(self):
        """Macro to start broadcast server"""
        self.__socketServer = BroadcastLogServer(SERVER_ADDRESS, args.logPort, self.__log, self.__msgQueue).listen()

    def processFileLog(self):
        """Log data to file. Creates empty file on startup"""

        lock.acquire()
        try:
            self.__logFileHandler = open(args.logFilePath, 'w')
        except:
            print("Error: while opening log file: " + args.logFilePath)
            sys.exit(1)
        else:
            # open file and clear content (if there is any)
            os.chmod(args.logFilePath, 0o644)
            self.__logFileHandler.truncate(0)

            if ( self.__start_time == False ):
                start_time = "0"
                timeAsString = "Unknown"
            else:
                start_time = str(self.__start_time)
                timeAsString = datetime.datetime.fromtimestamp(self.__start_time).strftime('%Y-%m-%d %H:%M:%S')

            # write connections-stats
            self.__logFileHandler.write("#TCPLOG\n")
            self.__logFileHandler.write("#VERSION: " + str(TCP_LOG_FORMAT_VERSION) + "\n")
            self.__logFileHandler.write("#DATE: " + timeAsString + "\n")
            self.__logFileHandler.write("#TIMESTAMP: " + start_time + "\n")
            self.__logFileHandler.write("#RESOLUTION: " + str(args.logResolution) + "s" + "\n")
            self.__logFileHandler.write("#FORMAT: " + " ".join(map(str, VALUES_TO_LOG)) +"\n")
            self.__logFileHandler.write("#UNITS: " + " ".join(map(str, VALUES_TO_LOG_UNITS)) +"\n")
            self.__logFileHandler.write("#END_HEADER\n\n")

            # write the actual logging data
            while(not self.__stopped.wait(0.0001)):
                try:
                    sampleObject = self.__log.popleft()
                except IndexError:
                    pass
                else:
                    if self.__stopped.isSet():
                        return
                    valueList = []
                    for val in VALUES_TO_LOG:
                        valueList.append(str(getattr(sampleObject, val, None)))
                    logLine = ' '.join(valueList)

                    self.__logFileHandler.write(logLine + "\n")

        lock.release()


    def printHelper(self, stringToPrint):
        """Macro for text printing. Tests for quiet-option"""
        if(args.quiet != True):
            print(stringToPrint)

    def processStdLog(self):
        """Print log data to stdout"""
        while(not self.__stopped.wait(0.0001)):
            try:
                sampleObject = self.__log.popleft()
            except IndexError:
                time.sleep(0.0001)
            else:
                valueList = []
                for val in VALUES_TO_LOG:
                    valueList.append(str(getattr(sampleObject, val, None)))
                logLine = ' '.join(valueList)
                print(logLine)
        return

    def autologgingControl(self):
        """Handles autologging timeouts"""
        while(not self.__stopped.wait(0.2)):
            currentTimestamp = time.time()
            if(self.__timestampLastSample > 0):
                if(currentTimestamp - self.__timestampLastSample > args.killswitchTimeout):
                    self.printHelper("Autologging timeout reached - exiting...")
                    self.__stopped.set()
                    return
            else:
                # no connection detected yet
                pass

    def printStats(self):
        """Macro to start printing stats within a ncurses wrapper"""
        try:
            curses.wrapper(self.printStatsHelper)
        except:
            print("Error while initializing curses - check terminal")

    def printStatsHelper(self, window):
        """Print continuously status information to stdout via curses"""
        COL_SEPARATOR = "|"
        HEAD_SEPARATOR = "="
        stdscr = curses.initscr()
        curses.savetty()
        stdscr.clear()
        curses.curs_set(False)
        stdscr.nodelay(True)
        curses.use_default_colors()
        y, x = window.getmaxyx()
        clearTerminal = False

        # TODO: clear cells or add padding to too short strings
        # TODO: cleanup, better layout?
        while(not self.__stopped.wait(0.01)):
            if self.__stopped.isSet():
                return

            try:
                if(clearTerminal):
                    time.sleep(args.refreshRateLiveStats)
                    window.clear()
                    window.refresh()
                    clearTerminal = False

                if(args.logType == "socket"):
                    try:
                        self.__numberOfClients = self.__msgQueue.get(True, 0.001)
                    except queue.Empty:
                        pass


                resize = curses.is_term_resized(y, x)
                if resize is True:
                    y, x = window.getmaxyx()
                    stdsrc.clear()
                    curses.resizeterm(y, x)
                    stdsrc.refresh()

                y, x = window.getmaxyx()
                cellWidth = math.floor(x / len(STATS_TO_PRINT))

                # print welcome
                welcomeString = ""
                welcomeString += "TCPlog " + TCP_LOG_VERSION + "\n"
                welcomeString += "==============================="

                # print general config
                configString = ""
                configString +=  "Filtering for these ports:\n"
                if(not args.noFilter):
                    for port in args.filterPorts:
                        configString += " * " + str(port) + "\n"
                else:
                    configString += " * all ports\n"
                configString +=  "\n"
                if(args.logType == "socket"):
                    configString += "Logging to socket: " + SERVER_ADDRESS + ":" + str(args.logPort)
                elif(args.logType == "file"):
                    configString += "Logging to file: " + args.logFilePath
                else:
                    pass
                configString +=  "\n"

                window.addstr(0, 0, welcomeString)
                window.addstr(3, 0, configString)

                # print application information
                applicationInfos = {
                        "Lines processed" : self.__linesProccessed,
                        "Lines filtered"  : self.__matchesProccessed,
                        "Filtered Flows"  : len(self.__flows),
                        "Log resolution"  : str(args.logResolution),
                        "Logbuffer"       : str(len(self.__log)) + "/" + str(args.bufferLength)
                    }

                if(args.logType == "socket"):
                    applicationInfos["Clients"] = str(self.__numberOfClients)

                lengthLongestString = 0
                for key, value in applicationInfos.items():
                    lengthLongestString = max(lengthLongestString, len(key))

                startYindex = 10
                for key, value in applicationInfos.items():
                    window.addstr(startYindex, 0, str(key) + ":")
                    window.addstr(startYindex, lengthLongestString + 2, str(value))
                    startYindex += 1

                # print value names
                startYindex += 1
                startXindex = 0
                for val in STATS_TO_PRINT:
                    tmpString = str(val)
                    tmpString = tmpString[:(cellWidth-1)]
                    window.addnstr(startYindex, startXindex, str(tmpString).ljust(cellWidth-1) + COL_SEPARATOR, cellWidth)
                    startXindex += cellWidth

                # print unit information
                startYindex += 1
                startXindex = 0
                for valUnit in STATS_TO_PRINT_UNITS:
                    tmpString = "[" + valUnit + "]"
                    tmpString = tmpString[:(cellWidth-1)]
                    window.addnstr(startYindex, startXindex, str(tmpString).ljust(cellWidth-1) + COL_SEPARATOR, cellWidth)
                    startXindex += cellWidth

                # print separator
                startYindex += 1
                startXindex = 0
                for valUnit in STATS_TO_PRINT_UNITS:
                    window.addnstr(startYindex, startXindex, str(HEAD_SEPARATOR * (cellWidth-1)) + COL_SEPARATOR, cellWidth)
                    startXindex += cellWidth




                # print flow information
                startYindex += 1
                startXindex = 0
                clearNow = False
                for flowKey, flowValue in self.__flows.items():
                    if(flowKey not in self.__flows):
                        break;
                    if(self.__flows[flowKey].dTime() >= FLOW_CLEAR_TIMEOUT):
                        del self.__flows[flowKey]
                        clearNow = True
                        break;


                if(clearNow):
                    window.clear()
                    window.refresh()
                    continue

                for flowKey, flowValue in self.__flows.items():
                    if(flowKey not in self.__flows):
                        break;

                    for val in STATS_TO_PRINT:
                        result = getattr(flowValue, val, None)

                        if result is not None:
                            if(val is 'dTime'):
                                valueAsString = str(format(self.__flows[flowKey].dTime(), ".4f"))
                            else:
                                valueAsString = str(result)

                            valueAsString = valueAsString.ljust(cellWidth-1)
                            if(len(valueAsString) > cellWidth-1):
                                valueAsString = valueAsString[:(cellWidth-3)] + ".."
                            window.addnstr(startYindex, startXindex, valueAsString + COL_SEPARATOR, cellWidth)
                            startXindex += cellWidth
                    startXindex = 0
                    startYindex += 1
                window.refresh()
                time.sleep(args.refreshRateLiveStats)

            except:
                clearTerminal = True
                print("Error drawing live-stats. Terminal too small?")

        return


    def handleSignals(self, signal, frame):
        """Callback handler for signals"""
        self.tearDown()
        raise SystemExit
        sys.exit(0)

    def tearDown(self):
        """Performs the cleanup at programm termination."""

        global shutdownFlag
        shutdownFlag = True
        self.__stopped.set()

        self.__processTcpProbeThread.join(1.5)
        if(args.quiet != True and args.logType != "stdout"):
            self.__printStatsThread.join(1.5)
        if(args.killswitchTimeout > 0):
            self.__autologgingControlThread.join(1.5)

        self.printHelper("\n")
        self.printHelper("Shutting down...")
        if(args.logType == "socket"):
            self.printHelper("Closing socket...")
            # Sockets gets closed by signal
        elif(args.logType == "file"):
            self.printHelper("Closing log file...")
            self.__logFileHandler.close()

        self.printHelper("All done... Goodbye cruel world!")
        sys.exit(0)

    def getLog(self):
        return self.__log

def main():
    #parse args
    parser = argparse.ArgumentParser()

    parser.add_argument(
            "-d",
            "--debug", help="Debug",
            action="store_true",
            dest="debug",
            default=False)
    parser.add_argument(
            "-q",
            "--quiet", help="Whether to ouput anything at all (false)",
            action="store_true",
            dest="quiet",
            default=False)
    parser.add_argument(
            "-a",
            "--notall", help="Filter flows by port (false)",
            action="store_false",
            dest="noFilter",
            default=True)
    parser.add_argument(
            "-t",
            "--type", help="Log to socket / file / stdout (socket)",
            dest="logType",
            default="socket")
    parser.add_argument(
            "-f",
            "--filepath",
            help="Path where the log file is stored (/tmp/tcplog)",
            dest="logFilePath",
            default="/tmp/tcplog")
    parser.add_argument(
            "--log-port",
            help="Port number for socket-logging (11337)",
            dest="logPort",
            type=int,
            default=11337)
    parser.add_argument(
            "-b",
            "--buffer-length",
            help="Buffer length (5000)",
            dest="bufferLength",
            type=int,
            default=5000)
    parser.add_argument(
            "-r",
            "--resolution",
            help="Log resolution (in seconds, default: 0.1)",
            dest="logResolution",
            type=float,
            default=0.1)
    parser.add_argument(
            "-i",
            "--input",
            help="Path to TCP-Probe proc-file, or actual file in the same format (default: " + PATH_TO_TCP_PROBE + ")",
            dest="inputFile",
            default=PATH_TO_TCP_PROBE)

    parser.add_argument(
            "-z",
            "--tcpinfo", help="Whether to use TcpInfo as (only!) source or not (false)",
            action="store_true",
            dest="useTcpInfo",
            default=False)

    parser.add_argument(
            "-y",
            "--nativetcpinfo", help="Whether to use native TcpInfo as (only!) source or not (false)",
            action="store_true",
            dest="useNativeTcpInfo",
            default=False)

    parser.add_argument(
            "-v",
            "--version", help="Print version information",
            action="store_true",
            dest="showVersion",
            default=False)
    parser.add_argument(
            "-l",
            "--refresh-rate-live-stats",
            help="Live stats refresh rate (in seconds, default: " + str(REFRESH_RATE_LIVE_STATS) + ")",
            dest="refreshRateLiveStats",
            type=float,
            default=REFRESH_RATE_LIVE_STATS)

    # Filter
    parser.add_argument(
            "-p",
            "--port",
            help="Filter by destination port. Multiple occurrences possible (5001)",
            dest="filterPorts",
            action='append',
            type=int,
            default=[])

    parser.add_argument(
            "-k",
            "--kill-timeout",
            help="Auto-logging timeout (in seconds, default: 0)",
            dest="killswitchTimeout",
            type=int,
            default=0)

    args = parser.parse_args()

    # test for root-permissions
    if (os.getuid() == 0):
        print("Error: Please do not run this program with root-privileges. Exiting...")
        sys.exit(1)

    if (args.showVersion):
        print("TCPlog version: " + TCP_LOG_VERSION + " (format version: " + TCP_LOG_FORMAT_VERSION + ")")
        sys.exit(0)

    PID = str(os.getpid())
    if(os.path.isfile(PID_FILE)):
        print("Error: %s already exists. Exiting..." % PID_FILE)
        sys.exit(1)

    # test if tcp_probe/input-file is readable
    if(not args.useTcpInfo and not args.useNativeTcpInfo):
        readable = os.access(args.inputFile, os.R_OK)
        if(not readable):
            print("\n\n")
            print("=======================================================================")
            print("Error: TCP-Probe file '" + args.inputFile + "' not readable. Exiting...")

            # only print this help if necessary
            if(args.inputFile == PATH_TO_TCP_PROBE):
                print("Kernel module loaded? Permissions set? Try:\n")
                print("sudo modprobe tcp_probe full=1 port=0 &&\n   \\sudo chmod 444 /proc/net/tcpprobe")

            print("=======================================================================")
            sys.exit(1)

    # test if TcpInfo binary is there and executable
    if(args.useTcpInfo):
        if(not os.path.isfile(PATH_TO_TCP_INFO)):
            print("Error: TcpInfo binary not found. Exiting...")
            sys.exit(1)
        if(not os.access(PATH_TO_TCP_INFO, os.X_OK)):
            print("Error: TcpInfo binary found but not executable. Exiting...")
            sys.exit(1)

    if(args.useNativeTcpInfo):
        try:
           import tcpinfo
           tcpinfo.getTcpInfoList()
        except:
            print("Error: tcpinfo module not found. Exiting...")
            sys.exit(1)

    # test if another process is already using the input-file
    if(not args.useTcpInfo and not args.useNativeTcpInfo):
        # count stdout of lsof and do some dirty casting...
        command = "lsof -t " + args.inputFile + "|wc -l"
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
        numberOfProcsAsString = bytes(process.communicate()[0]).decode('utf-8')
        numberOfProcs = int(numberOfProcsAsString)
        if(numberOfProcs > 0):
            print("Error: Input file already in use by another process. Exiting...")
            sys.exit(1)


    # if we made it to this point: No startup errors detected...

    # write pid-file
    pidFileHandler = open(PID_FILE, "w")
    pidFileHandler.write(PID)

    try:
        TcpLog().init()     # <-- starts the main programme
    finally:
        # clean up (remove pid-file) and exit
        os.unlink(PID_FILE)
        sys.exit(0)


if __name__ == "__main__":
    args = None
    stdsrc = None
    main()
