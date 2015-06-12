import numpy as np
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer
import pywt

EPS = 1e-9


class WaveletDeltaParameter(ParameterMeasurer):
    """
    Class that measure the max freq parameter on a segment
    """

    def __init__(self, level, wavelet="db10", decimal_places=2):
        ParameterMeasurer.__init__(self, decimal_places=decimal_places)
        self.wavelet = wavelet
        self.level = level
        self.name = "Wavelet Level {0} Delta".format(level)

    def delta(self, m):
        result = 0
        for i in xrange(len(m)-1):
            if m[i+1] > EPS:
                result += (abs(m[i]/m[i+1]))
        return result

    def measure(self, segment):
        dec = pywt.wavedec(segment.signal.data[segment.indexFrom:segment.indexTo], self.wavelet, level=6)

        return round(self.delta(np.abs(dec[self.level])), self.decimal_places)

