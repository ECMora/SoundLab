# -*- coding: utf-8 -*-
from .TimeParameter import TimeParameter


class EndTimeParameter(TimeParameter):
    """
    Class that measure the end time parameter on a segment
    """

    def __init__(self, decimal_places=4):
        TimeParameter.__init__(self, decimal_places=decimal_places)
        self.name = "End(s)"

    def measure(self, segment):
        return round(segment.indexTo * 1.0 / segment.signal.samplingRate, self.decimal_places)