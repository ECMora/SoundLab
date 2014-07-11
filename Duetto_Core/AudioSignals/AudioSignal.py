# -*- coding: utf-8 -*-
from PyQt4.QtGui import QMessageBox
import pyaudio
import numpy as np
from math import *
from Duetto_Core.AudioSignals.SplitArray import SplitArray


class AudioSignal(object):
    """an abstract class for the representation of an audio signal"""
    PLAYING, PAUSED, STOPPED, RECORDING = range(4)

    def __init__(self):
        self.samplingRate = 44100
        self.channels = 1
        self._currentChannel = 0
        self.data = np.array([])
        self.channelData = [self.data]
        self.bitDepth = 1
        self.name = ""
        self.stream = None
        self.playAudio = pyaudio.PyAudio()
        self.playStatus = self.STOPPED
        self.playSection = (0, 0, 0)  # (init,end,current)
        self.recordNotifier = None
        self.playNotifier = None

    def _get_data(self):
        return self._data if not self._padded else self._data[4096:-4096]

    def _set_data(self, data):
        self._data = data
        self._padded = False

    data = property(_get_data, _set_data)

    def pad(self):
        z = np.zeros(4096)
        self._data = np.concatenate((z, self._data, z))
        self._padded = True

    def generateWhiteNoise(self, duration=1, begin_at=0):
        wn = np.array([np.random.uniform(self.getMinimumValueAllowed(),self.getMaximumValueAllowed()) for i in
                       range(duration * self.samplingRate / 1000)],self.data.dtype)
        self.data = np.concatenate((self.data[0:begin_at], wn, self.data[begin_at:]))

    def openNew(self, samplingRate, duration, bitDepth, whiteNoise):
        self.samplingRate = samplingRate
        self.bitDepth = bitDepth
        if whiteNoise:
            self.data = np.array(
                [np.random.uniform(-(1 << (self.bitDepth - 1)), (1 << (self.bitDepth - 1)) - 1) for i in
                 range(int(duration * self.samplingRate))], np.dtype('int' + str(bitDepth)))
        else:
            s = 'int' + str(bitDepth)
            dt = np.dtype(s)
            self.data = np.zeros(samplingRate * duration, dt)
        self.name = "(new)"

    def set_currentChannel(self, channel):
        if not 0 <= channel <= self.channels:
            raise ValueError('Trying to set channel to %d but the signal only contains %d channels'
                             % (channel, self.channels))
        self._currentChannel = channel
        self.data = self.channelData[channel]

    def get_currentChannel(self):
        return self._currentChannel

    currentChannel = property(get_currentChannel, set_currentChannel)

    def resampling(self, samplinRate=44100):
        samplinRate = int(samplinRate)
        frac = samplinRate * 1. / self.samplingRate
        if abs(1./frac - 1) < 0.001:
            return

        n = int(ceil(log(len(self.data),2)))
        n = 2**n
        data_frec=np.fft.fft(self.data,n)
        if frac < 1:
            #down
            indexFrecuency=(n * 1.0)/self.samplingRate
            Fc=int(samplinRate*indexFrecuency/2)
            data_frec = np.concatenate((data_frec[:Fc],data_frec[-Fc:]))
        else:
            #up
            data_frec = np.concatenate((data_frec[:n/2],np.zeros(int(n*(frac-1))),data_frec[n/2:]))


        self.data = np.array(np.real(np.fft.ifft(data_frec)[:int(len(self.data)*frac)]),self.data.dtype)
        self.samplingRate = samplinRate

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

    #def _recordCallback(self, in_data, frame_count, time_info, status):
    #    if self.playStatus != self.RECORDING:
    #        return None, pyaudio.paAbort
    #    self._concatToData(np.fromstring(in_data, dtype=self.data.dtype))
    #    self.playSection = (0, len(self.data), len(self.data))
    #    if self.recordNotifier:
    #        self.recordNotifier(frame_count)
    #
    #    return None, pyaudio.paContinue

    def readFromStream(self):
        self._concatToData(np.fromstring(self.stream.read(self.stream.get_read_available()), dtype=self.data.dtype))
        self.playSection = (0, len(self.data), len(self.data))

    def _concatToData(self, x):
        if isinstance(self.data, SplitArray):
            self.data.extend(x)
        else:
            self.data = np.concatenate((self.data, x))

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
            self.readFromStream()
            self.stream.stop_stream()
            self.stream.close()
        self.playAudio.terminate()
        self.playAudio = pyaudio.PyAudio()
        self.stream = None

        if isinstance(self.data, SplitArray):
            self.data = self.data.to_ndarray()

    def pause(self):
        self.playStatus = self.PAUSED
        if self.stream is not None:
            self.stream.stop_stream()

    def record(self, speed=100):
        if self.playAudio.get_device_count() == 0:
            QMessageBox.critical(QMessageBox(), "Error", "No output devices to play the file.")
            return
        if self.playStatus == self.PLAYING or self.playAudio == self.PAUSED:
            self.stop()
            #ask for concatenate to the current file or make a new one

        #self.data = np.array([], dtype=self.data.dtype)
        self.data = SplitArray(dtype=self.data.dtype)

        #self.samplingRate = 44100
        #self.bitDepth = 16
        self.playSection = 0, 0, 0

        self.playStatus = self.RECORDING

        formatt = {8: pyaudio.paInt8, 16: pyaudio.paInt16, 24: pyaudio.paInt24, 32: pyaudio.paInt32}[self.bitDepth]
        self.stream = self.playAudio.open(format=formatt,
                                          channels=self.channels,
                                          rate=int(self.samplingRate * speed / 100.0),
                                          frames_per_buffer=1024,
                                          input=True)

    def toWav(self):
        raise NotImplemented

    def getDeviceIndex(self, output=False):
        for i in range(self.playAudio.get_device_count()):
            if (output and self.playAudio.get_device_info_by_index(i)["maxInputChannels"] > 0) or \
                    (not output and self.playAudio.get_device_info_by_index(i)["maxOutputChannels"] > 0):
                return i

        raise Exception("No index found")

