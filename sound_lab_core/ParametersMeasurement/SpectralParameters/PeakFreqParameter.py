# -*- coding: utf-8 -*-
from matplotlib import mlab
from numpy import argmax
from numpy.fft import fft
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
        # frequency_params is a tuple Pxx, freqs shared by all the frequency parameters
        # on their measurements
        if "frequency_params" not in segment.memory_dict:
            Pxx, freqs = mlab.psd(segment.signal.data[segment.indexFrom:segment.indexTo],
                                  Fs=segment.signal.samplingRate, noverlap=128)
            segment.memory_dict["frequency_params"] = (Pxx, freqs)

        Pxx, freqs = segment.memory_dict["frequency_params"]

        index = argmax(Pxx)
        return round((freqs[index] - freqs[index] % 10) / 1000.0, DECIMAL_PLACES)
