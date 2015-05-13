# -*- coding: utf-8 -*-
from matplotlib import mlab
import numpy as np
from sound_lab_core.ParametersMeasurement.SpectralParameters.FreqParameter import FreqParameter


class MaxFreqParameter(FreqParameter):
    """
    Class that measure the max freq parameter on a segment
    """

    def __init__(self, threshold=-20, total=True, decimal_places=2, measurement_location=None):
        FreqParameter.__init__(self, threshold, total, decimal_places=decimal_places,
                               measurement_location=measurement_location)
        self.name = "MaxFreq(kHz)"

    def measure(self, segment):
        # frequency_params is a tuple Pxx, freqs shared by all the frequency parameters
        # on their measurements
        if "frequency_params" not in segment.memory_dict:
            Pxx, freqs = mlab.psd(segment.signal.data[segment.indexFrom:segment.indexTo],
                                  Fs=segment.signal.samplingRate, noverlap=128)
            segment.memory_dict["frequency_params"] = (Pxx, freqs)

        Pxx, freqs = segment.memory_dict["frequency_params"]
        value = np.amax(Pxx) * np.power(10,self.threshold/10.0)

        if self.total:
            max_freq_index = np.argwhere(Pxx >= value).max()
        else:
            below = Pxx < value
            peak_index = np.argmax(Pxx)
            below[:peak_index] = False
            max_freq_index = np.argwhere(below).min() - 1
        return round((freqs[max_freq_index] - freqs[max_freq_index] % 10)/1000.0, self.decimal_places)