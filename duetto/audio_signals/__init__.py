import os

from duetto.audio_signals.audio_signals_stream_readers.WavStreamManager import WavStreamManager

__author__ = 'usuario'
from AudioSignal import AudioSignal


class FileAdapter:
    """
    Dependency Injection Adapter for the
    file audio signals open functionality.
    Makes an abstraction for the file specific extension handler
    that need to be instantiated in the opening process.
    """
    # dict with the pairs of extension-handler
    __adapter = {".wav": WavStreamManager}

    def getAdapter(self,ext=".wav"):
        """
        Provides the adapter for an specific file extension.
        raise exception if extension is not found.
        """
        if not isinstance(ext, (str, unicode)):
            raise Exception("Wrong parameter type. Ext must be of type string.")

        ext = ext.lower()

        if ext in self.__adapter:
            return self.__adapter[ext]()

        raise Exception("adapter not found for extension "+str(ext))

    def setAdapter(self,ext="wav",adapter=None):
        """
        Allows the users to change the handler for each extension.
        """
        if adapter is None:
            return
        self.__adapter[ext] = adapter


def openSignal(path):
    """
    Returns an audio signal from a path in the file system
    :param path:
    :return:
    """
    path = unicode(path)
    ext = os.path.splitext(path)[1]
    if not os.path.exists(path):
        raise Exception("Invalid path")

    signal = FileAdapter().getAdapter(ext).read(open(path, 'rb'))
    signal.name = os.path.basename(unicode(path))
    return signal



