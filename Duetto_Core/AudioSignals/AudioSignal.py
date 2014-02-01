from string import *
from PyQt4.QtGui import QMessageBox,QWidget
import pyaudio
from numpy import *
from numpy.numarray import fromstring
import pyaudio
from PyQt4.QtCore import QTimer, pyqtSignal



class AudioSignal:
    """an abstract class for the representation of an audio signal"""
    PLAYING, PAUSED, STOPPED, RECORDING = range(4)
    NUM_SAMPLES = 1024

    def __init__(self):
        self.samplingRate = 0
        self.channels=1
        self.data = array([])
        self.bitDepth = 0
        self.path = ""
        self.media=0#mean value of the signal
        self.stream=None
        self.playAudio=pyaudio.PyAudio()
        self.playStatus = self.STOPPED
        self.playSpeed = 100  # percent of the speed
        self.playSection = (0, 0, 0)  # (init,end,current)
        self.tick = 50  # msec interval for player update
        self.timer = QTimer()
        self.play_finished = None #the method to call when
        self.timer.timeout.connect(self.recordCallback)

    def generateWhiteNoise(self, duration=1, begin_at=0):
        wn = array([random.uniform(-2**self.bitDepth -1, 2**self.bitDepth-1) for i in range(duration*self.samplingRate/1000)])
        self.data=concatenate((self.data[0:begin_at],wn,self.data[begin_at:]))

    def name(self):
        if len(self.path) > 0:
            x = rfind(str(self.path), "\\")
            y = rfind(str(self.path), "/")
            index = max(x,y)
            if(index>0):
                return self.path[index+1:]
            else:
                return ""

    def resampling(self,  samplinRate= 44100):
        samplinRate = int(samplinRate)
        frac = self.samplingRate*1./samplinRate
        if( abs(frac-1) < 0.001 ):
            return
        if( frac > 1):
            #down sampling
            from Duetto_Core.SignalProcessors.FilterSignalProcessor import FilterSignalProcessor,FILTER_TYPE
            f = FilterSignalProcessor(self)
            self.data = f.filter(filterType=FILTER_TYPE().LOW_PASS,Fc=samplinRate/2).data
            self.data = array(self.data[[int(round(index*frac)) for index in range(int(floor(len(self.data)/frac)))]])
        else:
            # up
            arr = array([self.interpolate(i,frac) for i in range(int(round(len(self.data)/frac)))])
            self.data = arr

        self.samplingRate = samplinRate

    def interpolate(self, index, frac):
        """
        returns a interpolated new value corresponding to the index position
        in the new resampled array of data with frac fraction of resampling
        """
        if(index==0):
            return self.data[0]
        current_low_index , current_high_index = int(floor(index*frac)),int(ceil(index*frac))
        if(current_low_index==len(self.data)-1):
            return self.data[-1]
        y0 , y1 = self.data[current_low_index], self.data[current_high_index]
        return y0+(index*frac - current_low_index)*(y1-y0)

    def currentPlayingTime(self):
        return self.playSection[2]


    def removeDCOffset(self):
        if(len(self.data)==0):
            return
        media = mean(self.data)
        if(abs(media)>0.01):
            self.data -= media


    def generatePinkNoise(self,duration=1, begin_at=0):
        #generates common signals
        pass





    def playCallback(self,in_data, frame_count, time_info, status):
        if (self.playSection[1] - self.playSection[2] < frame_count):
            frame = self.playSection[2]
            self.playSection = (0, 0, 0)
            self.playStatus = self.STOPPED
            data = self.data[frame:frame + frame_count]
            data -= self.media
            if self.play_finished is not None and  callable(self.play_finished):
                self.play_finished()
            return (data, pyaudio.paComplete)
        data = self.data[self.playSection[2]:self.playSection[2] + frame_count]
        self.playSection = (self.playSection[0], self.playSection[1], self.playSection[2] + frame_count)
        return (data, pyaudio.paContinue)



    def recordCallback(self):
        if (self.playStatus == self.RECORDING):
            self.stream = self.playAudio.open(format=pyaudio.paInt16, channels=self.channels, rate=44100,
                                              input=True, frames_per_buffer=self.NUM_SAMPLES)
            self.playSection = (0, len(self.data) + self.NUM_SAMPLES, len(self.data))
            self.data = concatenate(
                (self.data, fromstring(self.stream.read(self.NUM_SAMPLES), dtype=numpy.int16)))

    def setTickInterval(self, ms):
        if (self.playStatus == self.STOPPED or self.playStatus == self.PAUSED):
            self.tick = ms if ms >= 0 else 0

    def opened(self):
        return len(self.data) > 0

    def play(self, startIndex=0, endIndex=-1, speed=100):
        if (self.playAudio.get_device_count() == 0):
            QMessageBox.warning(QMessageBox(), "Error", "No output devices to play the file.")
            return
        if (self.playStatus == self.PLAYING):
            return
        if (self.playStatus == self.PAUSED):
            if (self.stream != None):
                self.stream.start_stream()
            self.playStatus = self.PLAYING
            self.timer.start(self.tick)
            return

        self.media=mean(self.data)
        self.playStatus=self.PLAYING
        formatt=(pyaudio.paInt8 if self.bitDepth==8 else pyaudio.paInt16 if self.bitDepth==16 else pyaudio.paFloat32)
        self.stream =self.playAudio.open(format=formatt,
                            channels=self.channels,
                            rate=self.samplingRate,
                            output=True,
                            start=False,
                            stream_callback=self.playCallback)

        endIndex=endIndex if endIndex!=-1 else len(self.data)
        self.stream._rate=int(self.samplingRate*speed/100.0)
        self.playSection=(startIndex,endIndex,startIndex)

        self.stream.start_stream()
        self.timer.start(self.tick)

    def stop(self):
        self.timer.stop()
        self.playStatus = self.STOPPED
        if (self.stream != None):
            self.stream.stop_stream()
            self.stream.close()
        self.playAudio.terminate()
        self.playAudio = pyaudio.PyAudio()
        self.stream = None

    def pause(self):
        self.timer.stop()
        if (self.stream != None):
            self.stream.stop_stream()
        self.playStatus = self.PAUSED

    def record(self):
        #ask for concatenate to the current file or make a new one
        self.data = array([], dtype=int16)
        self.samplingRate = 44100
        self.bitDepth = 16
        self.playSection = (0, 0, 0)
        self.playStatus = self.RECORDING
        self.timer.start(self.tick)



    def toWav(self):
        raise NotImplemented

    def getDeviceIndex(self, output=False):
        for i in range(self.playAudio.get_device_count()):
            if (output and self.playAudio.get_device_info_by_index(i)["maxInputChannels"] > 0) or \
                    (not output and self.playAudio.get_device_info_by_index(i)["maxOutputChannels"] > 0):
                return i
        raise Exception("No index found")

