import numpy as np
from pylab import mlab
from sound_lab_core.ParametersMeasurement.SpectralParameters.FreqParameter import SpectralParameter

EPS = 1e-9


class DeltaSpectrumParameter(SpectralParameter):
    """
    Class that measure the max freq parameter on a segment
    """

    def __init__(self, func, funcName, decimal_places=2):
        SpectralParameter.__init__(self, decimal_places=decimal_places)
        self.name = "Delta Spectrum " + funcName
        self.func = func

    def _delta_spectrum(self, frames):
        result = np.zeros(len(frames))
        for i in range(len(frames)):
            frame = frames[i]
            delta = 0.0
            for j in range(len(frame)-1):
                delta += (np.log(abs(1.0*frame[j+1])+EPS) - np.log(abs(1.0*frame[j])+EPS))**2
            result[i] = delta/(len(frame)-1)
        return result

    def measure(self, segment):
        data = self.time_location.get_data_array_slice(segment)
        s, freqs, bins = mlab.specgram(data, Fs=segment.signal.samplingRate, NFFT=512, noverlap=-1)
        s = np.transpose(s)

        return round(self.func(self._delta_spectrum(s)), self.decimal_places)

