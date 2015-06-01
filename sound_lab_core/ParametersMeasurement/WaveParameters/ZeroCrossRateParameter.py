# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer
import numpy as np


class ZeroCrossRateParameter(ParameterMeasurer):
    """
    Class that measure the zero cross rate parameter on a segment
    """

    def __init__(self, decimal_places=2):
        ParameterMeasurer.__init__(self, decimal_places=decimal_places)
        self.name = "ZeroCrossRate"

    def measure(self, segment):
        a = segment.signal.data[segment.indexFrom:segment.indexTo]
        return round((len(np.where(a[:-1] * a[1:] <= 0)) * 1.0) / (a.size - 1), self.decimal_places)