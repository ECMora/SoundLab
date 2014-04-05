from Duetto_Core.Cursors.PointerCursor import PointerCursor
from Duetto_Core.Segmentation.Detectors.Detector import Detector


class MaxMinPeakDetector(Detector):

    def __init__(self):
        Detector.__init__(self)

    def detect(self,signal,indexFrom=0,indexTo=-1):
        #region MAX MIN PEAKS
        self.pointer2D=[]
        self.pointer2D.extend([PointerCursor(),PointerCursor()])
        if(indexTo==-1):
            indexTo==len(signal.data)
        _,self.pointer2D[0].index,_,self.pointer2D[1].index=self.maxMinPeaks(signal,indexFrom,indexTo)




        #endregion
    def maxMinPeaks(self,signal,indexFrom=0,indexTo=-1):
        """
        computes the max and min values of the signal
        indexFrom  the index of the signal
                   for the beginning of the search. If no index is given the default value is 0

        indexTo    the end of the interval to found the max and min
                    If no index is given the default value is len(self.signal.data)

        """
        if(indexTo==-1):
            indexTo=len(signal.data)
        max,min,maxIndex,minIndex=0,0,0,0
        for x in range(indexFrom,indexTo):
            if(signal.data[x]>max):
                max=signal.data[x]
                maxIndex=x
            if(signal.data[x]<min):
                min=signal.data[x]
                minIndex=x
        return max,maxIndex,min,minIndex

    def peakToPeak(self,signal,indexFrom=0,indexTo=-1):
        """
        return the max difference between two values in the signal.
        the max amplitude of the signal
        """
        tuple=self.maxMinPeaks(signal,indexFrom,indexTo)
        return tuple[0]-tuple[1]
