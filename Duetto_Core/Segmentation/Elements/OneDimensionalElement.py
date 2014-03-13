from .TwoDimensionalElement import TwoDimensionalElement
import numpy as np
from numpy.fft import fft
from .Element import Element



class OneDimensionalElement(Element):
    """
    Represents the minimal piece of information to clasify
    An element is a time and spectral region of the signal that contains a superior energy that the fragment of signal
    near to it
    """
    def __init__(self, signal, indexFrom, indexTo):
        Element.__init__(self, signal)
        self.indexFrom =  indexFrom#index of start of the element
        self.indexTo = indexTo # end of element in ms
        self.listOf2dimelements = []

    def twoDimensionalElements(self):
        #the 2dimensional elements storage in this 1 dimensional element
        #after apply a 2dimensional acoustic transformation to this one dimensional element and detec the 2 dim elements
        #in this transform they are returned
        pass

    def startTime(self):
        return self.indexFrom*1.0/self.signal.samplingRate

    def endTime(self):
        return self.indexTo*1.0/self.signal.samplingRate

    def duration(self):
        """
        returns the len in ms of an element (float)
        """
        return (self.indexTo-self.indexFrom)*1000.0/self.signal.samplingRate


class OscilogramElement(OneDimensionalElement):

    def __init__(self, signal, indexFrom, indexTo):
        OneDimensionalElement.__init__(self,signal,indexFrom,indexTo)
        self.twodimensionalOptions = dict()

    def twoDimensionalElements(self):
        if len(self.listOf2dimelements) == 0:
            #compute the elements
            elements = []
            self.listOf2dimelements = elements
        return self.listOf2dimelements

    def distanceFromStartToMax(self):
        return np.argmax(self.signal.data[self.indexFrom:self.indexTo])

    def peakFreq(self):
        indexFrecuency = self.signal.samplingRate/(self.indexTo-self.indexFrom)*1.0
        maxindex = np.argmax(fft(self.signal.data[self.indexFrom:self.indexTo]))
        return int(round((maxindex)*indexFrecuency))

    def peekToPeek(self):
        return np.ptp(self.signal.data[self.indexFrom:self.indexTo])

    def rms(self):
        """
        computes the root mean square of the signal.
        indexFrom,indexTo the optionally limits of the interval
        """
        n = self.indexTo-self.indexFrom
        globalSum = 0.0
        intervalSum = 0.0
        for i in range(n):
            intervalSum += (self.signal.data[self.indexFrom+i]**2)
            if i % 10 == 0:
                globalSum += intervalSum * 1.0 / n
                intervalSum = 0.0

        globalSum += intervalSum * 1.0 / n
        return np.sqrt(globalSum)