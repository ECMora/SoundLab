# -*- coding: utf-8 -*-
from matplotlib import mlab
from numpy import argmax
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer


class PeakFreqParameter(ParameterMeasurer):
    """
    Class that measure the peak freq parameter on a segment
    """

    def __init__(self):
        ParameterMeasurer.__init__(self)
        self.name = "PeakFreq(Hz)"

    def measure(self, segment):
        Pxx, freqs = mlab.psd(segment.signal.data[segment.indexFrom:segment.indexTo], Fs=segment.signal.samplingRate)
        index = argmax(Pxx)
        return int(freqs[index] - freqs[index] % 100)
