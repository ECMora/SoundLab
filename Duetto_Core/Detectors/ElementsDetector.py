from numpy import mean
from Duetto_Core.Cursors.IntervalCursor import IntervalCursor
from Duetto_Core.Detectors.Detector import Detector
from Duetto_Core.SignalProcessors.SignalProcessor import SignalProcessor

class ElementDetector(Detector):
    def __init__(self):
        Detector.__init__(self)

    def detect(self,signal,indexFrom=0,indexTo=-1):
        """
       identify the elements in the signal.

       """
        if(indexTo==-1):
            indexTo=len(signal.data)
        begin=0