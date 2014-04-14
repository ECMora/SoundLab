from math import *
import numpy as np
import matplotlib.mlab as mlab
from numpy.fft import fft
from ..AudioSignals.AudioSignal import AudioSignal
from Duetto_Core.AudioSignals.WavFileSignal import WavFileSignal


class SignalProcessor:
    """
    Class that execute several functionalities with an AudioSignal
    """
    def __init__(self, signal=None):
        self._signal = signal

    #region Propiedad SIGNAL
    def _getSignal(self):
        return self._signal
    def _setSignal(self, value):
        assert isinstance(value, AudioSignal)
        self._signal = value

    signal = property(_getSignal, _setSignal)
    #endregion

    def mean(self, indexFrom=0, indexTo=-1):
        return np.mean(self.signal.data[indexFrom:indexTo])

    def checkIndexes(self, indexFrom, indexTo):
        """
        check that the specified indexes are in the range of the signal data
        """
        dataLength = len(self.signal.data)
        if indexFrom > indexTo or indexFrom >= dataLength or indexTo > dataLength:
            raise IndexError()


def envelope(data, decay=1,progress= None,position= (5,20)):
    """
    decay is the min number of samples in data that separates two elements
    """
    progress_interval = position[1]-position[0]
    if progress is not None:
        progress(position[0]+progress_interval/10.0)
    rectified = np.array(abs(data))
    if progress is not None:
        progress(position[0]+progress_interval/5.0)
    i = 1
    arr = np.zeros(len(rectified), dtype=np.int32)
    current = rectified[0]
    fall_init = None
    progress_size = len(arr)/8.0
    while i < len(arr):
        if fall_init is not None:
            value = rectified[fall_init] - rectified[fall_init]*(i-fall_init)/decay
            arr[i-1] = max(value, rectified[i])
            fall_init = None if(value <= rectified[i] or i-fall_init >= decay) else fall_init
        else:
            fall_init = i-1 if rectified[i] < current else None
            arr[i-1] = current
        current = rectified[i]
        i += 1
        if i % progress_size == 0 and progress is not None:
            progress(position[0]+(i/progress_size)*progress_interval/10.0)
    arr[-1] = current
    return arr






