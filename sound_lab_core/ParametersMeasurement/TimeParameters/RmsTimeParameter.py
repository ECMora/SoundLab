# -*- coding: utf-8 -*-
from math import sqrt
from Utils.Utils import DECIMAL_PLACES
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer


class RmsTimeParameter(ParameterMeasurer):
    """
    Class that measure the start time paramter on a segment
    """

    def __init__(self):
        ParameterMeasurer.__init__(self)
        self.name = "RMS(V)"

    def measure(self, segment):
        indexFrom, indexTo = segment.indexFrom, segment.indexTo

        globalSum = 0.0
        intervalSum = 0.0
        for i in range(indexFrom, indexTo):
            intervalSum += (segment.signal.data[i] ** 2)
            if i % 10 == 0:
                globalSum += intervalSum * 1.0 / max(indexTo - indexFrom, 1)
                intervalSum = 0.0

        globalSum += intervalSum * 1.0 / max(indexTo - indexFrom, 1)
        return round(sqrt(globalSum) * 1.0 / segment.signal.maximumValue, DECIMAL_PLACES)