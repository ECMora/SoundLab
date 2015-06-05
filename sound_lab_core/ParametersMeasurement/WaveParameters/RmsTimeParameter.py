# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer
import numpy as np


class RmsTimeParameter(ParameterMeasurer):
    """
    Class that measure the rms parameter on a segment
    """

    def __init__(self, decimal_places=2):
        ParameterMeasurer.__init__(self, decimal_places=decimal_places)
        self.name = "RMS(V)"

    def measure(self, segment):
        data = self.time_location.get_data_array_slice(segment)

        squares = np.square(data / float(segment.signal.maximumValue))

        return np.round(np.sqrt(np.mean(squares)), self.decimal_places)