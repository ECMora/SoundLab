# -*- coding: utf-8 -*-
from utils.Utils import DECIMAL_PLACES
from matplotlib import mlab
import numpy as np
from scipy.ndimage import label
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer


class PeaksAboveParameter(ParameterMeasurer):
    """
    Class that measure the peaks above parameter on a segment
    """

    def __init__(self, threshold=-20):
        ParameterMeasurer.__init__(self)
        self.name = "PeaksAbove"
        self.threshold = threshold

    def measure(self, segment):
        Pxx, freqs = mlab.psd(segment.signal.data[segment.indexFrom:segment.indexTo], Fs=segment.signal.samplingRate,noverlap=128)
        value = np.amax(Pxx) * np.power(10, self.threshold/10.0)
        _, cnt_regions = label(Pxx >= value)
        return cnt_regions

