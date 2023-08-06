# -*- coding: utf-8 -*-

import sys
import time

from ...utils.utilty import Utility
from .input_base import InputBase
from ...sample import Sample

class TcpInfoInput(InputBase):
    def __init__(self, options, infoRegistry):
        self.options = options
        self.infoRegistry = infoRegistry
        self.__loggedSampleCounter = 0
        self.startTimestamp = time.time()
        self.shutdown = False

    def startupCheck(self):
        try:
           import tcpinfo
           tcpinfo.getListOfAvailableValues()
        except:
            Utility.eprint(\
                "Error: tcpinfo module not found. Exiting..."\
                "\n\n"\
                "Please install the tcpinfo module\n"
                "OR use \"tcpprobe\" as input-backend instead"\
            )
            sys.exit(1)
        else:
            self.tcpinfo = tcpinfo


    def startUp(self):
        self.tcpinfo.startUp()
        self.availableValues = self.tcpinfo.getListOfAvailableValues()

    def tearDown(self):
        self.shutdown = True
        self.tcpinfo.tearDown()
        pass

    def retrieveNewSamples(self):
        newSamples = []

        if(self.shutdown):
            return newSamples
        else:
            for flowSample in self.tcpinfo.getTcpInfoList():
                try:
                    if(flowSample['state'] != 'ESTABLISHED'): # only parse ESTABLISHED connections
                        continue
                except KeyError:
                        continue
                else:
                    dstPort = int(flowSample['dstPort'])
                    srcPort = int(flowSample['srcPort'])
                    log = False

                    if(self.options.filterWhiteListing):
                        log = False
                        if((srcPort in self.options.filterSrcPorts) or (dstPort in self.options.filterDstPorts)):
                            log = True

                    else: # blacklisting
                        log = True
                        if(srcPort in self.options.filterSrcPorts or dstPort in self.options.filterDstPorts):
                            log = False



                    if(log):
                        relativeTimestamp = time.time() - self.startTimestamp
                        sample = Sample(flowSample['srcIp'], flowSample['srcPort'], flowSample['dstIp'], flowSample['dstPort'])
                        sample.relativeTimestamp = relativeTimestamp

                        for value in self.availableValues:
                            if(value == "bytes_acked"):
                                sample.seq = flowSample['bytes_acked']
                            elif(value == "snd_ssthresh"):
                                sample.sst = flowSample['snd_ssthresh']
                            elif(value == "rtt"):
                                sample.rtt = float(flowSample['rtt']) / 1000
                            elif(value == "rcv_rtt"):
                                sample.rcv_rtt = float(flowSample['rcv_rtt']) / 1000
                            elif(value == "rttvar"):
                                sample.rttvar = float(flowSample['rttvar']) / 1000
                            else:
                                try:
                                    setattr(sample, value, flowSample[value])
                                except KeyError:
                                    pass

                        newSamples.append(sample)

                    else:
                        # skip sample
                        pass

            return newSamples
