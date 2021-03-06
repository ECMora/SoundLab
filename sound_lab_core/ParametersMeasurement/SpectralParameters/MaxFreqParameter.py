# -*- coding: utf-8 -*-
import numpy as np
from sound_lab_core.ParametersMeasurement.SpectralParameters.FreqParameter import FreqParameter


class MaxFreqParameter(FreqParameter):
    """
    Class that measure the max freq parameter on a segment
    """

    def __init__(self, **kwargs):
        FreqParameter.__init__(self, **kwargs)
        self.name = "MaxFreq(kHz)"

    def measure(self, segment):
        # frequency_params is a tuple Pxx, freqs shared by all the frequency parameters
        # on their measurements
        Pxx, freqs = self.time_location.get_segment_data(segment)

        min_freq_limit_index, max_freq_limit_index = self.spectral_location.get_freq_limits(freqs)

        Pxx = Pxx[min_freq_limit_index:max_freq_limit_index]

        if len(Pxx) == 0:
            return round((freqs[max_freq_limit_index] - freqs[max_freq_limit_index] % 10)/1000.0, self.decimal_places)

        max_value = np.amax(Pxx)
        if max_value == 0:
            max_value = 1.0

        Pxx = 10. * np.log10(Pxx / max_value)

        if not self.total:
            max_freq_index = np.argwhere(Pxx >= self.threshold).max()

        else:
            below = Pxx < self.threshold
            peak_index = np.argmax(Pxx)
            below[:peak_index] = False
            max_freq_index = np.argwhere(below).min() - 1

        max_freq_index += min_freq_limit_index

        return round((freqs[max_freq_index] - freqs[max_freq_index] % 10)/1000.0, self.decimal_places)