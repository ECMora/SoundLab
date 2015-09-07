# -*- coding: utf-8 -*-
import numpy as np
from sound_lab_core.ParametersMeasurement.SpectralParameters.FreqParameter import FreqParameter


class BandWidthParameter(FreqParameter):
    """
    Class that measure the band width parameter on a segment
    """

    def __init__(self, threshold=-20, total=True, decimal_places=2, time_measurement_location=None):
        FreqParameter.__init__(self, threshold, total, decimal_places=decimal_places,
                               time_measurement_location=time_measurement_location)
        self.name = "BandWidth(kHz)"

    def measure(self, segment):
        # frequency_params is a tuple Pxx, freqs shared by all the frequency parameters
        # on their measurements
        Pxx, freqs = self.time_location.get_segment_data(segment)

        min_freq_limit_index, max_freq_limit_index = self.spectral_location.get_freq_limits(freqs)

        Pxx = Pxx[min_freq_limit_index:max_freq_limit_index]

        if len(Pxx) == 0:
            band_with = (freqs[max_freq_limit_index] - freqs[max_freq_limit_index])

            return round((band_with - band_with % 10)/1000.0, self.decimal_places)

        value = np.amax(Pxx) * np.power(10, self.threshold / 10.0)

        if self.total:
            min_freq_index = np.argwhere(Pxx >= value).min()
            max_freq_index = np.argwhere(Pxx >= value).max()

        else:
            below = Pxx < value
            peak_index = np.argmax(Pxx)
            below_left = below[:peak_index]
            below_right = below[peak_index:]
            min_freq_index = np.argwhere(below_left).max() + 1
            max_freq_index = np.argwhere(below_right).min() - 1 + peak_index

        min_freq_index += min_freq_limit_index
        max_freq_index += min_freq_limit_index

        band_with = (freqs[max_freq_index] - freqs[min_freq_index])

        return round((band_with - band_with % 10)/1000.0, self.decimal_places)
