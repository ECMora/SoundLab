from numpy.fft import rfft
import numpy
from Duetto_Core.SignalProcessors.SignalProcessor import SignalProcessor


class CompensationSignalProcessor(SignalProcessor):
    def __init__(self, signal, v_p_rel_curve, freqs):
        SignalProcessor.__init__(self, signal)
        self._v_p_rel_curve = v_p_rel_curve
        self._freqs = freqs

    def compensate(self):
        ft = rfft(self.signal)
        ft_freqs = numpy.linspace(0, self.signal.samplingRate / 2., len(ft))
