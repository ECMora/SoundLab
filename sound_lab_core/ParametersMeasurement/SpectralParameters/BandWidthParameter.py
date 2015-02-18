# -*- coding: utf-8 -*-
from Utils.Utils import DECIMAL_PLACES
from matplotlib import mlab
import numpy as np
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer


class BandWidthParameter(ParameterMeasurer):
    """
    Class that measure the band width parameter on a segment
    """

    def __init__(self, threshold=-20):
        ParameterMeasurer.__init__(self)
        self.name = "BandWidth(kHz)"
        self.threshold = threshold

    def measure(self, segment):
        Pxx, freqs = mlab.psd(segment.signal.data[segment.indexFrom:segment.indexTo], Fs=segment.signal.samplingRate)
        value = np.amax(Pxx) * np.power(10, self.threshold / 10.0)
        max_freq_index = np.argwhere(Pxx >= value).max()
        min_freq_index = np.argwhere(Pxx >= value).min()
        return round((freqs[max_freq_index] - freqs[min_freq_index]) / 1000.0, DECIMAL_PLACES)
