# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer


class EntropyTimeParameter(ParameterMeasurer):
    """
    Class that measure the entropy parameter on a segment
    """

    def __init__(self, decimal_places=2):
        ParameterMeasurer.__init__(self, decimal_places=decimal_places)
        self.name = "Entropy"

    def measure(self, segment):
        return 0