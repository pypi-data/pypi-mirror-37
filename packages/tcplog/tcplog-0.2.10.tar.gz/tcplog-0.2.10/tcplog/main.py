#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import signal
import time

from .utils.utilty import Utility
from .tcplog import TcpLog
from .info_registry import InfoRegistry

# constants
TCP_LOG_VERSION = "0.2.10"
TCP_LOG_FORMAT_VERSION = "2"

# default values
DEFAULT_INPUT_BACKEND = "tcpinfo"
DEFAULT_OUTPUT_BACKEND = "none"
DEFAULT_REFRESH_RATE_LIVE_STATS = 1 # in seconds
DEFAULT_LOG_RESOLUTION = 0.1 # in seconds
DEFAULT_SOCKET_PORT = 11337
DEFAULT_LOGFILE_PATH = "/tmp/tcplog.log"
DEFAULT_VALUES_TO_LOG = ['absoluteTimestamp', 'relativeTimestamp', 'srcIp', 'srcPort', 'dstIp', 'dstPort', 'cwnd', 'sst', 'rtt', 'minRtt', 'maxRtt', 'avgRtt', 'meanRtt', 'throughput', 'smoothedThroughput', 'assumedLosses']


# main prog
def main():
    inputBackend = None
    outputBackend = None
    guiBackend = None

    infoRegistry = InfoRegistry()
    options = parse_options()

    infoRegistry.save("startTime", time.time())
    infoRegistry.save("version", TCP_LOG_VERSION)
    infoRegistry.save("logFormatVersion", TCP_LOG_FORMAT_VERSION)

    if(options.showVersion):
        print("TCPlog: " + TCP_LOG_VERSION)
        print("Log format: " + TCP_LOG_FORMAT_VERSION)
        sys.exit(0)

    if(options.showGuiHelp):
        printGuiHelp()
        sys.exit(0)

    # init input backend
    if(options.inputBackend == "tcpinfo"):
        from .backends.input.tcpinfo import TcpInfoInput
        inputBackend = TcpInfoInput(options, infoRegistry)
        options.samplePollWait = options.logResolution / 10 # read often
    elif(options.inputBackend == "tcpprobe"):
        from .backends.input.tcpprobe import TcpProbeInput
        inputBackend = TcpProbeInput(options, infoRegistry)
        options.samplePollWait = options.logResolution / 1000 # try to read fast enough to flush tcpprobe
    # elif(options.inputBackend == "file"):
    #     from .backends.input.file import FileInput
    #     inputBackend = FileInput(options, info)
    #     options.samplePollWait = 0 # read file as fast as possible

    # init output backend
    if(options.outputBackend == "socket"):
        from .backends.output.socket import SocketOutput
        outputBackend = SocketOutput(options, infoRegistry)
    elif(options.outputBackend == "file"):
        from .backends.output.file import FileOutput
        outputBackend = FileOutput(options, infoRegistry)
    elif(options.outputBackend == "stdout"):
        from .backends.output.stdout import StdoutOutput
        outputBackend = StdoutOutput(options, infoRegistry)
    elif(options.outputBackend == "none"):
        pass

    # init gui backend
    if(options.guiBackend == "curses"):
        from .backends.gui.curses import CursesGui
        guiBackend = CursesGui(options, infoRegistry)
    # elif(options.guiBackend == "progress"):
    #     from .backends.gui.progress import ProgressGui
    #     guiBackend = ProgressGui(options, info)
    elif(options.guiBackend == None):
        guiBackend = None

    if(inputBackend is None):
        Utility.eprint("No valid input backend selected. Exiting...")
        sys.exit(1)

    if(inputBackend is not None):
        inputBackend.startupCheck()
        inputBackend.startUp()

    if(outputBackend is not None):
        outputBackend.startupCheck()
        outputBackend.startUp()

    if(guiBackend is not None):
        guiBackend.startupCheck()
        guiBackend.startUp()

    try:
        tcpLog = TcpLog(inputBackend, outputBackend, guiBackend, options, infoRegistry)
        signal.signal(signal.SIGINT, tcpLog.handleSignals)
        signal.signal(signal.SIGTERM, tcpLog.handleSignals)
        tcpLog.run()
        # ^-- starts the main programme
    except Exception as e:
        Utility.eprint(str(e))
        raise e
        sys.exit(1)
    finally:
        if(not options.quiet and not options.outputBackend == "stdout"):
            print("Goodbye cruel world!")
        sys.exit(0)


def parse_options():
    parser = argparse.ArgumentParser()

    # TODO:
    # * more filter options
    # * whitelisting
    # * blacklisting

    # parser.add_argument(
    #         "-a",
    #         "--notall", help="Filter flows by port (false)",
    #         action="store_false",
    #         dest="noFilter",
    #         default=True)

    # TODO: read from config file
    # parser.add_argument(
    #         "-c",
    #         "--config",
    #         help="Load configuration from file (default: None)",
    #         dest="configFile",
    #         default=None)

    parser.add_argument(
            "-r",
            "--log-resolution",
            help="Log resolution (in seconds, default: " + str(DEFAULT_LOG_RESOLUTION) + ")",
            dest="logResolution",
            type=float,
            default=DEFAULT_LOG_RESOLUTION)

    parser.add_argument(
            "-i",
            "--input-backend",
            help="Available input backends: \"tcpprobe\" and \"tcpinfo\" (default: " + DEFAULT_INPUT_BACKEND + ")",
            dest="inputBackend",
            default=DEFAULT_INPUT_BACKEND)

    parser.add_argument(
            "-o",
            "--output-backend",
            help="Available output backends: \"stdout\", \"file\", \"socket\" and \"none\" (default: " + DEFAULT_OUTPUT_BACKEND + ") ",
            dest="outputBackend",
            default=DEFAULT_OUTPUT_BACKEND)

    parser.add_argument(
            "-w",
            "--writeto",
            help="Path where the log file is stored - only usable with \"file\" output backend (default: " + DEFAULT_LOGFILE_PATH + ")",
            dest="logFilePath",
            default=DEFAULT_LOGFILE_PATH)

    parser.add_argument(
            "--log-port",
            help="Port number for socket-logging - only usable with \"socket\" output backend (default: " + str(DEFAULT_SOCKET_PORT) + ")",
            dest="logPort",
            type=int,
            default=DEFAULT_SOCKET_PORT)

    parser.add_argument(
            "--inactivity-timeout",
            help="SoftTimeout: Automatically stops logging if no flow activity is detected for n seconds (in seconds, default: 0 = disabled)",
            dest="inActivityTimeout",
            type=int,
            default=0)

    parser.add_argument(
            "--hard-timeout",
            help="Automatically stops logging after n seconds (in seconds, default: 0 = disabled)",
            dest="hardTimeout",
            type=int,
            default=0)


    parser.add_argument(
            "--values-to-log",
            help="List of value-names to log (default: [" + ", ".join(DEFAULT_VALUES_TO_LOG) + "])",
            dest="valuesToLog",
            action='append',
            type=str,
            default=DEFAULT_VALUES_TO_LOG)

    parser.add_argument(
            "-f",
            "--fill-sample-gaps",
            help="Log all (active) flows even if no new sample was recorded - forces rewrites of previous values (default: false)",
            action="store_true",
            dest="fillSampleGaps",
            default=False)

    guiOptGroup = parser.add_argument_group('gui')
    guiOptGroup.add_argument(
            "--refresh-rate-live-stats",
            help="Live stats refresh rate (in seconds, default: " + str(DEFAULT_REFRESH_RATE_LIVE_STATS) + ")",
            dest="refreshRateLiveStats",
            type=float,
            default=DEFAULT_REFRESH_RATE_LIVE_STATS)

    guiOptGroup.add_argument(
            "--show-ephemeral-flows",
            help="Show ephemeral/short-living flows (default: false)",
            dest="showEphemeralFlows",
            action="store_true",
            default=False)

    # guiOptGroup.add_argument(
    #         "--ip2host",
    #         help="Tries to lookup hostname by IP address (default: false)",
    #         dest="translateIp2Hostname",
    #         action="store_true",
    #         default=False)

    guiOptGroup.add_argument(
            "--gui-help",
            help="Show keybinds and information about the GUI.",
            dest="showGuiHelp",
            action="store_true",
            default=False)

    # Filter
    filterOptGroup = parser.add_argument_group('filter')
    filterOptGroup.add_argument(
            "--filter-dst-port",
            help="Filter by destination port. Multiple occurrences possible",
            dest="filterDstPorts",
            action='append',
            type=int,
            default=[])

    filterOptGroup.add_argument(
            "--filter-src-port",
            help="Filter by source port. Multiple occurrences possible",
            dest="filterSrcPorts",
            action='append',
            type=int,
            default=[])

    filterOptGroup.add_argument(
            "--whitelisting",
            help="Enable whitelisting (default: false = blacklisting)",
            dest="filterWhiteListing",
            action='store_true',
            default=False)

    stripOptGroup = parser.add_argument_group('strip')
    stripOptGroup.add_argument(
            "-m",
            "--min-throughput",
            help="Strip logging-output of  flows with a throughput below given threshold (in Mbit/s, default: 0.0 = no filter)",
            dest="minThroughputThreshold",
            type=float,
            default=0.0)

    # misc options
    parser.add_argument(
            "-q",
            "--quiet", help="Whether to ouput anything at all (default: false)",
            action="store_true",
            dest="quiet",
            default=False)

    parser.add_argument(
            "--debug",
            help="Debug mode (default: false)",
            action="store_true",
            dest="debug",
            default=False)

    parser.add_argument(
            "--version",
            help="Print version information",
            action="store_true",
            dest="showVersion",
            default=False)

    options = parser.parse_args()

    if(options.outputBackend == "stdout"):
        options.guiBackend = None
        # highest priority --> in case of StdoutOutput no gui at all
    elif(options.inputBackend == "file"):
        # if reading from regular file --> use progressGui
        options.guiBackend = "progress"
    else:
        if(options.quiet):
            options.guiBackend = None
        else:
            options.guiBackend = "curses"

    return options

def printGuiHelp():
    print("\
Available keybinds:\n\
    'q':            quit TCPlog \n\
    '+':            increase time between gui refreshes \n\
    '-':            decrease time between gui refreshes \n\
    'arrow_right':  scroll flow table to the right\n\
    'arrow_left':   scroll flow table to the left\n\
    'arrow_top':    scroll flow table upwards\n\
    'arrow_down':   scroll flow table downwards\n\
    'page_up':      scroll flow table upwards (fast)\n\
    'page_down':    scroll flow table downwards (fast)\n\
"
)
    # TODO: print info about GUI-elements (abbrevations and so on...)

if __name__ == "__main__":
    main()
