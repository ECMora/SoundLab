# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer
from . import DECIMAL_PLACES


class DurationTimeParameter(ParameterMeasurer):
    """
    Class that measure the start time parameter on a segment
    """

    def __init__(self):
        ParameterMeasurer.__init__(self)
        self.name = "Duration(s)"

    def measure(self, segment):
        return round((segment.indexTo - segment.indexFrom) * 1.0 / segment.signal.samplingRate, DECIMAL_PLACES)