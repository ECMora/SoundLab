# -*- coding: utf-8 -*-
from Utils.Utils import DECIMAL_PLACES
from matplotlib import mlab
import numpy as np
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer


class MaxFreqParameter(ParameterMeasurer):
    """
    Class that measure the max freq parameter on a segment
    """

    def __init__(self, threshold=-20, total=True):
        ParameterMeasurer.__init__(self)
        self.name = "MaxFreq(kHz)"
        self.threshold = threshold
        self.total = total

    def measure(self, segment):
        Pxx, freqs = mlab.psd(segment.signal.data[segment.indexFrom:segment.indexTo], Fs=segment.signal.samplingRate,noverlap=128)
        value = np.amax(Pxx) * np.power(10,self.threshold/10.0)

        if self.total:
            max_freq_index = np.argwhere(Pxx >= value).max()
        else:
            below = Pxx < value
            peak_index = np.argmax(Pxx)
            below[:peak_index] = False
            max_freq_index = np.argwhere(below).min() - 1
        return round(freqs[max_freq_index] / 1000.0, DECIMAL_PLACES)

        max_freq_index = np.argwhere(Pxx >= value).max()
        return round(freqs[max_freq_index] / 1000.0, DECIMAL_PLACES)
