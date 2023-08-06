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

class Flow(object):
    """Data structure to represent a filtered flow"""

    def __init__(self, name):
        """Initializes new flow"""

        self.name = name
        self.loss = 0
        self.sst = 0
        self.absoluteTimestamp = 0

    def dTime(self):
        return (time.perf_counter() - self.absoluteTimestamp)

