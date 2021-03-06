import numpy as np
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer
import pywt

EPS = 1e-9


class WaveletCentroidParameter(ParameterMeasurer):
    """
    Class that measure the max freq parameter on a segment
    """

    def __init__(self, level, wavelet="db10", decimal_places=2):
        ParameterMeasurer.__init__(self, decimal_places=decimal_places)
        self.wavelet = wavelet
        self.level = level
        self.name = "Wavelet Level {0} Centroid".format(level)

    def centroid(self, v):
        num = 0.0
        dem = 0.0
        for i in xrange(len(v)):
            num += v[i] * v[i] * i
            dem += v[i] * v[i]

        return 0 if dem < EPS else num/dem

    def measure(self, segment):
        dec = pywt.wavedec(segment.signal.data[segment.indexFrom:segment.indexTo], self.wavelet, level=6)

        return round(self.centroid(np.abs(dec[self.level])), self.decimal_places)

