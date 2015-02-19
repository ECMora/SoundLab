# -*- coding: utf-8 -*-
from matplotlib import mlab
import numpy as np
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer
from sound_lab_core.ParametersMeasurement.SpectralParameters import DECIMAL_PLACES


class BandWidthParameter(ParameterMeasurer):
    """
    Class that measure the band width parameter on a segment
    """

    def __init__(self, threshold=-20,total=True):
        ParameterMeasurer.__init__(self)
        self.name = "BandWidth(kHz)"
        self.threshold = threshold
        self.total=total

    def measure(self, segment):
        Pxx, freqs = mlab.psd(segment.signal.data[segment.indexFrom:segment.indexTo], Fs=segment.signal.samplingRate,noverlap=128)
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

        band_with = (freqs[max_freq_index] - freqs[min_freq_index])

        return round((band_with - band_with % 10)/1000.0, DECIMAL_PLACES)
