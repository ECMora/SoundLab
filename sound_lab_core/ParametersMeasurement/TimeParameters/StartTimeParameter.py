# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.TimeParameters.TimeParameter import TimeParameter


class StartTimeParameter(TimeParameter):
    """
    Class that measure the start time parameter on a segment
    """

    def __init__(self, decimal_places=4):
        TimeParameter.__init__(self, decimal_places=decimal_places)
        self.name = "Start(s)"

    def measure(self, segment):
        return round(segment.indexFrom * 1.0 / segment.signal.samplingRate, self.decimal_places)