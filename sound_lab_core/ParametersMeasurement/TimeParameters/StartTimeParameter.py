# -*- coding: utf-8 -*-
from . import DECIMAL_PLACES
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer


class StartTimeParameter(ParameterMeasurer):
    """
    Class that measure the start time parameter on a segment
    """

    def __init__(self):
        ParameterMeasurer.__init__(self)
        self.name = "Start(s)"

    def measure(self, segment):
        return round(segment.indexFrom * 1.0 / segment.signal.samplingRate, DECIMAL_PLACES)