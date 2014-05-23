import numpy as np
from ..AudioSignals.AudioSignal import AudioSignal


class SignalProcessor:
    """
    Class that execute several functionalities with an AudioSignal
    Provides methods that modify the values on the signal but not its size
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

    def checkIndexes(self, indexFrom, indexTo):
        """
        check that the specified indexes are in the range of the signal data
        """
        dataLength = len(self.signal.data)
        if indexFrom < 0 or indexFrom > indexTo or indexTo > dataLength:
            raise IndexError()








