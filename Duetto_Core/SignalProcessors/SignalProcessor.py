import numpy as np
from ..AudioSignals.AudioSignal import AudioSignal


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








