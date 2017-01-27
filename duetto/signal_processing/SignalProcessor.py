from PyQt4.QtCore import QObject

from duetto.audio_signals.AudioSignal import AudioSignal


class SignalProcessor(QObject):
    """
    Class that provides functions that modify an AudioSignal.
    Provides methods that modify the values on the data array of the signal.

    """
    def __init__(self, signal=None):
        """
        Create a Signal Processor for the signal.
        :param signal: The AudioSignal for processing
        :raise Exception: If signal is None or is not instance of AudioSignal
        """
        QObject.__init__(self)
        if self.__checkSignalOk(signal):
            self._signal = signal
        else:
            raise Exception("Invalid parameter. Signal must be of type AudioSignal.")

    # region Propiedad SIGNAL

    @property
    def signal(self):
        return self._signal

    @signal.setter
    def signal(self, value):
        if self.__checkSignalOk(value):
            self._signal = value
        else:
            raise Exception("Invalid value. Signal must be not None and of type AudioSignal.")
    # endregion

    def __checkSignalOk(self, signal):
        """
        Check if the variable 'signal' is of type AudioSignal
        :param signal: The AudioSignal instance variable
        :return: True if signal is of type AudioSignal False otherwise
        """
        return isinstance(signal, AudioSignal)

    def checkIndexesOk(self, indexFrom, indexTo):
        """
        Check that the specified indexes are in the range of the signal data
        and indexFrom <= indexTo for signal processing operations.
        """
        return 0 <= indexFrom <= indexTo and indexTo <= len(self.signal)
