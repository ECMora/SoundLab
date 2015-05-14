# -*- coding: utf-8 -*-
from numpy import argmax
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer


class PeakFreqParameter(ParameterMeasurer):
    """
    Class that measure the peak freq parameter on a segment
    """

    def __init__(self, decimal_places=2, measurement_location=None):
        ParameterMeasurer.__init__(self, decimal_places=decimal_places, measurement_location=measurement_location)
        self.name = "PeakFreq(kHz)"

    def measure(self, segment):
        # frequency_params is a tuple Pxx, freqs shared by all the frequency parameters
        # on their measurements
        Pxx, freqs = self.location.get_segment_data(segment)
        index = argmax(Pxx)
        return round((freqs[index] - freqs[index] % 10) / 1000.0, self.decimal_places)
