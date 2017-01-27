class Device(object):
    """
    This class represents a Duetto device with its corresponding properties
    """

    def __init__(self, name, defaultSamplingRate, maxChannels, defaultLowLatency,
                 defaultHighLatency):
        self._name = name
        self._defaultSamplingRate = defaultSamplingRate
        self._maxChannels = maxChannels
        self._defaultLowLatency = defaultLowLatency
        self._defaultHighLatency = defaultHighLatency

    @property
    def name(self):
        """
        :return: the device name
        """
        return self._name

    @property
    def defaultSamplingRate(self):
        """
        :return: the device sampling rate
        """
        return self._defaultSamplingRate

    @property
    def maxChannels(self):
        """
        :return: the device maximum channels number
        """
        return self._maxChannels

    @property
    def defaultHighLatency(self):
        """
        :return: the device high latency
        """
        return self._defaultHighLatency

    @property
    def defaultLowLatency(self):
        """
        :return: the device low latency
        """
        return self._defaultLowLatency

    def __eq__(self, other):
        return other is None or\
                (isinstance(other, Device) and \
                self.name == other.name and
                self.defaultSamplingRate == other.defaultSamplingRate and
                self.maxChannels == other.maxChannels and
                self.defaultHighLatency == other.defaultHighLatency and
                self.defaultLowLatency == other.defaultLowLatency)

    def __str__(self):
        return self.name + " " + str(self.defaultSamplingRate * 1. / 1000)\
               + " kHz " + str(self.maxChannels) + " channels."