import numpy as np
from math import ceil, log
from numpy.fft import fft, ifft
from duetto.signal_processing.SignalProcessor import SignalProcessor


class FilterSignalProcessor(SignalProcessor):
    """
    Class that encapsulate the operation of filter a signal.
    A filter operation could be done in frequency or time domain
    """
    def __init__(self, signal=None):
        SignalProcessor.__init__(self, signal)

    def filter(self, indexFrom=0, indexTo=-1):
        """
        The virtual method that is executed for the filter action.
        Execute a filter on the frequencies of a signal in the given interval.
        :param indexFrom: Start index of the filtered interval in signal array data indexes.
        :param indexTo: End index of the filtered interval in signal array data indexes.
        :return:
        """
        pass