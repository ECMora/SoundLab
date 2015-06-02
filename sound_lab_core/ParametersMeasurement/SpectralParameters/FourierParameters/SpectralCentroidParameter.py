import numpy as np
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer
from pylab import mlab


class SpectralCentroidParameter(ParameterMeasurer):
    """
    Class that measure the max freq parameter on a segment
    """

    def __init__(self, func, funcName):
        ParameterMeasurer.__init__(self)
        self.name = "Spectral Centroid " + funcName
        self.func = func

    def _spectral_centroid(self, frames, freqs):
        result = np.zeros(len(frames))
        for i in range(len(frames)):
            frame = frames[i]
            w = np.amin(frame)
            frame = frame - w
            num = 0.0
            dem = 0.0
            for j in range(len(frame)):
                num += 1.0 * freqs[j] * frame[j] * frame[j]
                dem += 1.0 * frame[j] * frame[j]
            if dem < 1e-9:
                result[i] = 0
            else:
                result[i] = num/dem
        return result

    def measure(self, segment):
        s, freqs, bins = mlab.specgram(segment.signal.data[segment.indexFrom:segment.indexTo], Fs=segment.signal.samplingRate, NFFT=512, noverlap=-1)
        s = np.transpose(s)

        return self.func(self._spectral_centroid(s, freqs))

