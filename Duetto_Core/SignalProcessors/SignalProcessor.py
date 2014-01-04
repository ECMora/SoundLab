import numpy
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


def envelope(signal, indexFrom=0, indexTo=-1, decimation=1, decay=1):
    if indexTo == -1 :
        indexTo = len(signal.data)

    decay *= signal.samplingRate/1000  #salto para evitar caidas locales
    print(len(signal.data))
    if decimation > 1:
        rectified = numpy.array([(abs(x) if i %decimation == 0 else numpy.mean(abs(signal.data[i-i%decimation:i]))) for i, x in enumerate(signal.data[indexFrom: indexTo])])
    else:
        rectified = numpy.array(abs(signal.data[indexFrom: indexTo]))

    i = 1
    arr = numpy.zeros(len(rectified), dtype=numpy.uint32)
    current = rectified[0]
    arr[0] = current
    while i < len(arr):
        if rectified[i] < current:
            interval = min(decay, len(arr)-i-1)
            arr[i+1:i+interval] = [arr[i]+x*(arr[i]-arr[i+interval])/(-interval) for x in range(1, interval)]
            print("LLLLLLLLLLLLLLLLLLLLLLLLLLLL")
            current = arr[i+interval]
            i += interval
        else:
            current = rectified[i]
            arr[i] = current
        i += 1

    for i, x in enumerate(arr):
        print(str(x)+" --------  "+ str(rectified[i]))
    return arr





