#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Convenience wrapper for running TCPlog directly from source tree."""

import sys
sys.settrace

from tcplog.main import main

if __name__ == '__main__':
    main()
