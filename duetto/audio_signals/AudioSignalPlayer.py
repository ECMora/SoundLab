from PyQt4.QtCore import pyqtSignal, QObject
from duetto.sound_devices.Device import Device
from duetto.audio_signals import AudioSignal
import pyaudio
from duetto.sound_devices.PyAudioDevice import PyAudioDevice
import numpy as np
from duetto.audio_signals.SplitArray import SplitArray


class UnavailableAudioDeviceException(Exception):
    """
    Exception raised when an audio device is currently unavailable
    """
    def __init__(self,message=""):
        Exception.__init__(self,message)


class AudioSignalPlayer(QObject):
    """
    Class that handles a signal for reproduction options.
    Manages the reproduction status (play,stop,pause,record) for a signal
    and provides methods
    """
    #  the four states in which a signal reproduction can be
    PLAYING, PAUSED, STOPPED, RECORDING = range(4)

    #  signal that it's raised when the audio is been played
    #  raise the last index of the data array that was played
    playing = pyqtSignal(int)
    playingDone = pyqtSignal()

    #  The formats of reproduction for pyaudio.
    #  must be the same of the bit depth in the AudioSignal
    valid_formats = {8: pyaudio.paInt8, 16: pyaudio.paInt16, 24: pyaudio.paInt24, 32: pyaudio.paInt32}

    def __init__(self, signal, inputDevice=None, outputDevice=None):
        QObject.__init__(self)

        self.signal = signal

        # play audio variables for record and reproduction.
        # the reproduction is made using the PyAudio module
        self.stream = None
        self.playAudio = pyaudio.PyAudio()

        #  variable that allow to play in loops or not
        self._playLoop = False

        # the audio device from input and output
        # that would be used for play and record
        self._inputDevice = None
        self._outputDevice = None

        # the reproduction status of the signal
        self.playStatus = self.STOPPED

        # the section that is currently been played
        # (init,end,current) in the signal data array indices
        # init the initial index on the signal data array that the user wants to play
        self.playSection = {"startIndex":0,"endIndex":0,"currentIndex":0}

    # region Audio Devices
    @property
    def inputDevice(self):
        """
        :return: return the current input device
        :raise: UnavailableAudioDeviceException if the input device is not available
        """
        # try to ge the default device for input if no one is selected
        try:
            if self._inputDevice is None:
                default_input_device_info = self.playAudio.get_default_input_device_info()
                self._inputDevice = PyAudioDevice(default_input_device_info)

        except Exception as ex:
            raise UnavailableAudioDeviceException("An exception was raised when default"
                                                  " input device was requested.  "+ex.message)
        # check if the audio device is available
        if not self.audioDeviceAvailable(device=self._inputDevice, input=True):
            raise UnavailableAudioDeviceException("The selected input audio device was unavailable.")
        return self._inputDevice

    @property
    def outputDevice(self):
        """
        :return: the current output device
        :raise: UnavailableAudioDeviceException if the default output device is not available
        """

        # get the default output device if no one is selected
        try:
            if self._outputDevice is None:
                default_output_device_info = self.playAudio.get_default_output_device_info()
                self._outputDevice = PyAudioDevice(default_output_device_info)

        except Exception as ex:
            raise UnavailableAudioDeviceException("An exception was raised when default"
                                                  " ouput device was requested.  " + ex.message)
        # check if the audio device is available
        if not self.audioDeviceAvailable(device=self._outputDevice, output=True):
            raise UnavailableAudioDeviceException("The selected output audio device was unavailable.")

        return self._outputDevice

    @inputDevice.setter
    def inputDevice(self, value):
        """
        Set the current input device to a new one
        :param value: Device instance
        :raise: UnavailableAudioDeviceException if the input device is not available
        """
        # check if the new audio device is available
        if not self.audioDeviceAvailable(device=value, input=True):
            raise UnavailableAudioDeviceException("The selected input audio device was unavailable.")

        self._inputDevice = value

    @outputDevice.setter
    def outputDevice(self, value):
        """
        Set the current output device to a new one
        :param value: Device instance
        :raise: UnavailableAudioDeviceException if the new output device is not available
        """
        # check if the audio device is available
        if not self.audioDeviceAvailable(device=value, output=True):
            raise UnavailableAudioDeviceException("The selected output audio device was unavailable.")

        self._outputDevice = value

    def audioDeviceAvailable(self, device, input=False, output=False):
        """
        Check if there is available input/output audio devices for the current signal.
        :param device: The device to analyze availability. Must be a duetto Device
        :param input: True if the request is for input audio devices
        :param output: True if the request is for output audio devices
        :return: True if there is a device of the requested type (input/output)  false otherwise
        """
        if not isinstance(device, Device):
            raise Exception("'device' parameter must be of type Device.")

        input_request_result = not input
        output_request_result = not output

        # signal parameters to check
        sr = self.signal.samplingRate
        format = self.getPyAudioFormat(self.signal.bitDepth)
        channels = self.signal.channelCount

        if input:
            try:
                input_request_result = self.playAudio. \
                    is_format_supported(rate=sr,
                                        input_format=format,
                                        input_channels=channels,
                                        input_device=device.index)
            except Exception as ex:
                input_request_result = False

        if output:
            try:
                output_request_result = self.playAudio. \
                    is_format_supported(rate=sr,
                                        output_format=format,
                                        output_channels=channels,
                                        output_device=device.index)
            except Exception as ex:
                output_request_result = False

        return input_request_result and output_request_result

    # endregion

    @property
    def playLoop(self):
        return self._playLoop

    @playLoop.setter
    def playLoop(self, value):
        self._playLoop = value

    # region Play

    def play(self, startIndex=0, endIndex=-1, speed=100, device=None):
        """
        Play the Audio Signal in the interval [startIndex : endIndex]
        at speed "speed".
        :param startIndex:
        :param endIndex:
        :param speed: (int) percent of the normal speed (sampling rate samples per second)
        at which the signal would be played
        :raises: UnavailableAudioDeviceException if the supplied device is unavailable or None is supplied
         and  the default output device is not available.
        :return:
        """

        # comment until study of pyaudio 2.8
        # if device is None:
        #     device = self.outputDevice

        # if there is an on going reproduction already for this signal at this handler
        if self.playStatus == self.PLAYING:
            return

        # if the signal is been played but is on pause and must continue
        if self.playStatus == self.PAUSED and self.stream is not None:
            # if the signal was on pause stream must be not None
            self.stream.start_stream()
            self.playStatus = self.PLAYING
            return

        # set the start and end indexes of the playing section
        # noinspection PyPep8Naming
        endIndex = endIndex if endIndex != -1 else self.signal.length

        # TODO check if device could play at the sampling rate and channels and bit...
        self.__setPlayingSectionValues(startIndex, endIndex, startIndex)

        self.playStatus = self.PLAYING

        format = self.getPyAudioFormat(self.signal.bitDepth)

        self.stream = self.playAudio.open(format=format,
                                          channels=self.signal.channelCount,
                                          rate=int(self.signal.samplingRate * speed / 100.0),
                                          output=True,
                                          stream_callback=self._playCallback)
                                          #,output_device_index=device.index)

    def getPyAudioFormat(self,bitDepth):
        if bitDepth not in self.valid_formats:
            raise Exception("Invalid Bit Depth. Must be one of " +
                            str(self.valid_formats.keys())+
                            ". And was: "+str(bitDepth))
        return self.valid_formats[bitDepth]

    def __setPlayingSectionValues(self, startIndex=0, endIndex=0, currentIndex=0):
        """
        Set the values of the playing section variable. all the parameters are indexes of
        the data signal array
        :param startIndex: The start index of the reproduction interval
        :param endIndex: The end index of the reproduction interval
        :param currentIndex: The current index of the reproduction.
         must be lower that end index and greater than start index
        """
        if not (startIndex <= currentIndex <= endIndex):
            raise Exception("Invalid indexes")

        self.playSection["startIndex"] = startIndex
        self.playSection["endIndex"] = endIndex
        self.playSection["currentIndex"] = currentIndex

    def _playCallback(self, in_data, frame_count, time_info, status):
        """
        callback that implements the pyaudio interface for supply reproduction
        data to the audio output device.
        :param in_data:
        :param frame_count:
        :param time_info:
        :param status:
        :return: tuple (x,y)
        x : numpy array with the data to be played
        y : Status of reproduction one of [pyaudio.paAbort, pyaudio.paComplete]
        """
        # if there was a play process and the current status of the hanlder is not PLAYING
        # then the play with pyaudio is stopped
        if self.playStatus != self.PLAYING:
            self.__setPlayingSectionValues(0, 0, 0)
            return None, pyaudio.paAbort

        play_finished = False
        # get the section of signal that must be played now
        # playsection --> (initIndex,endIndex,currentIndex) of playing in
        # signal data array indexes
        if self.playSection["endIndex"] - self.playSection["currentIndex"] < frame_count:
            data = self.signal.data[self.playSection["currentIndex"]:self.playSection["endIndex"]]

            self.__setPlayingSectionValues(startIndex=self.playSection["startIndex"],
                                           endIndex=self.playSection["endIndex"],
                                           currentIndex=self.playSection["endIndex"])
            play_finished = True
        else:
            data = self.signal.data[self.playSection["currentIndex"]: self.playSection["currentIndex"] + frame_count]

            self.__setPlayingSectionValues(startIndex=self.playSection["startIndex"],
                                       endIndex=self.playSection["endIndex"],
                                       currentIndex=self.playSection["currentIndex"] + frame_count)

        self.playing.emit(self.currentPlayingFrame)
        if play_finished:
            if not self._playLoop:
                self.__setPlayingSectionValues(0, 0, 0)
                self.playingDone.emit()
                self.playStatus = self.STOPPED
                return data, pyaudio.paComplete
            else:
                data = np.concatenate((data, np.zeros(frame_count - len(data), dtype=data.dtype)))
                self.resetPlayState()

        return data, pyaudio.paContinue

    def resetPlayState(self):
        """
        Reset the play status of the player to its initial state.
        :return:
        """
        self.__setPlayingSectionValues(startIndex=self.playSection["startIndex"],
                                       endIndex=self.playSection["endIndex"],
                                       currentIndex=self.playSection["startIndex"])

    @property
    def currentPlayingFrame(self):
        """
        :return: Returns the current index of the signal data array that is been playing.
        """
        return self.playSection["currentIndex"]

    # endregion

    # region Record

    def readFromStream(self):
        """
        Reads the data from the input audio device stream into memory.
        :return:
        """
        samples = self.stream.get_read_available()

        # case pyport returns an error code
        if samples > 0:
            # get the data array from stream
            data_array = np.fromstring(self.stream.read(samples), dtype=self.signal.data.dtype)

            # concat into the signal data array
            if isinstance(self.signal.data, SplitArray):
                self.signal.data.extend(data_array)
            else:
                self.signal.data = np.concatenate((self.signal.data, data_array))

        # update the play section
        self.__setPlayingSectionValues(0, self.signal.length, self.signal.length)

    def record(self, speed=100, device=None):
        """
        Starts the record process. The new data would be concatenated at the end of the signal
        :param speed: record speed
        :raises: UnavailableAudioDeviceException if the supplied device is unavailable
        """
        # comment until study of pyaudio 2.8
        # if device is None:
        #     device = self.inputDevice

        # if not self.audioDeviceAvailable(device=device, input=True):
        #     raise Exception("No input devices to record a new file.")

        if self.playStatus == self.PLAYING or self.playAudio == self.PAUSED:
            self.stop()
            # TODO ask for concatenate to the current file or make a new one

        #  use of a data structure for the record processing
        #  is used for optimize the graph of the signal in the user interface just visualizing
        #  the last section recorded and not the entire signal

        #  self.signal.data = SplitArray(dtype=self.signal.data.dtype)

        self.__setPlayingSectionValues(0, 0, 0)

        self.playStatus = self.RECORDING

        format = self.getPyAudioFormat(self.signal.bitDepth)

        self.stream = self.playAudio.open(format=format,
                                          channels=self.signal.channelCount,
                                          rate=int(self.signal.samplingRate * speed / 100.0),
                                          frames_per_buffer=1024,
                                          input=True)
                                          #,input_device_index=device.index)

    # endregion

    def pause(self):
        """
        Pause the signal reproduction
        """
        self.playStatus = self.PAUSED
        if self.stream is not None:
            # stream must be != None except if previous status was STOPPED
            self.stream.stop_stream()

    def stop(self):
        """
        Stop the play of the signal if it's playing. Nothing otherwise
        """
        self.playStatus = self.STOPPED

        # Stream must be None if playstatus == STOPPED
        if self.stream is not None:
            # finish the read from the stream
            self.readFromStream()

            # release the resources from stream
            self.stream.stop_stream()
            self.stream.close()

        # release pyaudio resources from reproduction process
        self.playAudio.terminate()
        self.playAudio = pyaudio.PyAudio()

        # Stream must be None if playstatus == Stopped
        self.stream = None

        if isinstance(self.signal.data, SplitArray):
            self.signal.data = self.signal.data.to_ndarray()