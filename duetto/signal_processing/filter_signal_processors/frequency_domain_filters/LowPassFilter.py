from duetto.signal_processing.filter_signal_processors.FilterSignalProcessor import *


class LowPassFilter(FilterSignalProcessor):
    """
    Class that executes a low pass filter on the frequencies of an AudioSignal
    """

    def __init__(self,signal=None,Fc=0):
        FilterSignalProcessor.__init__(self,signal)
        self.cut_frequency = Fc

    def filter(self,indexFrom=0,indexTo=-1,):
        if self.signal is None:
            return

        if indexTo == -1:
            indexTo = len(self.signal)

        if self.checkIndexesOk(indexFrom, indexTo):
            n = int(ceil(log(indexTo - indexFrom, 2)))
            data_frec = fft(self.signal.data[indexFrom:indexTo], 2**n)
            n = 2 ** n
            indexFrecuency = (n * 1.0) / self.signal.samplingRate
            cut_frequency = int(self.cut_frequency * indexFrecuency)
            size = len(data_frec)

            if cut_frequency != 0 and cut_frequency < n / 2:
                data_frec[cut_frequency:size - cut_frequency + 1] = complex(0, 0)
            elif cut_frequency == 0:
                data_frec[:] = complex(0, 0)

            if indexFrom == 0 and indexTo == len(self.signal.data):
                self.signal.data = np.array(np.real(ifft(data_frec)[0:indexTo - indexFrom]), self.signal.data.dtype)
            else:
                self.signal.data = np.concatenate((self.signal.data[0:indexFrom],
                                              np.array(np.real(ifft(data_frec)[0:indexTo-indexFrom]),
                                              self.signal.data.dtype),
                                              self.signal.data[indexTo:]
                                              ))
            return self.signal
        else:
            raise IndexError()