# -*- coding: utf-8 -*-
import numpy as np
from . import DECIMAL_PLACES
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer


class StartToMaxTimeParameter(ParameterMeasurer):
    """
    Class that measure the start time paramter on a segment
    """

    def __init__(self):
        ParameterMeasurer.__init__(self)
        self.name = "StartToMax(s)"

    def measure(self, segment):
        return round(np.argmax(segment.signal.data[segment.indexFrom:segment.indexTo])
                     * 1.0 / segment.signal.samplingRate, DECIMAL_PLACES)