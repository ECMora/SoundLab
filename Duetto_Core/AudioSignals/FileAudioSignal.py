from Duetto_Core.AudioSignals.AudioSignal import AudioSignal


class FileAudioSignal(AudioSignal):
    """
    this class represents an audio file from a hard storage device
    the source could be the filesystem or any connection that provides a way to get
    an audio signal
    """

    def __init__(self):
        AudioSignal.__init__(self)

    def open(self, filepath):
        """
        open a file audio signal from a given source path
        """
        pass

    def save(self, filepath):
        """
        saves a file audio signal to a given source path
        """
        pass