# -*- coding: utf-8 -*-

# Copyright (c) 2016,
# Karlsruhe Institute of Technology, Institute of Telematics
#
# This code is provided under the BSD 2-Clause License.
# Please refer to the LICENSE.txt file for further information.
#
# Author: Michael König
# Author: Mario Hock

class Sample(object):
    """Data structure ro represent a single log sample object"""

    def __init__(self, timestamp):
        """Initializes a new sample object"""

        # timestamp is real unix-timestamp (seconds since 1970-01-01)
        self.timestamp = timestamp

