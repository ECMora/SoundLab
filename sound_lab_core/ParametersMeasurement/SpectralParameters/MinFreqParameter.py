# -*- coding: utf-8 -*-
from matplotlib import mlab
import numpy as np
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer
from sound_lab_core.ParametersMeasurement.SpectralParameters import DECIMAL_PLACES


class MinFreqParameter(ParameterMeasurer):
    """
    Class that measure the min freq parameter on a segment
    """

    def __init__(self, threshold=-20, total=True):
        ParameterMeasurer.__init__(self)
        self.name = "MinFreq(kHz)"
        self.threshold = threshold
        self.total = total


    def measure(self, segment):
        Pxx, freqs = mlab.psd(segment.signal.data[segment.indexFrom:segment.indexTo], Fs=segment.signal.samplingRate,noverlap=128 )
        value = np.amax(Pxx) * np.power(10,self.threshold/10.0)

        if self.total:
            min_freq_index = np.argwhere(Pxx >= value).min()
        else:
            below = Pxx < value
            peak_index = np.argmax(Pxx)
            below[peak_index:] = False
            min_freq_index = np.argwhere(below).max() + 1
        return round((freqs[min_freq_index] - freqs[min_freq_index] % 10)/1000.0, DECIMAL_PLACES)
