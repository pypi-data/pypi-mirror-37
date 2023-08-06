# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import math

class Utility:
    @staticmethod
    def eprint(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

    @staticmethod
    def truncate(number, digits) -> float:
        stepper = pow(10.0, digits)
        return math.trunc(stepper * number) / stepper
