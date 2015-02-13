# -*- coding: utf-8 -*-
from . import DECIMAL_PLACES
import numpy as np
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer


class PeekToPeekParameter(ParameterMeasurer):
    """
    Class that measure the start time paramter on a segment
    """

    def __init__(self):
        ParameterMeasurer.__init__(self)
        self.name = "PeekToPeek(V)"

    def measure(self, segment):
        return round(np.ptp(segment.signal.data[segment.indexFrom:segment.indexTo]) *
                     1.0 / segment.signal.maximumValue, DECIMAL_PLACES)