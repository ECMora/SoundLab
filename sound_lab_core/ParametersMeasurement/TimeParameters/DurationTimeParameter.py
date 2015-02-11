# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer


class DurationTimeParameter(ParameterMeasurer):
    """
    Class that measure the start time paramter on a segment
    """

    def __init__(self):
        ParameterMeasurer.__init__(self)
        self.name = "Duration(s)"

    def measure(self, segment):
        return 0