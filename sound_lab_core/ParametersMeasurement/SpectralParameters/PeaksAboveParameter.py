# -*- coding: utf-8 -*-
from matplotlib import mlab
import numpy as np
from scipy.ndimage import label
from sound_lab_core.ParametersMeasurement.SpectralParameters.FreqParameter import SpectralParameter


class PeaksAboveParameter(SpectralParameter):
    """
    Class that measure the peaks above parameter on a segment
    """

    def __init__(self, threshold=-20, decimal_places=2, time_measurement_location=None):
        SpectralParameter.__init__(self, decimal_places=decimal_places,
                                   time_measurement_location=time_measurement_location)
        self.name = "PeaksAbove"
        self.threshold = threshold

    def measure(self, segment):
        # frequency_params is a tuple Pxx, freqs shared by all the frequency parameters
        # on their measurements
        Pxx, freqs = self.time_location.get_segment_data(segment)

        min_freq_index, max_freq_index = self.spectral_location.get_freq_limits(freqs)

        Pxx = Pxx[min_freq_index:max_freq_index]

        value = np.amax(Pxx) * np.power(10, self.threshold/10.0)
        _, cnt_regions = label(Pxx >= value)
        return cnt_regions


