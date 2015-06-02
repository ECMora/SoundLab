# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer


class ShortTimeEnergyParameter(ParameterMeasurer):
    """
    Class that measure the start time paramter on a segment
    """

    def __init__(self, decimal_places=2):
        ParameterMeasurer.__init__(self, decimal_places=decimal_places)
        self.name = "Short Time Energy"

    def measure(self, segment):
        data = segment.signal.data[segment.indexFrom:segment.indexTo]
        return sum([1.0*x*x for x in data]) / len(data)
