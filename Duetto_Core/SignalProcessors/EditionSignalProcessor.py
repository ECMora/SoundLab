# coding=utf-8
from numpy import array, concatenate
from Duetto_Core.AudioSignals.WavFileSignal import WavFileSignal
from Duetto_Core.SignalProcessors.SignalProcessor import SignalProcessor

class EditionSignalProcessor(SignalProcessor):
    def __init__(self, signal=None):
        SignalProcessor.__init__(self, signal)
        self.clipboard = []

    def cut(self, start_index, end_index):
        if start_index > end_index or start_index < 0 or end_index > len(self.signal.data):
            raise IndexError("Hubo un error con el orden o con los valores de los índices. Deben ser menores que el "
                             "tamaño del array de datos y start_index < end_index")
        self.clipboard = array(self.signal.data[start_index:end_index])
        self.signal.data = concatenate((self.signal.data[0:start_index], self.signal.data[end_index:]))
        return self.signal

    def copy(self, start_index, end_index):
        self.clipboard = array(self.signal.data[start_index:end_index])
        return self.signal

    def paste(self, data, startpos):
        self.signal.data = concatenate((self.signal.data[0:startpos], array(data), self.signal.data[startpos:]))
        return self.signal

