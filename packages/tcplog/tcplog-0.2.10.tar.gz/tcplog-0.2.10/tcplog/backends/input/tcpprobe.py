# -*- coding: utf-8 -*-

#  format of "/proc/net/tcpprobe"
#
#  11.30814 192.168.123.42:35120 192.168.123.99:80 1472 0x259a6f5 0x259a6f5 10 2147483647 19840 36604 150784
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

import sys
import os
import select
import subprocess
from ipaddress import ip_address

from ...utils.utilty import Utility
from .input_base import InputBase
from ...sample import Sample

PATH_TO_TCP_PROBE = "/proc/net/tcpprobe"
TCP_PROBE_FORMAT = ['time', 'src', 'dst', 'packetSize', 'seq', 'unackSeq', 'cwnd', 'sst', 'swnd', 'rtt', 'rwnd']
TCP_PROBE_POLL_TIMEOUT = 0.01

class TcpProbeInput(InputBase):
    def __init__(self, options, infoRegistry):
        self.options = options
        self.infoRegistry = infoRegistry
        self.__linesProccessed = 0
        self.__matchedLinesProccessed = 0
        self.closed = False

    def startupCheck(self):
        readable = os.access(PATH_TO_TCP_PROBE, os.R_OK)
        if(not readable):
            Utility.eprint(\
                "Error: TCP-Probe file \"" + PATH_TO_TCP_PROBE + "\" not readable. Exiting..."\
                "\n\n"\
                "Kernel module loaded? Permissions set? Try:\n"\
                "sudo modprobe tcp_probe full=1 port=0 && sudo chmod 444 /proc/net/tcpprobe"\
                "\n\n"\
                "OR use \"tcpinfo\" as input-backend instead"\
                )
            sys.exit(1)

        # count stdout of lsof and do some dirty casting...
        command = "lsof -t " + PATH_TO_TCP_PROBE + "|wc -l"
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
        numberOfProcsAsString = bytes(process.communicate()[0]).decode('utf-8')
        numberOfProcs = int(numberOfProcsAsString)
        if(numberOfProcs > 0):
            Utility.eprint("Error: Input file already in use by another process. Exiting...")
            sys.exit(1)

    def startUp(self):
        self.__tcpProbeFileHandler = open(PATH_TO_TCP_PROBE, "r")

    def tearDown(self):
        self.closed = True
        self.__tcpProbeFileHandler.close()

    def retrieveNewSamples(self):
        newSamples = []
        if(self.closed):
            return newSamples

        inputReady,outputReady,exceptReady = select.select([self.__tcpProbeFileHandler.fileno()], [], [], TCP_PROBE_POLL_TIMEOUT)
        if(inputReady):
            for s in inputReady:
                if(self.closed):
                    return newSamples
                elif(s == self.__tcpProbeFileHandler.fileno()):
                    try:
                        line = self.__tcpProbeFileHandler.readline()
                        proccessSample = self.processLogLine(line)
                        newSamples.append(proccessSample)

                    except IOError:
                        pass

                    else:
                        return newSamples
        return newSamples

    def processLogLine(self, line):
        self.__linesProccessed += 1
        self.__matchedLinesProccessed += 1
        log = False
        tmpData = line.strip().split(" ")
        data = dict(zip(TCP_PROBE_FORMAT, tmpData))

        srcIp, separator, srcPort = data['src'].rpartition(':')
        assert separator
        srcPort = int(srcPort)
        srcIp = ip_address(srcIp.strip("[]"))

        dstIp, separator, dstPort = data['dst'].rpartition(':')
        assert separator
        dstPort = int(dstPort)
        dstIp = ip_address(dstIp.strip("[]"))

        if(self.options.filterWhiteListing):
            log = False
            if((srcPort in self.options.filterSrcPorts) or (dstPort in self.options.filterDstPorts)):
                log = True

        else: # blacklisting
            log = True
            if(srcPort in self.options.filterSrcPorts or dstPort in self.options.filterDstPorts):
                log = False


        # line matches - continue processing
        if(log):
            self.__matchedLinesProccessed += 1

            # time since opening of tcp-probe file
            relativeTimestamp = float(data['time'])
            rtt = float(data['rtt']) / 1000 # now rtt is in ms
            seq = int(data['seq'], 0)

            # create ne sample object and return it
            sample = Sample(srcIp, srcPort, dstIp, dstPort)
            sample.relativeTimestamp = relativeTimestamp
            sample.cwnd = int(data['cwnd'])
            sample.rwnd = int(data['rwnd'])
            sample.sst = int(data['sst'])
            sample.seq = seq
            sample.rtt = rtt

            return sample
        else:
            return None
