from string import rfind
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QMessageBox
import pyaudio
import numpy as np


class AudioSignal:
    """an abstract class for the representation of an audio signal"""
    PLAYING, PAUSED, STOPPED, RECORDING = range(4)

    def __init__(self):
        self.samplingRate = 0
        self.channels = 1
        self._currentChannel = 0
        self.data = np.array([])
        self.channelData = [self.data]
        self.bitDepth = 0
        self.path = ""
        #self.media = 0  # mean value of the signal
        self.stream = None
        self.playAudio = pyaudio.PyAudio()
        self.playStatus = self.STOPPED
        self.playSpeed = 100  # percent of the speed
        self.playSection = (0, 0, 0)  # (init,end,current)
        self.recordNotifier = None
        self.playNotifier = None

    def generateWhiteNoise(self, duration=1, begin_at=0):
        wn = np.array([np.random.uniform(-2 ** (self.bitDepth - 1), 2 ** self.bitDepth - 1) for i in
                       range(duration * self.samplingRate / 1000)])
        self.data = np.concatenate((self.data[0:begin_at], wn, self.data[begin_at:]))

    def openNew(self, samplingRate, duration, bitDepth, whiteNoise):
        self.samplingRate = samplingRate
        self.bitDepth = bitDepth
        if whiteNoise:
            self.data = np.array(
                [np.random.uniform(-(1 << (self.bitDepth - 1)), (1 << (self.bitDepth - 1)) - 1) for i in
                 range(int(duration * self.samplingRate))], np.dtype('int' + str(bitDepth)))
        else:
            self.data = np.zeros(samplingRate * duration, np.dtype('int' + str(bitDepth)))

    def name(self):
        if len(self.path) > 0:
            x = rfind(str(self.path), "\\")
            y = rfind(str(self.path), "/")
            index = max(x, y)

            pointindex= rfind(str(self.path), ".")
            pointindex = len(self.path) if pointindex == -1 else pointindex
            if index > 0 and pointindex-index>1:
                return self.path[index + 1:pointindex]
            else:
                return ""

    def set_currentChannel(self, channel):
        if not 0 <= channel <= self.channels:
            raise ValueError('Trying to set channel to %d but the signal only contains %d channels'
                             % (channel, self.channels))
        self._currentChannel = channel
        self.data = self.channelData[channel]
<<<<<<< HEAD

    def get_currentChannel(self):
        return self._currentChannel

    currentChannel = property(get_currentChannel, set_currentChannel)

    def resampling(self, samplinRate=44100):
        samplinRate = int(samplinRate)
        frac = self.samplingRate * 1. / samplinRate
        if abs(frac - 1) < 0.001:
            return
        if frac > 1:
            #down sampling
            from Duetto_Core.SignalProcessors.FilterSignalProcessor import FilterSignalProcessor, FILTER_TYPE

            f = FilterSignalProcessor(self)
            self.data = f.filter(filterType=FILTER_TYPE().LOW_PASS, Fc=samplinRate / 2).data
            self.data = np.array(
                self.data[[int(round(index * frac)) for index in range(int(np.floor(len(self.data) / frac)))]])
        else:
            # up
            arr = np.array([self.interpolate(i, frac) for i in range(int(round(len(self.data) / frac)))])
            self.data = arr

        self.samplingRate = samplinRate

    def interpolate(self, index, frac):
        """
        returns a interpolated new value corresponding to the index position
        in the new resampled array of data with frac fraction of resampling
        """
        if index == 0:
            return self.data[0]
        current_low_index, current_high_index = int(np.floor(index * frac)), int(np.ceil(index * frac))
        if current_low_index == len(self.data) - 1:
            return self.data[-1]
        y0, y1 = self.data[current_low_index], self.data[current_high_index]
        return y0 + (index * frac - current_low_index) * (y1 - y0)

    def currentPlayingFrame(self):
        return self.playSection[2]

    def removeDCOffset(self):
        if len(self.data) == 0:
            return
        if self.data.dtype.str[1] == 'u':
            self.data = (self.data - (1 << (self.data.dtype.itemsize * 8 - 1))) \
                .astype(self.data.dtype.str.replace('u', 'i'))

    def getMinimumValueAllowed(self):
        return -(1 << (self.data.dtype.itemsize * 8 - 1))

    def getMaximumValueAllowed(self):
        return (1 << (self.data.dtype.itemsize * 8 - 1)) - 1

    def generatePinkNoise(self, duration=1, begin_at=0):
        #generates common signals
        pass

    def _playCallback(self, in_data, frame_count, time_info, status):
        if self.playStatus != self.PLAYING:
            return None, pyaudio.paAbort

        if self.playSection[1] - self.playSection[2] < frame_count:
            data = self.data[self.playSection[2]: self.playSection[1]]
            self.playSection = self.playSection[0], self.playSection[1], self.playSection[1]
            if self.playNotifier:
                self.playNotifier(self.currentPlayingFrame())
            self.playSection = (0, 0, 0)
            self.playStatus = self.STOPPED
            return data, pyaudio.paComplete

        data = self.data[self.playSection[2]: self.playSection[2] + frame_count]
        self.playSection = (self.playSection[0], self.playSection[1], self.playSection[2] + frame_count)
        if self.playNotifier:
            self.playNotifier(self.currentPlayingFrame())
        return data, pyaudio.paContinue

    def _recordCallback(self, in_data, frame_count, time_info, status):
        if self.playStatus != self.RECORDING:
            return None, pyaudio.paAbort

        self.data = np.concatenate((self.data, np.fromstring(in_data, dtype=self.data.dtype)))
        self.playSection = (0, len(self.data), len(self.data))
        if self.recordNotifier:
            self.recordNotifier(frame_count)

        return None, pyaudio.paContinue

    def opened(self):
        return len(self.data) > 0

    def play(self, startIndex=0, endIndex=-1, speed=100):
        if self.playAudio.get_device_count() == 0:
            QMessageBox.warning(QMessageBox(), "Error", "No output devices to play the file.")
            return
        if self.playStatus == self.PLAYING:
            return
        if self.playStatus == self.PAUSED:
            if self.stream is not None:
                self.stream.start_stream()
            self.playStatus = self.PLAYING
            return

        endIndex = endIndex if endIndex != -1 else len(self.data)
        self.playSection = startIndex, endIndex, startIndex

        self.playStatus = self.PLAYING

        formatt = {8: pyaudio.paInt8, 16: pyaudio.paInt16, 24: pyaudio.paInt24, 32: pyaudio.paInt32}[self.bitDepth]
        self.stream = self.playAudio.open(format=formatt,
                                          channels=self.channels,
                                          rate=int(self.samplingRate * speed / 100.0),
                                          output=True,
                                          stream_callback=self._playCallback)

    def stop(self):
        self.playStatus = self.STOPPED
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.playAudio.terminate()
        self.playAudio = pyaudio.PyAudio()
        self.stream = None

    def pause(self):
        self.playStatus = self.PAUSED
        if self.stream is not None:
            self.stream.stop_stream()

    def record(self, speed=100):
        if self.playAudio.get_device_count() == 0:
            QMessageBox.warning(QMessageBox(), "Error", "No output devices to play the file.")
            return
        if self.playStatus == self.PLAYING or self.playAudio == self.PAUSED:
            self.stop()
            #ask for concatenate to the current file or make a new one
        self.data = np.array([], dtype=self.data.dtype)
        #self.samplingRate = 44100
        #self.bitDepth = 16
        self.playSection = 0, 0, 0

        self.playStatus = self.RECORDING

        formatt = {8: pyaudio.paInt8, 16: pyaudio.paInt16, 24: pyaudio.paInt24, 32: pyaudio.paInt32}[self.bitDepth]
        self.stream = self.playAudio.open(format=formatt,
                                          channels=self.channels,
                                          rate=int(self.samplingRate * speed / 100.0),
                                          input=True,
                                          stream_callback=self._recordCallback)

    def toWav(self):
        raise NotImplemented

    def getDeviceIndex(self, output=False):
        for i in range(self.playAudio.get_device_count()):
            if (output and self.playAudio.get_device_info_by_index(i)["maxInputChannels"] > 0) or \
                    (not output and self.playAudio.get_device_info_by_index(i)["maxOutputChannels"] > 0):
                return i
        raise Exception("No index found")

