# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer


class SpectralParameter(ParameterMeasurer):
    """
    Class that measure the min freq parameter on a segment
    """

    def __init__(self, **kwargs):
        ParameterMeasurer.__init__(self, **kwargs)

    def getName(self):
        """
        :return: The name and the location (if any)
        """
        location_name = "" if self.location is None else self.location.name
        return self._name + "(" + location_name + ")"


class FreqParameter(SpectralParameter):
    """
    Class that measure the min freq parameter on a segment
    """

    def __init__(self, threshold=-20, total=True, decimal_places=2, measurement_location=None):
        SpectralParameter.__init__(self, decimal_places=decimal_places, measurement_location=measurement_location)
        self.threshold = threshold
        self.total = total
