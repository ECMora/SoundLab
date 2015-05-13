# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer


class TimeParameter(ParameterMeasurer):
    """
    Super class for time parameter measurements
    """

    def __init__(self, decimal_places=4):
        ParameterMeasurer.__init__(self, decimal_places=decimal_places)