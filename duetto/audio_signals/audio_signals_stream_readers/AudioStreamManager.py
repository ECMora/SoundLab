class AudioStreamManager:
    """
    This is the abstract base class for all classes that read and write audio signals from and to streams.
    Derived classes should implement the read and write methods according to each format (e.g. wav, mp3, etc.)
    """

    def __init__(self):
        pass

    def read(self, stream):
        """
        Reads an audio signal from a given readable stream. Returns the read signal.
        :param stream: An instance of a class derived from io.IOBase.
            The stream from which to read. A call to its readable() method must return True.
        """
        raise NotImplementedError()

    def write(self, audioSignal, stream, userData=bytearray([])):
        """
        Writes an audio signal to a given writable stream. Returns nothing.
        :param audioSignal: An instance of AudioSignal.
            The signal to be written to the stream.
        :param stream: An instance of a class derived from io.IOBase.
            The stream in which to write. A call to its writable() method must return True.
        """
        raise NotImplementedError()
