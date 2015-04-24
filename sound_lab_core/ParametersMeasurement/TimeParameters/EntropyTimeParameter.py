# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer
from . import DECIMAL_PLACES


class EntropyTimeParameter(ParameterMeasurer):
    """
    Class that measure the entropy parameter on a segment
    """

    def __init__(self):
        ParameterMeasurer.__init__(self)
        self.name = "Entropy"

    def measure(self, segment):
        return 0