# -*- coding: utf-8 -*-
from matplotlib import mlab
import numpy as np
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer
from sound_lab_core.ParametersMeasurement.WaveletParameters import *
import pywt


class WaveletMeanParameter(ParameterMeasurer):
    """
    Class that measure the max freq parameter on a segment
    """

    def __init__(self, level, wavelet="db10"):
        ParameterMeasurer.__init__(self)
        self.wavelet = wavelet
        self.level = level
        self.name = "Wavelet Level {0} Mean".format(level)

    def measure(self, segment):
        dec = pywt.wavedec(segment.signal.data[segment.indexFrom:segment.indexTo], self.wavelet, level=6)

        return np.mean(np.abs(dec[self.level]))

