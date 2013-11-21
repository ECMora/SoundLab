from numpy import mean
from Duetto_Core.Cursors.IntervalCursor import IntervalCursor
from Duetto_Core.Detectors.Detector import Detector
from Duetto_Core.SignalProcessors.SignalProcessor import SignalProcessor

class ElementDetector(Detector):
    def __init__(self):
        Detector.__init__(self)

    def detect(self,signal,noiseThreshold=100,width=100,indexFrom=0,indexTo=-1):
        """
       identify the elements in the signal.

       """
        if(indexTo==-1):
            indexTo=len(signal.data)
        begin=0

        elem_found=False
        signalprocessor=SignalProcessor(signal)
        for i in range(indexFrom,indexTo):
            if(not elem_found and signalprocessor.envelope(i)> noiseThreshold ):
                #start of the call found
                elem_found=True
                begin=i
            elif(signalprocessor.envelope(i)<=noiseThreshold and elem_found and i-begin >width):
                interval=IntervalCursor()
                interval.min,interval.max=begin,i-1
                self.intervals.append(interval)
                elem_found=False
                begin=0
        if(begin!=0):
            interval=IntervalCursor()
            interval.min,interval.max=begin,len(signal.data)-1
            self.intervals.append(interval)





