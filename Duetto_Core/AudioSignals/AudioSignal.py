import wave
from PyQt4.QtCore import QTimer

import numpy
from numpy.numarray import fromstring
import pyaudio
from PyQt4.QtCore import QTimer


class AudioSignal:
    """an abstract class for the representation of an audio signal"""
    PLAYING, PAUSED, STOPPED = range(3)
    NUM_SAMPLES = 1024

    def __init__(self):
        self.samplingRate = 0
        self.data = numpy.array([])
        self.bitDepth = 0
        self.path = ""
        self.playStatus = self.STOPPED
        self.playAudio = pyaudio.PyAudio()
        self.playSection = (0, 0, 0)#(init,end,current)
        self.tick = 1000#1 sec interval for player update
        self.timer = QTimer()
        self.stream = None


    def currentPlayingTime(self):
        return self.playSection[2]


    def callback(self):
        """PLay callback"""

        def function(in_data, frame_count, time_info, status):
            if (self.playSection[1] - self.playSection[2] < frame_count):
                frame = self.playSection[2]
                self.playSection = (0, 0, 0)
                self.playStatus = self.STOPPED
                return (self.data[frame:frame + frame_count], pyaudio.paComplete)
            data = self.data[self.playSection[2]:self.playSection[2] + frame_count]
            self.playSection = (self.playSection[0], self.playSection[1], self.playSection[2] + frame_count)
            return (data, pyaudio.paContinue)

        return function

    def recordCallback(self):
        self.stream = self.playAudio.open(format=pyaudio.paInt16, channels=1, rate=44100,
                                          input=True, frames_per_buffer=self.NUM_SAMPLES)
        self.data = numpy.concatenate((self.data, fromstring(self.stream.read(self.NUM_SAMPLES), dtype=numpy.int16)))

    def setTickInterval(self, ms):
        self.tick = ms if ms >= 0 else 0


    def opened(self):
        return len(self.data) > 0

    def play(self, startIndex=0, endIndex=-1, speed=1):
        pass

    def stop(self):
        self.timer.stop()

    def pause(self):
        pass


    def record(self):

        self.data = numpy.array([], dtype=numpy.int16)
        self.timer.timeout.connect(self.recordCallback)
        self.samplingRate=44100
        self.bitDepth=16
        self.timer.start(20)




    def toWav(self):
        raise NotImplemented


