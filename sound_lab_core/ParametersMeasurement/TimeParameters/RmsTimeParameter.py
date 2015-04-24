# -*- coding: utf-8 -*-
from math import sqrt
from utils.Utils import DECIMAL_PLACES
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer
import numpy as np


class RmsTimeParameter(ParameterMeasurer):
    """
    Class that measure the rms parameter on a segment
    """

    def __init__(self):
        ParameterMeasurer.__init__(self)
        self.name = "RMS(V)"

    def measure(self, segment):
        index_from, index_to = segment.indexFrom, segment.indexTo

        squares = np.square(segment.signal.data[index_from:index_to] / float(segment.signal.maximumValue))

        return np.round(np.sqrt(np.mean(squares)), DECIMAL_PLACES)