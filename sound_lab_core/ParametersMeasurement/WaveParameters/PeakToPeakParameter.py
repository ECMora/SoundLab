# -*- coding: utf-8 -*-
import numpy as np
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer


class PeakToPeakParameter(ParameterMeasurer):
    """
    Class that measure the Peak to Peak parameter on a segment
    """

    def __init__(self, decimal_places=2):
        ParameterMeasurer.__init__(self, decimal_places=decimal_places)
        self.name = "PeekToPeek(V)"

    def measure(self, segment):
        data = self.time_location.get_data_array_slice(segment)

        return np.round(np.ptp(data / float(segment.signal.maximumValue)), self.decimal_places)