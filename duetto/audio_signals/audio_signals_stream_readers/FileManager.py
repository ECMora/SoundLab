import io
from duetto.audio_signals.audio_signals_stream_readers.WavStreamManager import WavStreamManager


# noinspection PyClassHasNoInit
class Format:
    """
    Enum-type class with all the formats allowed by FileManager
    """
    WAV = 0


class FileManager:
    """
    This class is a factory for classes derived from AudioStreamManager. It also has methods that handle opening files
    and reading from or writing to them.
    """

    # dictionary mapping format to the respective class derived from AudioStreamManager
    _dict_fc = {Format.WAV: WavStreamManager}
    # dictionary mapping file extension to format
    _dict_ef = {'.wav': Format.WAV}

    def __init__(self):
        pass

    def getAudioStreamManager(self, fileName, fileFormat=None):
        """
        Given a file (and optionally its format), returns an instance of the corresponding class derived from
        AudioStreamManager. The class is determined by fileFormat; if it is None, then the format will be inferred from
        the file extension.
        :param fileName: str.
            The name of the file to read from or write to.
        :param fileFormat: int.
            A value from the Format enum. If it is None, then the format will be inferred from the file extension.
        :return: An instance of a class derived from AudioStreamManager.
        """
        if fileFormat is None:
            # noinspection PyPep8Naming
            fileFormat = FileManager.inferFormat(fileName)
        cls = FileManager._dict_fc[fileFormat]
        return cls()

    def write(self, audioSignal, fileName, format=None):
        """
        Writes an audioSignal to a file in the specified format. If format is None, then the format will be inferred
        from the file extension.
        :param audioSignal: An instance of AudioSignal.
            The signal to be written to the file.
        :param fileName: str.
            The name of the file to which to write.
        :param format: int
            A value from the Format enum. If it is None, then the format will be inferred from the file extension.
        :param userData: bytearray.
            Additional data to be written to the file (Note: some formats may not support this)
        :return: Nothing
        """
        mng = self.getAudioStreamManager(fileName, format)
        stream = open(fileName, 'wb')  # TODO: in the future it'd be better to use io.open instead of __builtin__.open
        mng.write(audioSignal, stream)

    def read(self, fileName, format=None):
        """
        Reads an audio signal from a file in the specified format. If format is None, then the format will be inferred
        from the file extension. Returns the read signal.
        :param fileName: str.
            The name of the file from which to read.
        :param format: int
            A value from the Format enum. If it is None, then the format will be inferred from the file extension.
        :return: An instance of AudioSignal.
        """
        mng = self.getAudioStreamManager(fileName, format)
        stream = open(fileName, 'rb')  # TODO: in the future it'd be better to use io.open instead of __builtin__.open
        return mng.read(stream)

    @staticmethod
    def inferFormat(fileName):
        """
        Infers a file's format from its file extension. The format is returned as a value from the Format enum.
        :param fileName: str.
            The name of the file.
        :return: int
        """
        return FileManager._dict_ef[fileName[-4:]]
