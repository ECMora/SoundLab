# -*- coding: utf-8 -*-
from . import DECIMAL_PLACES
import numpy as np
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer


class PeakToPeakParameter(ParameterMeasurer):
    """
    Class that measure the Peak to Peak parameter on a segment
    """

    def __init__(self):
        ParameterMeasurer.__init__(self)
        self.name = "PeekToPeek(V)"

    def measure(self, segment):
        return np.round(np.ptp(segment.signal.data[segment.indexFrom:segment.indexTo] /
                            float(segment.signal.maximumValue)), DECIMAL_PLACES)