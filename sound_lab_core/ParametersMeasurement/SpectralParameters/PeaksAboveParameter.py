# -*- coding: utf-8 -*-
from matplotlib import mlab
import numpy as np
from scipy.ndimage import label
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer


class PeaksAboveParameter(ParameterMeasurer):
    """
    Class that measure the peaks above parameter on a segment
    """

    def __init__(self, threshold=-20, decimal_places=2, measurement_location=None):
        ParameterMeasurer.__init__(self, decimal_places=decimal_places, measurement_location=measurement_location)
        self.name = "PeaksAbove"
        self.threshold = threshold

    def measure(self, segment):
        # frequency_params is a tuple Pxx, freqs shared by all the frequency parameters
        # on their measurements
        if "frequency_params" not in segment.memory_dict:
            Pxx, freqs = mlab.psd(segment.signal.data[segment.indexFrom:segment.indexTo], Fs=segment.signal.samplingRate,noverlap=128)
            segment.memory_dict["frequency_params"] = (Pxx, freqs)

        Pxx, freqs = segment.memory_dict["frequency_params"]
        value = np.amax(Pxx) * np.power(10, self.threshold/10.0)
        _, cnt_regions = label(Pxx >= value)
        return cnt_regions

