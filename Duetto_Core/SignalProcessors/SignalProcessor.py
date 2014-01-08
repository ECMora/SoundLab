import math
import numpy
import matplotlib.mlab as mlab
from Duetto_Core.AudioSignals.AudioSignal import AudioSignal
from Duetto_Core.AudioSignals.WavFileSignal import WavFileSignal


class SignalProcessor:
    """
    Class that execute several functionalities with an AudioSignal
    """
    def __init__(self, signal=WavFileSignal()):
        self._signal = signal

    #region Propiedad SIGNAL
    def _getSignal(self):
        return self._signal
    def _setSignal(self, value):
        assert isinstance(value, AudioSignal)
        self._signal = value

    signal = property(_getSignal, _setSignal)
    #endregion

    def rms(self, indexFrom=0, indexTo=-1):
        """
        computes the root mean square of the signal.
        indexFrom,indexTo the optionally limits of the interval
        """
        if indexTo == -1:
            indexTo = len(self.signal.data)
        n = indexTo-indexFrom
        globalSum = 0.0
        intervalSum = 0.0
        for i in range(n):
            intervalSum += (self.signal.data[indexFrom+i]**2)
            if i % 10 == 0:
                globalSum += intervalSum * 1.0 / n
                intervalSum = 0.0

        globalSum += intervalSum * 1.0 / n
        return numpy.sqrt(globalSum)

    def checkIndexes(self, indexFrom, indexTo):
        """
        check that the specified indexes are in the range of the signal data
        """
        dataLength = len(self.signal.data)
        if indexFrom > indexTo or indexFrom >= dataLength or indexTo > dataLength:
            raise IndexError()


def envelope(signal, indexFrom=0, indexTo=-1, decay=1):
    if indexTo == -1 :
        indexTo = len(signal.data)
    rectified = numpy.array(abs(signal.data[indexFrom: indexTo]))
    i = 1
    arr = numpy.zeros(len(rectified), dtype=numpy.uint32)
    current = rectified[0]
    fall_init = None
    while i < len(arr):
        if fall_init is not None:
            value = rectified[fall_init] - rectified[fall_init]*(i-fall_init)/decay    #formula
            arr[i-1] = value
            fall_init = None if(value <= rectified[i] or i-fall_init >= decay) else fall_init
        else:
            fall_init = i-1 if rectified[i] < current else None
            arr[i-1] = current
        current = rectified[i]
        i += 1

    arr[-1] = current
    return arr





