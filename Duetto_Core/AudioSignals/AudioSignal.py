from PyQt4.phonon import *


class AudioSignal:
    """an abstract class for the representation of an audio signal"""

    def __init__(self):
        self.samplingRate=0
        self.data=[]
        self.bitDepth=0
        self.path=""
        self.AudioPlayer = None




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


