from PyQt4.QtCore import QTimer
import pyaudio
from PyQt4.QtCore import QTimer

class AudioSignal:
    """an abstract class for the representation of an audio signal"""
    PLAYING,PAUSED,STOPPED=range(3)
    def __init__(self):
        self.samplingRate=0
        self.data=[]
        self.bitDepth=0
        self.path=""
        self.playStatus=self.STOPPED
        self.playAudio = pyaudio.PyAudio()
        self.playSection=(0,0,0)#(init,end,current)
        self.tick=1000#1 sec interval for player update
        self.timer=QTimer()
        self.stream =None
        self.timer.timeout.connect(self.stopTimer)


    def currentPlayingTime(self):
        return self.playSection[2]




    def setTickInterval(self,ms):
        self.tick= ms if ms>=0 else 0

    def stopTimer(self):
        if(self.stream!=None and self.stream.is_stopped()):
            self.timer.stop()
    def opened(self):
        return  len(self.data)>0

    def play(self, startIndex=0, endIndex=-1, speed=1):
        pass
    def stop(self):
       pass
    def pause(self):
        pass


    def toWav(self):
        raise NotImplemented


