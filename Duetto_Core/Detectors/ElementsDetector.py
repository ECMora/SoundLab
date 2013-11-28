from numpy import mean
from Duetto_Core.AudioSignals.WavFileSignal import WavFileSignal
from Duetto_Core.Cursors.IntervalCursor import IntervalCursor
from Duetto_Core.Detectors.Detector import Detector
from Duetto_Core.SignalProcessors.SignalProcessor import SignalProcessor

class ElementDetector(Detector):
    def __init__(self):
        Detector.__init__(self)
        self.NOISE_MERGE_FACTOR=1/50.0
        self.MIN_INTERVAL=0

    def detect(self,signal,indexFrom=0,indexTo=-1,threshold=50,type="simple"):
        if("minInterval" == type):
            self.minIntervalDetect(signal,indexFrom,indexTo,threshold)
        elif("mergedIntervals" == type):
            self.mergedIntervals(signal,indexFrom,indexTo,threshold)
        else:
            self.MIN_INTERVAL=0
            self.minIntervalDetect(signal,indexFrom,indexTo,threshold)

    def minIntervalDetect(self,signal,indexFrom=0,indexTo=-1,threshold=50):
        """
        identify the elements in the signal.
        minInterval float in ms of the min interval for detected call
       """
        if(indexTo==-1):
            indexTo=len(signal.data)

        begin=-1#the index of the start of an element
        i=indexFrom
        minInterval=self.MIN_INTERVAL*signal.samplingRate/1000.0

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
                #all the calls has at least ms size
                self.intervals.append(IntervalCursor(begin,i))
                begin=-1
            if(i+1<indexTo):
                monotonyAscending=currentMaxPeak<abs(signal.data[i+1])
            i+=1
        if(begin!=-1):
            self.intervals.append(IntervalCursor(begin,i))

    def mergedIntervals(self,signal,indexFrom=0,indexTo=-1,threshold=50):
        aux=self.MIN_INTERVAL
        self.MIN_INTERVAL=0
        self.minIntervalDetect(signal,indexFrom,indexTo,threshold)
        self.MIN_INTERVAL=1
        newIntervals=[]
        if(len(self.intervals)==0):
            return
        current=self.intervals[0]
        i=1
        length=len(self.intervals)
        msSize=self.MIN_INTERVAL*signal.samplingRate/1000


        while(i<length):
            while(i<length and self.intervals[i].min-current.max<self.NOISE_MERGE_FACTOR*(self.intervals[i].max-self.intervals[i].min)):
                current.max=self.intervals[i].max
                i+=1
            if(i<length):
                newIntervals.append(current)
                current=self.intervals[i]
                i+=1
        newIntervals.append(current)
        self.intervals=[x for x in newIntervals if(x.max-x.min>msSize)]





#data=[1,2,5,9,10,12,15,12,8,2,5,8,15,10,8,9,8,8,7,6,5,4,2,1]
#a=ElementDetector()
#signal=WavFileSignal()
#signal.data=data
#a.minIntervalDetect(signal,threshold=5,minInterval=0)
#for c in  a.intervals:
#    print(" min "+str(c.min)+" max "+str(c.max))
