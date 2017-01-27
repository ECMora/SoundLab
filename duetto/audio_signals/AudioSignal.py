#  -*- coding: utf-8 -*-
import math
import numpy as np


class AudioSignal:
    """
    A class for the representation of an audio signal.
    Contains the metadata that defines an audio signal:
     sampling rate,bit depth, channelCount number, signal data etc and
    provides several methods for manipulating the signal.
    """

    def __init__(self, samplingRate=44100, bitDepth=16, channelCount=1, data=None, putInAllChannels=True):
        """
        Creates an Audio Signal. with the supplied parameters
        :param samplingRate: The sampling rate at which this signal was recorded or generated.
        :param bitDepth: The amount of bits of storage for each sample in each channel.
        :param channelCount: The number of channels of the signal.
        :param data: The initial data of the signal. It must be a numpy array of one dimension or None.
        :param putInAllChannels: Whether the initial data specified must be copied in all channels or just in the first
        one. In this last case the other channels are filled with 0's.
        """

        if samplingRate <= 0:
            raise Exception("The sampling rate must be greater than zero.")

        if channelCount <= 0:
            raise Exception("The number of channels must be greater  than zero.")

        #  the sampling Rate of the signal
        self.samplingRate = samplingRate

        #  the bit depth at which the signal was recorded
        self.bitDepth = bitDepth
        dtype = np.dtype('int' + str(bitDepth))
        #  data of samples for channel 0. If putInAllChannels==True then also copy to other channels.
        if data is None:
            data = np.array([], dtype)

        data = np.array(data, dtype)

        # the object of extra data stored on the signal
        self._extraData = ""

        # channelData contains the information of all the channels
        # is a list of numpy arrays, one for each channel
        self.channelData = np.zeros((channelCount, len(data)), dtype)
        self.channelData[0] = data

        if putInAllChannels:
            #  copy the data in all the channels
            for i in range(1, channelCount):
                self.channelData[i] = data.copy()

        self.currentChannelIndex = 0

        # an utility name for signal manipulation
        self.name = "unnamed"

    def __str__(self):
        return "Audio Signal-> Sampling-Rate: {0} Bit-Depth: {1} Channels-Count: {2} Duration: {3}(s)".format(
            str(self.samplingRate), str(self.bitDepth), str(self.channelCount),
            str(len(self) * 1.0 / self.samplingRate))

    def copy(self, indexFrom=0, indexTo=-1):
        """
        Create a copy of the current signal.
        :param indexFrom:
        :param indexTo:
        :return: Audio Signal.
        """
        # noinspection PyPep8Naming
        indexTo = len(self) if indexTo == -1 else indexTo

        if indexFrom < 0 or indexTo < indexFrom or len(self) < indexTo:
            raise IndexError()

        result = AudioSignal(self.samplingRate, self.bitDepth,
                             self.channelCount,data=self.data[indexFrom:indexTo])

        result.name = self.name

        # todo copy in depth the extra data into the new signal
        result.extraData = self.extraData

        return result

    def insert(self, other, indexFrom=0):
        """
        Method that inserts the data from an audio signal into the current signal data at
        the position indexFrom.
        :param other: numpy array with the values of the sound.
        :param indexFrom: the index in data array to insert the new_data
        """
        if not self.__eq__(other):
            raise Exception("The two signals must be similar")

        if indexFrom < 0 or indexFrom > self.length:
            raise IndexError("The index of insertion must be between 0 and " + str(self.length))

        if other.length == 0:
            return

        result = np.zeros((self.channelCount, self.length + other.length), dtype=self.data.dtype)
        for i in range(self.channelCount):
            result[i] = np.insert(self.channelData[i], np.ones(other.length) * indexFrom, other.channelData[i])
        self.channelData = result

    def remove(self, indexFrom, indexTo):
        """
        Remove a section of the signal data
        :param indexFrom: the index in data array of the start of removed section
        :param indexTo: the index in data array of the end of removed section
        :return:
        """
        if not 0 <= indexFrom < self.length or not 0 <= indexTo < self.length or indexTo < indexFrom:
            raise Exception("Index out of signal range")

        if indexFrom == indexTo:
            return

        result = np.zeros((self.channelCount, self.length - (indexTo-indexFrom)), dtype=self.data.dtype)

        for i in range(self.channelCount):
            result[i] = np.concatenate((self.channelData[i][:indexFrom+1], self.channelData[i][indexTo+1:]))

        self.channelData = result

    # region Properties

    @property
    def data(self):
        """
        The data array of the signal. The sound samples.
        :return: numpy array of the currently selected channel data of the signal.
        """
        return self.channelData[self.currentChannelIndex]

    @property
    def extraData(self):
        """
        The array of extra data information stored on the signal.
        """
        return self._extraData

    @extraData.setter
    def extraData(self, value):
        """
        The object of extra data information stored on the signal.
        """
        self._extraData = value

    @property
    def channelCount(self):
        """
        The number of channels of the signal.
        :return: int
        """
        return self.channelData.shape[0]

    @property
    def minimumValue(self):
        """
        :return: The minimum amplitude value that the data array could have.
         That value is directly dependent of the bit depth of the signal
        """
        return -(1 << (self.data.dtype.itemsize * 8 - 1))

    @property
    def maximumValue(self):
        """
        :return: The maximum amplitude value that the data array could have.
         That value is directly dependent of the bit depth of the signal
        """
        return (1 << (self.data.dtype.itemsize * 8 - 1)) - 1

    @property
    def currentChannelIndex(self):
        return self._currentChannelIndex

    @currentChannelIndex.setter
    def currentChannelIndex(self, value):
        """
        Switch between channels
        :param value: int new channel index to switch on.
        """
        if not (0 <= value < self.channelCount):
            raise ValueError
        self._currentChannelIndex = value

    @property
    def duration(self):
        """
        :return : The duration time of the signal
        """
        return len(self.data) * 1. / self.samplingRate

    @property
    def length(self):
        """
        :return: the length of the signal data array
        """
        return self.__len__()

    #  endregion

    #  region Channels Handling

    def update_channel(self, data, channel_index=0):
        """
        Changes the data samples of a channel
        :param data: the new samples for this channel
        :param channel_index: the index of the channel that will be changed
        """

        if channel_index < 0 or channel_index >= self.channelCount:
            raise Exception("The channel_index must be between 0 and " + str(self.channelCount - 1))

        if len(self) != len(data):
            raise Exception("The new data array must have the same size of the old channel")

        self.channelData[channel_index] = np.array(data)

    #  endregion

    #  region Audio Signal Operations

    def __add__(self, other):
        """
        Overload for the + plus operation between audio signals.
        The result of this operation between two audio Signals is it's concatenation.
        This operation requires that the two signals share the same metadata parameters ie
        sampling rate
        bit depth
        and number of channels
        :param other: The other rAudioSignal for the concatenation.
        :return: Audio Signal result of the concatenation
        """
        if not isinstance(other,AudioSignal):
            err = type(other)
            raise Exception("Can't concatenate an audio signal with "+str(err)+". Must be of type AudioSignal")

        if not self.__eq__(other):
            raise Exception("The signals must have similar metadata to be added")

        # performs the creation of a new signal for result
        # copy the arrays of data

        result = self.copy()
        result.channelData = np.concatenate((result.channelData, other.channelData), 1)
        return result

    def __len__(self):
        """
        :return: The count of samples in the signal
        """
        return len(self.data)

    def __eq__(self, audio_signal):
        """
        Compares the metadata of the current signal and the supplied parameter.
        :param audio_signal:
        :raise Exception:
        """
        if audio_signal is None:
            return False

        if not isinstance(audio_signal,AudioSignal):
            raise Exception
        return audio_signal.samplingRate == self.samplingRate and \
            audio_signal.bitDepth == self.bitDepth and \
            audio_signal.channelCount == self.channelCount

    #  endregion

    def resampling(self, samplinRate=44100):
        """
        Method that performs the change of sampling rate in the signal.
        Update the data array for the new sampling rate.
        :param samplinRate: the new sampling rate
        """
        #  TODO: comment and implement correctly this method
        # noinspection PyPep8Naming
        samplinRate = int(samplinRate)
        frac = samplinRate * 1. / self.samplingRate
        if np.abs(1./frac - 1) < 0.001:
            return

        self.samplingRate = samplinRate
        # noinspection PyPep8Naming
        oldLen = len(self)
        # noinspection PyPep8Naming
        newLen = int(oldLen*frac)
        temp = np.zeros((self.channelCount, newLen))
        n = int(math.ceil(math.log(oldLen,2)))
        n = 2**n

        for i in range(self.channelCount):
            data_frec=np.fft.fft(self.channelData[i], n)
            if frac < 1:
                # down
                # noinspection PyPep8Naming
                indexFrecuency=(n * 1.0)/self.samplingRate
                # noinspection PyPep8Naming
                Fc=int(samplinRate*indexFrecuency/2)
                data_frec = np.concatenate((data_frec[:Fc],data_frec[-Fc:]))
            else:
                # up
                data_frec = np.concatenate((data_frec[:n/2],np.zeros(int(n*(frac-1))),data_frec[n/2:]))
            temp[i] = np.array(np.real(np.fft.ifft(data_frec)[:newLen]),self.data.dtype)
        self.channelData = temp

    def getTime(self, i):
        """
        :return : The time that corresponds with the sample i
        """
        return i * 1. / self.samplingRate