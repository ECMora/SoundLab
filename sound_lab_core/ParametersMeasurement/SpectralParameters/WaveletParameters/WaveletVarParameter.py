# -*- coding: utf-8 -*-
import numpy as np
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer
import pywt


class WaveletVarParameter(ParameterMeasurer):
    """
    Class that measure the max freq parameter on a segment
    """

    def __init__(self, level, wavelet="db10", decimal_places=2):
        ParameterMeasurer.__init__(self, decimal_places=decimal_places)
        self.wavelet = wavelet
        self.level = level
        self.name = "Wavelet Level {0} Variance".format(level)

    def measure(self, segment):
        dec = pywt.wavedec(segment.signal.data[segment.indexFrom:segment.indexTo], self.wavelet, level=6)

        return round(np.var(np.abs(dec[self.level])), self.decimal_places)

