from numpy import array,zeros,concatenate
from Duetto_Core.AudioSignals.WavFileSignal import WavFileSignal
from Duetto_Core.Detectors.MaxMinPeakDetector import MaxMinPeakDetector
from Duetto_Core.Detectors.MeanDetector import MeanDetector
from math import sin,cos,pi
from Duetto_Core.SignalProcessors.SignalProcessor import SignalProcessor

class CommonSignalProcessor(SignalProcessor):
    mean=None
    def __init__(self,signal=WavFileSignal()):
        SignalProcessor.__init__(self,signal)

    def normalize(self,indexFrom=0,indexTo=-1,interval=(-1,1)):
        """
        normalize the signal in a specific interval
        interval is a tuple (a,b) with the  limits of the interval. Are [-1,1] by default
        """
        if(indexTo==-1):
            indexTo=len(self.signal.data)
        self.signal.data=array(self.signal.data,float)
        max,_,min,_=MaxMinPeakDetector().maxMinPeaks(self.signal,indexFrom,indexTo)
        amplitude=1.0*abs(max-min)
        for i in range(indexFrom,indexTo):
            self.signal.data[i]=interval[0]+(interval[1]-interval[0])*(abs(self.signal.data[i]-min)/amplitude)
        return self.signal

    def setSilence(self, indexFrom=0, indexTo=-1):
        """
        Clear the signal in the specified interval.
        indexFrom indexTo  the indexes for the interval.
        indexFrom is the beginning and  indexTo is the end of the interval
        by default are indexFrom=0, indexTo=-1
        """
        if(indexTo==-1):
            indexTo=len(self.signal.data)
        self.checkIndexes(indexFrom,indexTo)
        if(self.mean==None):
            detector=MeanDetector()
            detector.detect(self.signal)
            self.mean=detector.pointers[0].index
        self.signal.data[indexFrom:indexTo] = self.mean
        return self.signal

    def reverse(self,indexFrom,indexTo=-1):
        """
        reverse the signal in the interval [indexFrom,indexTo]
         Example:
         data=[1,2,3,4,5]
         reverse data
         data=[5,4,3,2,1]
        """
        if(indexTo==-1):
            indexTo=len(self.signal.data)
        self.checkIndexes(indexFrom,indexTo)
        data=self.signal.data[indexFrom:indexTo]
        self.signal.data[indexFrom:indexTo]=data[::-1]
        return self.signal

    def insertSilence(self, indexFrom=0,indexTo=-1, ms=0):
        if(self.mean==None):
            detector=MeanDetector()
            detector.detect(self.signal)
            self.mean=detector.pointers[0].index
        arr=zeros(ms*self.signal.samplingRate/1000,type(self.signal.data[0]))
        if(self.mean!=0):
            arr.fill(self.mean)
        self.signal.data=concatenate((self.signal.data[0:indexFrom],
                                      arr,
                                      self.signal.data[indexFrom:]))
        return self.signal

    def scale(self,indexFrom=0,indexTo=-1,factor=100,function="const",fade="IN"):
        n=indexTo-indexFrom if(indexTo!=-1) else len(self.signal.data)-indexFrom
        def f(index):
            if(function=="normalize"):
                return factor/100.0
            elif(function=="linear"):
                 if(fade=="OUT"):
                     return 1-(index*1.0)/n
                 elif(fade=="IN"):
                     return (index*1.0)/n
            elif(function=="sin"):
                 if(fade=="OUT"):
                     return sin((index*1.0*pi)/(n*2)+pi/2)
                 elif(fade=="IN"):
                     return sin((index*1.0*pi)/(n*2))
            elif(function=="cuadratic"):
                if(fade=="OUT"):
                    return (index*1.0/n)**2
                elif(fade=="IN"):
                    return (1-(index*1.0)/n)**2
        if(function=="const"):
            self.signal.data[indexFrom:indexTo]=factor
        else:
            self.signal.data[indexFrom:indexTo] = [self.signal.data[indexFrom+index]*f(index) for index in range(n)]
        return self.signal
