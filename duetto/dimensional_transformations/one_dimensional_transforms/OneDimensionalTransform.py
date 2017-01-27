# -*- coding: utf-8 -*-
import numpy as np
from duetto.audio_signals import AudioSignal


class OneDimensionalTransform(object):
    """
    This is an abstract class that represents an one dimensional signal transformation
    """

    def __init__(self, signal=None):

        object.__init__(self)
        self._signal = signal
        self._data = None

    # region Properties signal, data

    @property
    def signal(self):
        return self._signal

    @signal.setter
    def signal(self, new_signal):
        """
        Modify and update the internal variables that uses the signal.
        :param new_signal: the new AudioSignal
        :raise Exception: If signal is not of type AudioSignal
        """
        if new_signal is None or not isinstance(new_signal, AudioSignal):
            raise Exception("Invalid assignation value. Must be of type AudioSignal")
        self._signal = new_signal

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    # endregion


    def getData(self, indexFrom, indexTo):
        """
        Computes and returns the one dimensional one_dim_transform
        over the signal data in the supplied interval.
        :param indexFrom: the start of the signal interval to process in signal array data indexes.
        :param indexTo: the end of the signal interval to process in signal array data indexes..
        """
        return np.zeros(indexTo-indexFrom)





