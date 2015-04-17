# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer


class FreqParameter(ParameterMeasurer):
    """
    Class that measure the min freq parameter on a segment
    """

    def __init__(self, threshold=-20, total=True):
        ParameterMeasurer.__init__(self)
        self.threshold = threshold
        self.total = total