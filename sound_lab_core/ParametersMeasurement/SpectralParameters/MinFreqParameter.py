# -*- coding: utf-8 -*-
from matplotlib import mlab
import numpy as np
from sound_lab_core.ParametersMeasurement.SpectralParameters.FreqParameter import FreqParameter


class MinFreqParameter(FreqParameter):
    """
    Class that measure the min freq parameter on a segment
    """

    def __init__(self, threshold=-20, total=True, decimal_places=2,
                 measurement_location=None):
        FreqParameter.__init__(self,threshold, total, decimal_places=decimal_places, measurement_location=measurement_location)
        self.name = "MinFreq(kHz)"

    def measure(self, segment):
        # frequency_params is a tuple Pxx, freqs shared by all the frequency parameters
        # on their measurements
        if "frequency_params" not in segment.memory_dict:
            Pxx, freqs = mlab.psd(segment.signal.data[segment.indexFrom:segment.indexTo],
                                  Fs=segment.signal.samplingRate, noverlap=128)
            segment.memory_dict["frequency_params"] = (Pxx, freqs)

        Pxx, freqs = segment.memory_dict["frequency_params"]
        value = np.amax(Pxx) * np.power(10, self.threshold/10.0)

        if self.total:
            min_freq_index = np.argwhere(Pxx >= value).min()
        else:
            below = Pxx < value
            peak_index = np.argmax(Pxx)
            below[peak_index:] = False
            min_freq_index = np.argwhere(below).max() + 1
        return round((freqs[min_freq_index] - freqs[min_freq_index] % 10)/1000.0, self.decimal_places)
