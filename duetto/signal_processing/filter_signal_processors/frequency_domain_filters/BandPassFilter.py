from duetto.signal_processing.filter_signal_processors.FilterSignalProcessor import *


class BandPassFilter(FilterSignalProcessor):
    """
    Class that executes a Band Pass filter on a range [x1,x2] of the
    frequencies of an AudioSignal
    """

    def __init__(self, signal=None, frequency_lower=0, frequency_upper=0):
        FilterSignalProcessor.__init__(self,signal)
        self.frequency_cut_upper = frequency_upper
        self.frequency_cut_lower = frequency_lower

    def filter(self,indexFrom=0, indexTo=-1):
        if self.signal is None:
            return

        if indexTo == -1:
            indexTo = len(self.signal.data)

        if self.checkIndexesOk(indexFrom, indexTo):
            n = int(ceil(log(indexTo - indexFrom, 2)))

            data_frec = fft(self.signal.data[indexFrom:indexTo], 2 ** n)
            n = 2 ** n

            indexFrecuency = (n * 1.0) / self.signal.samplingRate
            frequency_cut_lower, frequency_cut_upper = int(round(self.frequency_cut_lower * indexFrecuency)), \
                                                                 int(round(self.frequency_cut_upper * indexFrecuency))
            size = len(data_frec)

            data_frec[frequency_cut_upper:size - frequency_cut_upper + 1] = complex(0,0)
            data_frec[:frequency_cut_lower + 1] = complex(0, 0)
            data_frec[-frequency_cut_lower:] = complex(0, 0)

            if indexFrom == 0 and indexTo == len(self.signal):
                 self.signal.data = np.array(np.real(ifft(data_frec)[0:indexTo - indexFrom]), self.signal.data.dtype)
            else:
                self.signal.data = np.concatenate((self.signal.data[0:indexFrom],
                                                   np.array(np.real(ifft(data_frec)[0:indexTo - indexFrom]), self.signal.data.dtype),
                                                   self.signal.data[indexTo:]))

            return self.signal
        else:
            raise IndexError()



