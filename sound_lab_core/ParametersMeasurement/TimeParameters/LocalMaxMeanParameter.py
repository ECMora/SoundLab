# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer
import duetto

class LocalMaxMeanParameter(ParameterMeasurer):
    """
    Class that measure the local max mean on a segment
    """
    DECIMAL_PLACES = 2
    def __init__(self):
        ParameterMeasurer.__init__(self)
        self.name = "Local Max Mean(V)"

    def measure(self, segment):

        data = abs(segment.signal.data[segment.indexFrom:segment.indexTo])

        indexes = [i for i in xrange(1, data.size - 1) if (data[i - 1] < data[i] > data[i + 1]) or
                   (data[i] == data[i - 1] == data[i + 1])]

        return round(data[indexes].mean() / segment.signal.maximumValue, self.DECIMAL_PLACES)
