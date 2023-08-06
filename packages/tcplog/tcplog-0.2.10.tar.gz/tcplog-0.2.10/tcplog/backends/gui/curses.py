# -*- coding: utf-8 -*-

# TODO: cleaner?
STATS_TO_PRINT = ['#', 'activity', 'elapsed', 'srcIp', 'srcPort', 'dstIp', 'dstPort', 'cwnd', 'sst', 'rtt', 'minRtt', 'maxRtt', 'avgRtt', 'smoothedRtt', 'smoothedThroughput', 'assumedLosses']
STATS_TO_PRINT_TITLES = ['#', 'activity', 'elapsed', 'locIp', 'loc. port', 'remote IP', 'rem. port', 'cwnd', 'sst', 'rtt', 'minRtt', 'maxRtt', 'avgRtt', 'smoothRtt', 'throughput', 'losses']
STATS_TO_PRINT_UNITS = [' ', 's', 's', 'ip', 'port', 'ip', 'port', 'pkt', 'pkt', 'ms', 'ms', 'ms', 'ms', 'ms', 'mbit/s', '#']
# STATS_TO_PRINT_UNITS_TYPE = ['time', 'time', 'str', 'str', 'str', 'str', 'count', 'count', 'time', 'time', 'time', 'time', 'time', 'transferSpeed', 'count']
# STATS_TO_PRINT_TITLES = [...... avgRtt, smoothedRtt, bw, aLosses]

import curses
import math
import time

from ...utils.utilty import Utility
from .gui_base import GuiBase

NUMBER_OF_DECIMALS = 2
MAX_INT_32 = 2147483647 # initial sst value...
MIN_TERM_WIDTH = 68
MIN_TERM_HEIGHT = 10
VERTICAL_SEPARATOR = " "
HORIZONTAL_SEPARATOR = "_"
COLORS_ENABLED = True
KEYCODE_ESC = 27
REFRESH_RATE_STEP = 0.5
MIN_REFRESH_RATE = 0.5
SCROLL_STEP_X = 5
SCROLL_STEP_Y = 1
SCROLL_STEP_Y_LARGE = 10 # PageUp/Down
KEYSTROKE_COOLDOWN = 0.100 # ms until next keystroke is processed
FLOW_VALUE_CELL_WIDTH = 11
INNER_PAD_SUB = 4 # 2 rows for header and 2 rows for footer

class CursesGui(GuiBase):
    def __init__(self, options, infoRegistry):
        self.options = options
        self.infoRegistry = infoRegistry
        self.window = None
        self.unloading = False
        self.outerPadHeight = 0
        self.outerPadWidth = 1000
        self.innerPadHeight = 0
        self.innerPadWidth = 1000
        self.timestampOfLastRedraw = 0
        self.timestrampOfLastKeystroke = 0
        self.innerPadPosCoordinates = 4, 0  # absolute position of pad
        self.innerPadStartCoordinates = 0, 0 # relative position of scroll-box
        self.outerPadPosCoordinates = 2, 0  # absolute position of pad
        self.outerPadStartCoordinates = 0, 0 # relative position of scroll-box

    def setFlows(self, flows):
        self.flows = flows

    def startupCheck(self):
        pass

    def startUp(self):
        self.window = curses.initscr()
        self.window.clear()
        self.window.nodelay(True)
        self.window.keypad(True)
        curses.savetty()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(False)
        curses.start_color()
        curses.use_default_colors()

        if(COLORS_ENABLED):
            curses.init_pair(1, curses.COLOR_MAGENTA, -1)
            curses.init_pair(2, curses.COLOR_BLUE, -1)
            curses.init_pair(3, curses.COLOR_GREEN, -1)
            curses.init_pair(4, curses.COLOR_YELLOW, -1)
            curses.init_pair(5, curses.COLOR_CYAN, -1)
            curses.init_pair(6, curses.COLOR_WHITE, -1)
            curses.init_pair(7, curses.COLOR_RED, -1)
            curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        else:
            curses.init_pair(1, -1, -1)
            curses.init_pair(2, -1, -1)
            curses.init_pair(3, -1, -1)
            curses.init_pair(4, -1, -1)
            curses.init_pair(5, -1, -1)
            curses.init_pair(6, -1, -1)
            curses.init_pair(7, -1, -1)
            curses.init_pair(8, -1, -1)

        self.clearTerminal = True

        try:
            self.window.addstr(3, 3, "loading...", curses.A_BOLD)
            self.window.refresh()
            self.y, self.x = self.window.getmaxyx()
        except:
            print("Display Error! (Check terminal-size)")

    def isUnloadingRequested(self):
        return self.unloading

    def initTearDown(self):
        self.window.clear()
        self.window.addstr(3, 3, "unloading...", curses.A_BOLD)
        self.window.refresh()
        time.sleep(1)
        self.tearDown()
        self.unloading = True

    def tearDown(self):
        curses.nocbreak()
        curses.echo()
        curses.curs_set(True)
        self.window.keypad(False)
        curses.endwin()

    def processInput(self):
        self.processKeyInput()

    def processKeyInput(self):
        pressedkey = self.window.getch()
        if(pressedkey > 0):
            if(time.time() - self.timestrampOfLastKeystroke <= KEYSTROKE_COOLDOWN):
                curses.flushinp()
                return
            else:
                self.timestrampOfLastKeystroke = time.time()

                if(pressedkey == ord('q') or pressedkey == KEYCODE_ESC): # q or ESC
                    self.initTearDown()
                    return
                elif(pressedkey == curses.KEY_LEFT):
                    y,x = self.outerPadStartCoordinates
                    x -= SCROLL_STEP_X
                    x = max(0, x)
                    self.outerPadStartCoordinates = y, x

                    y,x = self.innerPadStartCoordinates
                    x -= SCROLL_STEP_X
                    x = max(0, x)
                    self.innerPadStartCoordinates = y, x
                    try:
                        self.outerPad.refresh(*self.outerPadStartCoordinates, *self.outerPadPosCoordinates, self.y-3, self.x-1)
                        self.innerPad.refresh(*self.innerPadStartCoordinates, *self.innerPadPosCoordinates, self.y-3, self.x-1)
                    except Exception as e:
                        pass
                elif(pressedkey == curses.KEY_RIGHT):
                    y,x = self.outerPadStartCoordinates
                    x += SCROLL_STEP_X
                    x = min(self.x, x)
                    self.outerPadStartCoordinates = y, x

                    y,x = self.innerPadStartCoordinates
                    x += SCROLL_STEP_X
                    x = min(self.x, x)
                    self.innerPadStartCoordinates = y, x
                    try:
                        self.outerPad.refresh(*self.outerPadStartCoordinates, *self.outerPadPosCoordinates, self.y-3, self.x-1)
                        self.innerPad.refresh(*self.innerPadStartCoordinates, *self.innerPadPosCoordinates, self.y-3, self.x-1)
                    except Exception as e:
                        pass
                elif(pressedkey == curses.KEY_UP or pressedkey == curses.KEY_PPAGE):
                    y,x = self.innerPadStartCoordinates
                    if(pressedkey == curses.KEY_UP):
                        y -= SCROLL_STEP_Y
                    elif(pressedkey == curses.KEY_PPAGE):
                        y -= SCROLL_STEP_Y_LARGE
                    y = max(0, y)
                    self.innerPadStartCoordinates = y, x
                    try:
                        self.innerPad.refresh(*self.innerPadStartCoordinates, *self.innerPadPosCoordinates, self.y-4, self.x-1)
                    except Exception as e:
                        pass
                elif(pressedkey == curses.KEY_DOWN or pressedkey == curses.KEY_NPAGE):
                    if((len(self.flows) + 2) > (self.y - INNER_PAD_SUB )):
                        y,x = self.innerPadStartCoordinates
                        if(pressedkey == curses.KEY_DOWN):
                            y += SCROLL_STEP_Y
                        elif(pressedkey == curses.KEY_NPAGE):
                            y += SCROLL_STEP_Y_LARGE
                        y = min(self.innerPadHeight - INNER_PAD_SUB, y)
                        try:
                            self.innerPadStartCoordinates = y, x
                            self.innerPad.refresh(*self.innerPadStartCoordinates, *self.innerPadPosCoordinates, self.y-4, self.x-1)
                        except Exception as e:
                            pass
                elif(pressedkey == ord('+')):
                    self.options.refreshRateLiveStats += REFRESH_RATE_STEP
                elif(pressedkey == ord('-')):
                    tmpValue = self.options.refreshRateLiveStats
                    tmpValue -= REFRESH_RATE_STEP
                    self.options.refreshRateLiveStats = max(MIN_REFRESH_RATE, tmpValue)

                self.repaint()



    def refresh(self):
        self.processInput()
        if(time.time() - self.timestampOfLastRedraw >= self.options.refreshRateLiveStats):
            self.timestampOfLastRedraw = time.time()
            self.repaint()
        else:
            time.sleep(0.1)

    def repaint(self):
        resize = curses.is_term_resized(self.y, self.x)
        if(resize is True):
            if(self.options.debug):
                self.window.addstr(3, 3, "Info: Terminal was resized.")
            self.y, self.x = self.window.getmaxyx()
            self.window.clear()
            curses.resizeterm(self.y, self.x)
            self.window.refresh()
            return

        if(self.x < MIN_TERM_WIDTH):
            self.window.clear()
            self.window.addstr(3, 3, "Error: Terminal too narrow.")
            self.window.refresh()
            self.clearTerminal = True
            return

        if(self.y < MIN_TERM_HEIGHT):
            self.window.clear()
            self.window.addstr(3, 3, "Error: Terminal too small.")
            self.window.refresh()
            self.clearTerminal = True
            return


        if(self.clearTerminal):
            self.window.clear()
            self.window.refresh()
            self.clearTerminal = False

        INFO_GRID_CELLS = 4
        INFO_GRID_CELL_WIDTH = math.floor((self.x-2) / INFO_GRID_CELLS)
        INFO_GRID_CELL_STARTS = {}
        for x in range(0, (INFO_GRID_CELLS)):
            INFO_GRID_CELL_STARTS[x] = (x * INFO_GRID_CELL_WIDTH) + 1

        try:

            # header area
            timeNow = time.strftime("%H:%M:%S")
            headerPos = 0 # + 1 @ border
            headerTexts = {}
            headerTexts[0] = 'TCPlog: ' + self.infoRegistry.load("version")
            headerTexts[1] = 'Time: {}'.format(timeNow)
            headerTexts[2] = 'Input: ' + self.options.inputBackend
            headerTexts[3] = 'Output: ' + self.options.outputBackend
            self.window.addnstr(headerPos, INFO_GRID_CELL_STARTS[0], headerTexts[0].ljust(INFO_GRID_CELL_WIDTH), INFO_GRID_CELL_WIDTH, curses.A_BOLD)
            self.window.addnstr(headerPos, INFO_GRID_CELL_STARTS[1], headerTexts[1].center(INFO_GRID_CELL_WIDTH), INFO_GRID_CELL_WIDTH, curses.A_BOLD)
            self.window.addnstr(headerPos, INFO_GRID_CELL_STARTS[2], headerTexts[2].center(INFO_GRID_CELL_WIDTH), INFO_GRID_CELL_WIDTH, curses.A_BOLD)
            self.window.addnstr(headerPos, INFO_GRID_CELL_STARTS[3], headerTexts[3].rjust(INFO_GRID_CELL_WIDTH), INFO_GRID_CELL_WIDTH, curses.A_BOLD)

            # footer area
            footerPos = self.y - 1 # -2 @ border

            # TODO: count active flows, count long-living, count all
            numberOfFlows = len(self.flows)
            numberOfActiveFlows = 0
            for flow in self.flows:
                if(self.flows[flow].isActive()):
                    numberOfActiveFlows += 1

            timeoutCellAttr = curses.A_BOLD
            hardTimeout = "N/A"
            if(self.options.hardTimeout > 0):
                elapsedTime = self.infoRegistry.load("hardTimeout_elapsedTime")
                hardTimeout = str(round(elapsedTime, 1))
                hardTimeout += "/"
                hardTimeout += str(self.options.hardTimeout) + "s"

                if(self.options.hardTimeout - elapsedTime <= 10):
                    timeoutCellAttr |= curses.A_BLINK

            softTimeout = "N/A"
            if(self.options.inActivityTimeout > 0):
                timeSinceLastFlowActivity = self.infoRegistry.load("softTimeout_timeSinceLastFlowActivity")
                softTimeout = str(round(timeSinceLastFlowActivity, 1))
                softTimeout += "/"
                softTimeout += str(self.options.inActivityTimeout) + "s"

                if(self.options.inActivityTimeout * 0.6 <= timeSinceLastFlowActivity):
                    timeoutCellAttr |= curses.A_BLINK

            footerTexts = {}
            footerTexts[0] = 'Interval: {}s'.format(round(self.options.refreshRateLiveStats, 1))
            footerTexts[1] = 'Log-Res: {}s'.format(self.options.logResolution)
            footerTexts[2] = 'Flows: ' + str(numberOfActiveFlows) + " (" + str(numberOfFlows) + ")"
            footerTexts[3] = 'ST: ' + str(softTimeout) + ' | HT: ' + str(hardTimeout)
            self.window.addnstr(footerPos, INFO_GRID_CELL_STARTS[0], footerTexts[0].ljust(INFO_GRID_CELL_WIDTH), INFO_GRID_CELL_WIDTH, curses.A_BOLD)
            self.window.addnstr(footerPos, INFO_GRID_CELL_STARTS[1], footerTexts[1].center(INFO_GRID_CELL_WIDTH), INFO_GRID_CELL_WIDTH, curses.A_BOLD)
            self.window.addnstr(footerPos, INFO_GRID_CELL_STARTS[2], footerTexts[2].center(INFO_GRID_CELL_WIDTH), INFO_GRID_CELL_WIDTH, curses.A_BOLD)
            self.window.addnstr(footerPos, INFO_GRID_CELL_STARTS[3], footerTexts[3].rjust(INFO_GRID_CELL_WIDTH), INFO_GRID_CELL_WIDTH, timeoutCellAttr)

            cellWidth = FLOW_VALUE_CELL_WIDTH
            normalCellWidth = cellWidth

            # TODO:
            # * print config before flow-info
            # * filter options
            # * inputFile, outputFile, logSocketPort
            # * stats --> samples processed, samples logged...
            # * numberOfSocket-clients
            # print value names

            # y-fixed content: header of flow-table --> only scrollable in x-direction
            self.outerPadHeight = 2 # header
            self.outerPad = curses.newpad(self.outerPadHeight, self.outerPadWidth)
            self.outerPad.scrollok(1)
            self.outerPad.idlok(1)
            # self.outerPad.bkgd("+")

            # print units
            startYindex = 1
            startXindex = 0
            i = 0
            for val in STATS_TO_PRINT_UNITS:
                cellWidth = normalCellWidth
                if(i is 0):
                    cellWidth = 5
                elif(i is 1):
                    cellWidth = 7
                elif(i is 2):
                    cellWidth = 5
                elif(i is 3):
                    i += 1
                    continue
                elif(i is 5):
                    cellWidth = 16
                tmpString = str(val)
                tmpString = tmpString[:(cellWidth-1)]
                self.outerPad.addnstr(startYindex, startXindex, str(tmpString).ljust(cellWidth), cellWidth, curses.A_BOLD | curses.color_pair(8))
                startXindex += cellWidth
                i += 1

            # print cell titles
            startYindex = 0
            startXindex = 0
            i = 0
            for val in STATS_TO_PRINT_TITLES:
                cellWidth = normalCellWidth
                if(i is 0):
                    cellWidth = 5
                elif(i is 1):
                    cellWidth = 7
                elif(i is 2):
                    cellWidth = 5
                elif(i is 3):
                    i += 1
                    continue
                elif(i is 5):
                    cellWidth = 16

                tmpString = str(val)
                tmpString = tmpString[:(cellWidth-1)]
                self.outerPad.addnstr(startYindex, startXindex, str(tmpString).ljust(cellWidth), cellWidth, curses.A_BOLD)
                startXindex += cellWidth
                i += 1



            self.innerPadHeight = len(self.flows)
            self.innerPadHeight = max(self.innerPadHeight, (self.y - INNER_PAD_SUB))
            self.innerPad = curses.newpad(self.innerPadHeight, self.innerPadWidth) # contains flows
            self.innerPad.scrollok(1)
            self.innerPad.idlok(1)
            # self.innerPad.bkgd("*")

            startYindex = 0
            startXindex = 0
            i = 0

            for flowKey, flowValue in self.flows.items():
                if(flowKey not in self.flows):
                    break;

                if(not self.options.showEphemeralFlows and self.flows[flowKey].isEphemeral()):
                    continue

                cellStyle = curses.color_pair(3)
                if(not self.flows[flowKey].isActive()):
                    cellStyle = curses.color_pair(4)

                for val in STATS_TO_PRINT:
                    cellWidth = normalCellWidth

                    if(val is '#'):
                        valueAsString = str(i)
                        cellWidth = 5

                    elif(val is 'activity'):
                        if(self.flows[flowKey].isActive()):
                            valueAsString = str(round(self.flows[flowKey].timeSinceLastActivity(), 2))
                        else:
                            valueAsString = "inact."
                        cellWidth = 7

                    elif(val is 'elapsed'):
                        valueAsString = str(int(round(self.flows[flowKey].totalActiveTime(), 0)))
                        cellWidth = 5

                    elif(val is 'srcIp'):
                        continue
                        if(self.flows[flowKey].srcHostname is None):
                            valueAsString = str(self.flows[flowKey].srcIp)
                        else:
                            valueAsString = str(self.flows[flowKey].srcHostname)

                    elif(val is 'dstIp'):
                        cellWidth = 16
                        if(self.flows[flowKey].dstHostname is None):
                            valueAsString = str(self.flows[flowKey].dstIp)
                        else:
                            valueAsString = str(self.flows[flowKey].dstHostname)


                    else:
                        valueAsString = "#"
                        sample = None
                        result = None
                        sample = self.flows[flowKey].currentSample
                        if(sample is not None):
                            result = getattr(sample, val, None)
                            if result is not None:
                                # maybe float?
                                if("." in str(result)):
                                    try:
                                        floatResult = float(result)
                                    except ValueError:
                                        # nope no float...
                                        valueAsString = str(result)
                                    else:
                                        valueAsString = str(Utility.truncate(floatResult, NUMBER_OF_DECIMALS))

                                # maybe int?
                                else:
                                    try:
                                        intResult = int(result)
                                    except ValueError:
                                        # nope no int...
                                        valueAsString = str(result)
                                    else:
                                        if(intResult == MAX_INT_32):
                                            valueAsString = "+INF"
                                        else:
                                            valueAsString = str(intResult)


                    valueAsString = valueAsString.ljust(cellWidth-1)
                    if(len(valueAsString) > cellWidth-1):
                        valueAsString = valueAsString[:(cellWidth-3)] + ".."

                    self.innerPad.addnstr(startYindex, startXindex, valueAsString, cellWidth, cellStyle)
                    startXindex += cellWidth
                startXindex = 0
                startYindex += 1
                i += 1

            self.outerPad.refresh(*self.outerPadStartCoordinates, *self.outerPadPosCoordinates, self.y-3, self.x-1)
            self.innerPad.refresh(*self.innerPadStartCoordinates, *self.innerPadPosCoordinates, self.y-3, self.x-1)
            self.window.refresh()

        except Exception as e:
            print(str(e))
            self.clearTerminal = True
            print("Error drawing live-stats. Terminal small?")

        return
