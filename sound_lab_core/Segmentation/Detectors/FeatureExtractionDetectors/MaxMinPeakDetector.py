# -*- coding: utf-8 -*-
from sound_lab_core.Segmentation.Detectors.ElementsDetectors import ElementsDetector


class MaxMinPeakDetector(ElementsDetector):

    def __init__(self):
        ElementsDetector.__init__(self)

    def detect(self,signal,indexFrom=0,indexTo=-1):
        #region MAX MIN PEAKS
        if(indexTo==-1):
            indexTo==len(signal.data)




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
