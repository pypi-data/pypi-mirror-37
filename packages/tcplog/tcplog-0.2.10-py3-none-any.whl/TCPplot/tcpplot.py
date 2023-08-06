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

import signal
import argparse
import time
import threading
import socket
import select
import sys
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
from collections import deque
from ipaddress import ip_address
import numpy as np

# Constants
DEFAULT_SOCKETSERVER_PORT = 11337
DEFAULT_SOCKETSERVER_LOCATION = 'localhost:' + str(DEFAULT_SOCKETSERVER_PORT)
DEFAULT_LINES_TO_SHOW = ['cwnd']
DEFAULT_FILTER_PORT = 5001
LOGSERVER_CONNECT_RETRY_TIME = 3 #in s
CLEAR_GAP = 0.2 # gap in s
INFINITY_THRESHOLD = 1e8
VALUES_TO_PLOT = ['cwnd', 'sst', 'rtt', 'bw'] # (only values for Y-axis)
#VALUES_TO_PLOT = ['cwnd', 'sst', 'rtt', 'bw', 'loss'] # (only values for Y-axis)
# VALUES_TO_PLOT_ON_SECOND_AXIS = ['rtt']
VALUES_TO_PROCESS = ['time']  + VALUES_TO_PLOT #helper to init all data structures

# Strings
FIGURE_TITLE = "TCPplot"
PLOT_TITLE = "Data from"
PAUSE = "Pause"
QUIT = "Quit"


#  TODO: update format-example
#  format of "/tmp/tcplog" resp. socket-data
#
#  14.910653454 46.163.76.98 9999 35 29312 25 39626 10.750693667388724 10.599101599959623
#  ^            ^            ^    ^  ^     ^  ^     ^                  ^
#  |            |            |    |  |     |  |     |                  |
#  |            |            |    |  |     |  |     |                  +------- [8] Bandwidth II (mbit/s)
#  |            |            |    |  |     |  |     +-------------------------- [7] Bandwidth (mbit/s)
#  |            |            |    |  |     |  +-------------------------------- [6] sRTT ms
#  |            |            |    |  |     +----------------------------------- [5] SlowStart-Threshold
#  |            |            |    |  +----------------------------------------- [4] RWND
#  |            |            |    +-------------------------------------------- [3] CWND
#  |            |            +------------------------------------------------- [2] Receiver Port
#  |            +-------------------------------------------------------------- [1] Receiver IP
#  +--------------------------------------------------------------------------- [0] Time seconds
LOG_FORMAT = ['time', 'srcIp', 'srcPort', 'dstIp', 'dstPort', 'cwnd', 'rwnd', 'sst', 'rtt', 'bw', 'loss']
#at least time & dstPort required
NUMBER_OF_VALUES = len(LOG_FORMAT)

class TcpPlot:
    def init(self):
        # register signals
        signal.signal(signal.SIGINT, self.handleSignals)
        signal.signal(signal.SIGTERM, self.handleSignals)
        self.__stopped = threading.Event()

        # initialize vars
        self.__incomeBuffer = deque(maxlen=args.bufferLength)
        self.__tmpBuffer = deque(maxlen=args.bufferLength)
        self.__connectionBuffer = {}
        self.__tmpTimestamp = 0

        if(len(args.filterPorts) < 1):
            args.filterPorts.append(DEFAULT_FILTER_PORT)
        for i in args.filterPorts:
            self.__connectionBuffer[i] = deque(maxlen=args.bufferLength)

        if(args.logFilePath):
            self.__logType = "file"
        else:
            self.__logType = "socket"

        if(len(args.linesToShow) < 1):
            args.linesToShow.extend(DEFAULT_LINES_TO_SHOW)

        # init tasks and run them
        self.__retrieveDataThread = threading.Thread(target=self.retrieveLogData)
        self.__retrieveDataThread.daemon = True
        self.__retrieveDataThread.start()
        self.plotGraph()

    def retrieveLogData(self):
        """Macro to initialize data retrieval and processing from various sources."""
        self.__filterRetrievedLogData= threading.Thread(target=self.filterRetrievedLogData)
        self.__filterRetrievedLogData.start()
        if(self.__logType == "socket"):
            self.retrieveLogDataFromSocket()
        else:
            self.retrieveLogDataFromFile()

    def retrieveLogDataFromSocket(self):
        """Reads data (in blocks) from a socket and adds the received data to an income buffer."""
        self.__processSocketLogData = threading.Thread(target=self.processSocketLogData)
        self.__processSocketLogData.start()

        ip, separator, port = args.logServer.rpartition(':')
        if(':' not in args.logServer or port is ''):
            logServerPort = DEFAULT_SOCKETSERVER_PORT
            logServerIp = ip_address(socket.gethostbyname(args.logServer.strip("[]")))
        else:
            logServerPort = int(port)
            logServerIp = ip_address(socket.gethostbyname(ip.strip("[]")))
        dst = str(logServerIp) + ":" + str(logServerPort)

        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print("Failed to create socket")

        while(not self.__stopped.wait(0.00001)):
            try:
                self.__socket.connect((str(logServerIp), logServerPort))
                print("Successfully connected to " + dst + "")
            except socket.error:
                print("Error: Could not connect to " + dst + " Retrying in " + str(LOGSERVER_CONNECT_RETRY_TIME) + "s ...")
                time.sleep(LOGSERVER_CONNECT_RETRY_TIME)
            else:
                break

        while(not self.__stopped.wait(0.00001)):
            try:
                data = self.__socket.recv(4096)
            except socket.timeout:
                print("Connection timeout.")
                self.__socket.close()
                return
            except IOError:
                print("Error: Could not retrieve data from " + dst)
                self.__socket.close()
                return
            else:
                if(len(data) == 0):
                    print("Connection closed by foreign host.")
                    self.__socket.close()
                    break;
                self.__incomeBuffer.append(data)


    def retrieveLogDataFromFile(self):
        """Reads data from log file and adds the data to the temporary queue."""

        try:
            self.__logFileHandler = open(args.logFilePath, 'r')
        except IOError:
            print ("Error: while parsing " + args.logFilePath)
            SystemExit
            return
        else:
            inputready,outputready,exceptready = select.select([self.__logFileHandler.fileno()],[],[])
            while(not self.__stopped.wait(0.00001)):
                if self.__stopped.isSet():
                    return
                else:
                    for s in inputready:
                        if(s == self.__logFileHandler.fileno()):
                            for line in self.__logFileHandler:
                                if self.__stopped.isSet():
                                    return

                                #ignore comments
                                if not line.startswith("#"):
                                    line = line.strip()
                                    self.__tmpBuffer.append(line,)

    def tailFile(self, fileHandler):
        """Helper function to read continuously from a growing file."""
        fileHandler.seek(0,2)
        while True:
            line = fileHandler.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line

    def processSocketLogData(self):
        """Reads data from the income buffer and tries to reassemble splitted data."""
        tmpBuffer = ""
        while(True):
            try:
                line = self.__incomeBuffer.popleft()
                line = line.decode("UTF-8")
                lines = line.split("\n")
            except IndexError:
                time.sleep(0.00001)
            else:
                for i in lines:
                    data = i.split(" ")
                    if(tmpBuffer != ""):
                        tmpBuffer += i
                        self.__tmpBuffer.append(tmpBuffer)
                        tmpBuffer = ""
                        continue

                    if(len(data) < NUMBER_OF_VALUES):
                        tmpBuffer += i
                    else:
                        self.__tmpBuffer.append(i)

    def filterRetrievedLogData(self):
        """Filters retrieved data by selected port. Drops malformed data."""
        lastTimestamp = 0
        while(True):
            try:
                line = self.__tmpBuffer.popleft()
            except IndexError:
                time.sleep(0.00001)
            else:
                tmpData = line.split(" ")
                if(len(tmpData) is NUMBER_OF_VALUES):
                    data = dict(zip(LOG_FORMAT, tmpData))
                else:
                    continue

                try:
                    timestamp = float(data['time'])
                    port = int(data['dstPort'])
                except ValueError:
                    continue
                else:
                    if(port not in args.filterPorts):
                        continue

                filteredData = {}
                try:
                    for val in VALUES_TO_PROCESS:
                        filteredData[val] = float(data[val])
                except ValueError:
                    continue
                else:
                    timestampDelta = lastTimestamp - timestamp
                    if(timestampDelta > args.plotResolution):
                        lastTimestamp = timestamp
                        continue
                    self.__connectionBuffer[port].append(filteredData)
                    lastTimestamp = timestamp


    def pause(self, event):
        """Toggles pause flag."""
        self.__paused ^= True
        return

    def toggleVisibility(self, lineID):
        """Toggles visibility for given line."""
        for port in args.filterPorts:
            self.__plotLineConfigs[port][lineID] ^= True
            self.__plotLines[port][lineID].set_visible(self.__plotLineConfigs[port][lineID])
        self.drawPlotLegend()

    def drawPlotLegend(self):
        """(Re)draws legend with visible lines."""
        labelObjs  = []
        labelTexts = []
        for port in args.filterPorts:
            for val in VALUES_TO_PLOT:
                if(self.__plotLineConfigs[port][val]):
                    labelObjs.append(self.__plotLines[port][val])
                    labelTexts.append(self.__plotLines[port][val].get_label())
        if(len(labelObjs) > 0):
            self.__ax.legend(labelObjs, labelTexts, fontsize='small')
        else:
            self.__ax.legend_.remove()

    def plotKeyPressCallback(self, event):
        """Callback to handle key presses."""
        if(args.debug):
            print("Key pressed: '" + event.key + "'")

        # p pauses
        if(event.key == "p"):
            self.pause(event)
        # ctrl+{c,q,w} quits programm
        elif(event.key == "ctrl+c" or event.key == "ctrl+w" or event.key == "ctrl+q"):
            raise SystemExit
        else:
            try:
                index = int(event.key)
            except ValueError:
                pass
            else:
                # Numbers 1-N toggle visibility of lines
                if index in range(1, len(VALUES_TO_PLOT)+1):
                    self.toggleVisibility(VALUES_TO_PLOT[(index-1)])

    def stopPlotting(self, event):
        """Callback function to stop plotting and the programm."""
        self.__tmpTimestamp = time.perf_counter()
        plt.close()
        self.tearDown()

    def plotGraph(self):
        """Initializes plot configuration and starts the plotting."""
        self.__paused = False
        self.__minVal = 9999999999
        self.__maxVal = 0


        fig = plt.figure(FIGURE_TITLE)
        fig.canvas.mpl_connect('key_press_event', self.plotKeyPressCallback)
        self.__ax = plt.axes()
        self.__ax.set_autoscaley_on(False)
        self.__ax.set_xlim(0, args.xDelta)
        self.__ax.set_title(PLOT_TITLE + " :" + ', :'.join(map(str, args.filterPorts)))

        self.__plotLines = {}
        self.__plotValues = {}
        self.__plotLineConfigs = {}
        for port in args.filterPorts:
            self.__plotLines[port] = {}
            self.__plotValues[port] = {}
            self.__plotLineConfigs[port] = {}
            self.__plotLineConfigs[port]['lastTimestamp'] = 0
            for val in VALUES_TO_PROCESS:
                self.__plotValues[port][val] = deque(maxlen=(int(args.xDelta / args.plotResolution * 10)))
            index = 1
            for val in VALUES_TO_PLOT:
                self.__plotLines[port][val], = self.__ax.plot([])
                self.__plotLines[port][val].set_label("[" + str(index) + "] " + val + " - " + str(port) + "")
                self.__plotLineConfigs[port][val] = True
                self.__plotLines[port][val].set_visible(True)
                index += 1
        self.drawPlotLegend()

        # pause button
        pauseAx = plt.axes([0.8, 0.025, 0.1, 0.04])
        pauseButton = Button(pauseAx, PAUSE)
        pauseButton.on_clicked(self.pause)

        # quit button
        quitAx = plt.axes([0.125, 0.025, 0.1, 0.04])
        quitButton = Button(quitAx, QUIT)
        quitButton.on_clicked(self.stopPlotting)

        if(args.preloadBuffer > 0):
            self.__preloading = True
        else:
            self.__preloading = False

        self.__lastPlotTimestamp = {}
        for port in args.filterPorts:
            self.__lastPlotTimestamp[port] = 0
        self.__lastDrawTimestamp = 0
        self.__initRealtimeTimestamp = 0
        self.__initSampletimeTimestamp = -1

        self.__timeOffset = 0
        self.__bufferFactor = 1
        self.__apsFixFactor = 1

        # call update-routine
        animation.FuncAnimation(fig, self.plotGraphUpdate, init_func=self.plotInit,
                               frames=args.drawFps, interval=args.drawIntervall, blit=args.blitting, repeat=True)
        if self.__stopped.isSet():
            return
        else:
            plt.show()

    def returnAllLines(self):
        """Macro to return all lines as they are."""
        allPlotLines = []
        for port in args.filterPorts:
            for val in VALUES_TO_PLOT:
                allPlotLines.append(self.__plotLines[port][val])
        return tuple(allPlotLines)

    def returnNanSample(self, time):
        """Macro to return NaN-Samples (to fill plot)."""
        data = {}
        data['time'] = time - args.plotResolution
        for val in VALUES_TO_PLOT:
            data[val] = np.nan
        return data

    def plotGraphUpdate(self, i):
        """Animation loop - does the actual plot update."""
        if(self.__initSampletimeTimestamp == -1):
            self.__initSampletimeTimestamp = 0
            return self.returnAllLines()
        elif(self.__initSampletimeTimestamp == 0):
            self.calculateSampleTimeOffset()
            return self.returnAllLines()

        # fill playback-buffer
        if(self.__preloading):
            bufferLength = -1
            for port in args.filterPorts:
                bufferLength = max(bufferLength, len(self.__connectionBuffer[port]))

            if(bufferLength > 0):
                bufferedTime = bufferLength * args.plotResolution
                bufferTarget = args.preloadBuffer * self.__bufferFactor
                if(bufferedTime >= bufferTarget):
                    self.__preloading = False
                    # reduce buffer-target to half size after initial buffering
                    self.__bufferFactor = 0.5
                    print("Buffer filled.")
            if(self.__preloading):
                print("Buffering... " + str(format(bufferedTime, ".2f")) + "/" + str(format(bufferTarget, ".2f")))
                return self.returnAllLines()

        if(self.__paused == True):
            return self.returnAllLines()
        else:
            while(True):
                currentTimestamp = time.perf_counter()
                if(self.__initRealtimeTimestamp == 0):
                    self.__initRealtimeTimestamp = currentTimestamp
                timestampDelta = (currentTimestamp - self.__lastDrawTimestamp) * args.playbackSpeed * self.__apsFixFactor

                currentXmin, currentXmax = self.__ax.get_xlim()
                currentYmin, currentYmax = self.__ax.get_ylim()
                newXmax = currentTimestamp - args.preloadBuffer
                newXmin = newXmax - args.xDelta
                self.__ax.set_xlim(newXmin, newXmax)

                maxYval = 0
                minYval = 9999999
                connectionsData = {}

                # skip this cycle, plot resolution not yet reached
                if(timestampDelta < args.plotResolution):
                    return self.returnAllLines()

                for port in args.filterPorts:
                    connectionsData[port] = deque()
                    whileRun = True
                    while(len(self.__connectionBuffer[port]) > 0 and whileRun):
                        try:
                            data = self.__connectionBuffer[port].popleft()
                        except IndexError:
                            whileRun = False
                            pass
                        else:
                            lineTime = self.__initRealtimeTimestamp  + (data['time'] - self.__initSampletimeTimestamp)
                            # time in past
                            if(lineTime < newXmin):
                                continue
                            # time older than newst timestamp
                            elif(lineTime < self.__lastPlotTimestamp[port]):
                                continue
                            # skip this sample due plot plotResolution
                            elif((lineTime - self.__lastPlotTimestamp[port]) < args.plotResolution):
                                continue
                            else:
                                if(self.__lastPlotTimestamp[port] > 0 and ((lineTime - self.__lastPlotTimestamp[port]) > CLEAR_GAP)):
                                    self.__lastPlotTimestamp[port] = lineTime
                                    nanSample = self.returnNanSample(lineTime)
                                    connectionsData[port].append(nanSample)
                                infinityReached = False
                                for val in VALUES_TO_PLOT:
                                    if(data[val] > INFINITY_THRESHOLD):
                                        data[val] = np.nan
                                        # nanSample = self.returnNanSample(lineTime)
                                        # connectionsData[port].append(nanSample)
                                        # infinityReached = True

                                if(not infinityReached):
                                    self.__lastPlotTimestamp[port] = lineTime
                                    connectionsData[port].append(data)

                data = 0
                for port in connectionsData:
                    if(len(connectionsData[port]) > 0):
                        data += 1

                for port in args.filterPorts:
                    if(data < 1 and currentTimestamp > self.__lastPlotTimestamp[port] ):
                        if(args.debug):
                            print("No data for any connection.")
                        if(args.interimBuffering):
                            self.__preloading = True
                        return self.returnAllLines()



                for connection in connectionsData:
                    while(len(connectionsData[connection]) > 0):
                        data = connectionsData[connection].popleft()

                        lineTime = self.__initRealtimeTimestamp  + (data['time'] - self.__initSampletimeTimestamp)
                        self.__plotLineConfigs[connection]['lastTimestamp'] = data['time']

                        for val in VALUES_TO_PROCESS:
                            if(val == 'time'):
                                self.__plotValues[connection][val].append(lineTime)
                            else:
                                self.__plotValues[connection][val].append(data[val])

                    for val in VALUES_TO_PLOT:
                        self.__plotLines[connection][val].set_data(self.__plotValues[connection]['time'], self.__plotValues[connection][val])


                for port in args.filterPorts:
                    for val in VALUES_TO_PLOT:
                        if(self.__plotLineConfigs[port][val]):
                            if(len(self.__plotValues[port][val]) > 0):
                                maxYval = max(maxYval, max(self.__plotValues[port][val]))
                                minYval = min(minYval, min(self.__plotValues[port][val]))

                if(maxYval > 0):
                    newYmin = minYval - 50
                    newYmin = max(newYmin, 0)
                    newYmax = maxYval * 2
                    self.__ax.set_ylim(newYmin, newYmax)

                self.__lastDrawTimestamp = time.perf_counter()
                return self.returnAllLines()

    def plotInit(self):
        """Helper to initialize plot."""
        for port in args.filterPorts:
            for val in VALUES_TO_PLOT:
                self.__plotLines[port][val].set_data([], [])

                # hide "invisible" lines
                if(val not in args.linesToShow):
                    self.__plotLineConfigs[port][val] = False
                    self.__plotLines[port][val].set_visible(False)



        newXmin = 0
        newXmax = newXmin + args.xDelta
        self.__ax.set_xlim(newXmin, newXmax)

        if(args.debug):
            print("Plot init done.")

        return self.returnAllLines()

    def calculateSampleTimeOffset(self):
        """Calculate SampleTime difference at start"""
        for port in args.filterPorts:
            try:
                data = self.__connectionBuffer[port].popleft()
            except IndexError:
                pass
            else:
                #re-add first sample (to head of dequeue)
                self.__connectionBuffer[port].appendleft(data)
                self.__initSampletimeTimestamp = float(data['time'])
                return

    def handleSignals(self, signal, frame):
        """Callback function to handle signals."""
        self.tearDown()
        raise SystemExit

    def tearDown(self):
        """Performs the cleanup at programm termination."""
        self.__stopped.set()
        if(self.__logType == "socket"):
            self.__socket.close()
        else:
            self.__logFileHandler.close()
        raise SystemExit
        sys.exit

def main():
    #pars args
    parser = argparse.ArgumentParser()

    parser.add_argument(
            "-d",
            "--debug", help="Debug mode - ignores \"-q\"",
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
            "-b",
            "--buffer", help="Length of preload buffer (in seconds, default: 1, 0 to deactivate preload buffer)",
            type=float,
            dest="preloadBuffer",
            default=1)

    parser.add_argument(
            "-ib",
            "--interimbuffer", help="Activate interim buffering.",
            action="store_true",
            dest="interimBuffering",
            default=False)

    parser.add_argument(
            "-ps",
            "--playback-speed", help="Playback speed (factor, default: 1)",
            type=float,
            dest="playbackSpeed",
            default=1)
    parser.add_argument(
            "-aps",
            "--adaptive-playback-speed", help="Enable adaptive playback speed (default: false)",
            action="store_true",
            dest="adaptivePlaybackSpeed",
            default=False)

    parser.add_argument(
            "--buffer-size", help="Number of elements to buffer from socket per filter (5000)",
            dest="bufferLength",
            default=5000)


    parser.add_argument(
            "-z",
            "--blit", help="Deactivate blitting",
            action="store_false",
            dest="blitting",
            default=True)

    logTypeGroup = parser.add_mutually_exclusive_group()

    logTypeGroup.add_argument(
            "-s",
            "--server",
            help="IP and Port of socket-logging server (" + DEFAULT_SOCKETSERVER_LOCATION + ")",
            dest="logServer",
            default=DEFAULT_SOCKETSERVER_LOCATION)
    logTypeGroup.add_argument(
            "-f",
            "--filepath",
            help="Path where the log file is stored",
            type=str,
            dest="logFilePath")

    parser.add_argument(
            "-df",
            help="Number of FPS to draw",
            dest="drawFps",
            type=int,
            default=60)
    parser.add_argument(
            "-di",
            help="Draw intervall",
            dest="drawIntervall",
            type=int,
            default=30)

    parser.add_argument(
            "-x",
            help="Seconds to plot (20)",
            dest="xDelta",
            type=int,
            default=20)
    parser.add_argument(
            "-r",
            "--resolution",
            help="Plot resolution (in seconds, default: 0.001)",
            dest="plotResolution",
            type=float,
            default=0.01)

    # Filter
    parser.add_argument(
            "-p",
            "--port",
            help="Filter by port. Multiple occurrences possible (" + str(DEFAULT_FILTER_PORT) + ")",
            dest="filterPorts",
            action='append',
            type=int,
            default=[])
    parser.add_argument(
            "-l",
            "--line",
            help="Plot lines to show initially. Multiple occurrences possible. Possible values: " + ', '.join(VALUES_TO_PLOT),
            dest="linesToShow",
            action='append',
            default=[])


    args = parser.parse_args()
    lock = threading.Lock()

    TcpPlot().init()

if __name__ == "__main__":
    args = None
    main()
