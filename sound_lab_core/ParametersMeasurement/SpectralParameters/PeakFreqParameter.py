# -*- coding: utf-8 -*-
from matplotlib import mlab
from numpy import argmax
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer
from sound_lab_core.ParametersMeasurement.SpectralParameters import DECIMAL_PLACES


class PeakFreqParameter(ParameterMeasurer):
    """
    Class that measure the peak freq parameter on a segment
    """

    def __init__(self):
        ParameterMeasurer.__init__(self)
        self.name = "PeakFreq(kHz)"

    def measure(self, segment):
        Pxx, freqs = mlab.psd(segment.signal.data[segment.indexFrom:segment.indexTo], Fs=segment.signal.samplingRate,noverlap=128)
        index = argmax(Pxx)
        return round((freqs[index] - freqs[index] % 10) / 1000.0, DECIMAL_PLACES)
