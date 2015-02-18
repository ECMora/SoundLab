# -*- coding: utf-8 -*-
from . import DECIMAL_PLACES
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer


class EndTimeParameter(ParameterMeasurer):
    """
    Class that measure the start time paramter on a segment
    """

    def __init__(self):
        ParameterMeasurer.__init__(self)
        self.name = "End(s)"

    def measure(self, segment):
        return round(segment.indexTo * 1.0 / segment.signal.samplingRate, DECIMAL_PLACES)