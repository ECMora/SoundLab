# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer


class LocalMaxMeanParameter(ParameterMeasurer):
    """
    Class that measure the local max mean on a segment
    """

    def __init__(self, decimal_places=2):
        ParameterMeasurer.__init__(self, decimal_places=decimal_places)
        self.name = "Local Max Mean(V)"

    def measure(self, segment):

        data = abs(self.time_location.get_data_array_slice(segment))

        indexes = [i for i in xrange(1, data.size - 1) if (data[i - 1] < data[i] > data[i + 1]) or
                   (data[i] == data[i - 1] == data[i + 1])]

        return round(data[indexes].mean() / segment.signal.maximumValue, self.decimal_places)
