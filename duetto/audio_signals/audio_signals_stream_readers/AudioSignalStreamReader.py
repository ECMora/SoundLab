# -*- coding: utf-8 -*-
from duetto.audio_signals.AudioSignal import AudioSignal


class AudioSignalStreamReader:
    """
    this class represents a handler for read and save audio file from a hard storage device
    the source could be the filesystem or any connection that provides a way to get
    an audio signal through a path.
    """

    def __init__(self):
        self.signal = AudioSignal()

    def removeDCOffset(self):
        """
        Update the values of data array if the stored values was treated as unsigned.
        :return:
        """
        if len(self.signal.data) == 0:
            return
        if self.signal.data.dtype.str[1] == 'u':
            self.signal.data = (self.signal.data - (1 << (self.signal.data.dtype.itemsize * 8 - 1))) \
                .astype(self.signal.data.dtype.str.replace('u', 'i'))

    def read(self, path):
        """
        read an audio signal from a given source path
        """
        raise NotImplementedError()

    def save(self, path):
        """
        saves an audio signal to a given source path
        """
        raise NotImplementedError()
