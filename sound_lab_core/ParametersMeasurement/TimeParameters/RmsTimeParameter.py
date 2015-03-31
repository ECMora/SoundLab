# -*- coding: utf-8 -*-
import numpy as np
from utils.Utils import DECIMAL_PLACES
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

        return np.round(np.sqrt(np.mean(np.square(segment.signal.data[indexFrom:indexTo] /
                        np.amax(segment.signal.maximumValue)))), DECIMAL_PLACES)