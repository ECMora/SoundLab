from numpy import mean
from Duetto_Core.Cursors.IntervalCursor import IntervalCursor
from Duetto_Core.Detectors.Detector import Detector
from Duetto_Core.SignalProcessors.SignalProcessor import SignalProcessor

class ElementDetector(Detector):
    def __init__(self):
        Detector.__init__(self)

    def detect(self,signal,indexFrom=0,indexTo=-1,threshold=50,minInterval=1):
        """
        identify the elements in the signal.
        minInterval float in ms of the detected call
       """
        if(indexTo==-1):
            indexTo=len(signal.data)

        begin=-1#the index of the start of an element
        i=indexFrom
        minInterval=minInterval*signal.samplingRate/1000
        currentMaxPeak=abs(signal.data[i])
        monotonyAscending=currentMaxPeak<abs(signal.data[i+1])
        while(i<indexTo):
            while(i+1<indexTo and ((monotonyAscending and currentMaxPeak<=abs(signal.data[i+1])) or
                  (not monotonyAscending and currentMaxPeak>=abs(signal.data[i+1])))):#get the next peak
                i+=1
                currentMaxPeak=abs(signal.data[i])
            if(begin==-1 and currentMaxPeak>threshold):#found a first point above threshold
                begin=i
            if(begin!=-1 and currentMaxPeak<threshold and monotonyAscending and (i-begin)>minInterval):#the end of a peak
                self.intervals.append(IntervalCursor(begin,i))
                begin=-1
            if(i+1<indexTo):
                monotonyAscending=currentMaxPeak<abs(signal.data[i+1])
            i+=1

