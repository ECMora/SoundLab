from duetto.sound_devices.Device import Device

class PyAudioDevice(Device):
    """
    This class is a Device inherited class with pyAudio additional property
    """
    def __init__(self, device_info):

        super(PyAudioDevice, self).__init__(device_info.get('name'),
                                            device_info.get('defaultSampleRate'),
                                            device_info.get('maxInputChannels'),
                                            device_info.get('defaultLowInputLatency'),
                                            device_info.get('defaultHighInputLatency'))

        self._index = device_info.get('index')

    @property
    def index(self):
        """
        The device index.
        :return: integer.
        """
        return self._index

    def __eq__(self, other):
        return Device.__eq__(self, other) and self.index == other.index






