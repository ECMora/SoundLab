# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer
import numpy as np


class ZeroCrossRateParameter(ParameterMeasurer):
    """
    Class that measure the start time paramter on a segment
    """

    DECIMAL_PLACES = 4

    def __init__(self):
        ParameterMeasurer.__init__(self)
        self.name = "ZeroCrossRate"

    def measure(self, segment):
        a = segment.signal.data[segment.indexFrom:segment.indexTo]
        return round((len(np.where(a[:-1] * a[1:] <= 0)) * 1.0) / (a.size - 1), self.DECIMAL_PLACES)