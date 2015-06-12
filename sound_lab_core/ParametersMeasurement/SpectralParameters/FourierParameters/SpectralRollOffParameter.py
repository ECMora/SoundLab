import numpy as np
from pylab import mlab
from sound_lab_core.ParametersMeasurement.SpectralParameters.FreqParameter import SpectralParameter


class SpectralRollOffParameter(SpectralParameter):
    """
    Class that measure the max freq parameter on a segment
    """

    def __init__(self, func, funcName, decimal_places=2):
        SpectralParameter.__init__(self, decimal_places=decimal_places)
        self.name = "Spectral RollOff " + funcName
        self.func = func

    def _spectral_rolloff(self, frames, freqs):
        result = np.zeros(len(frames))
        for i in xrange(len(frames)):
            frame = frames[i]
            w = np.amin(frame)
            frame = frame - w
            sum = np.cumsum(np.multiply(frame, frame))
            lo = 0
            hi = len(frame)-1
            th = 0.92
            while lo <= hi:
                m = (lo+hi)/2
                if sum[m] < th * sum[-1]:
                    lo = m+1
                else:
                    hi = m-1
            result[i] = freqs[hi]
        return result

    def measure(self, segment):
        data = self.time_location.get_data_array_slice(segment)

        s, freqs, bins = mlab.specgram(data, Fs=segment.signal.samplingRate, NFFT=512, noverlap=-1)
        s = np.transpose(s)

        return round(self.func(self._spectral_rolloff(s, freqs)), self.decimal_places)

