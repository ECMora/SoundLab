from math import floor, ceil
from .TwoDimensionalElement import TwoDimensionalElement
from ..Detectors.ElementsDetectors.TwoDimensionalElementsDetector import TwoDimensionalElementsDetector
import numpy as np
from numpy.fft import fft
import pyqtgraph as pg
from .Element import Element
from PyQt4 import QtGui



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

    def __init__(self, signal, indexFrom, indexTo,number=0,threshold_spectral=0, pxx=[], freqs=[], bins=[], minsize_spectral=(0,0),
               merge_factor_spectral=(1,1)):
        OneDimensionalElement.__init__(self,signal,indexFrom,indexTo)
        text = pg.TextItem(str(number),color=(255,255,255),anchor=(0.5,0.5))
        text.setPos(self.indexFrom/2.0+self.indexTo/2.0, 0.75*2**(signal.bitDepth-1))
        lr = pg.LinearRegionItem([self.indexFrom,self.indexTo], movable=False,brush=(pg.mkBrush(QtGui.QColor(0, 255, 0, 70)) if number%2==0 else pg.mkBrush(QtGui.QColor(0, 0, 255,70))))
        self._peakFreq = False
        self._peekToPeek = False
        self._rms = False
        self.number = number
        self.twoDimensionalElements = []
        if(pxx != [] and bins != [] and freqs != []):
            #spec_resolution, temp_resolution = signal.samplingRate/2.0*len(freqs),bins[1]-bins[0]
            spec_resolution, temp_resolution = 1000.0/freqs[1],(bins[1]-bins[0])*1000.0
            #minsize came with the hz, sec of min size elements and its translated to index values in pxx for comparations
            minsize_spectral = (max(1,int(minsize_spectral[0]*spec_resolution)),max(1,int(minsize_spectral[1]*temp_resolution)))
            sr = signal.samplingRate*1.0
            aux = max(0,int(floor(indexFrom/((bins[1]-bins[0])*sr))-1))
            aux2 = min(int(ceil((indexTo/((bins[1]-bins[0])*sr))+1)),len(pxx[0]))
            matrix = pxx[:,aux:aux2]
            self.indexFromInPxx,self.indexToInPxx = aux,aux2
            self.computeTwoDimensionalElements(threshold_spectral,matrix,freqs,bins,minsize_spectral,merge_factor_spectral)


        tooltip = "<b> Start Time:</b> "+ str(indexFrom*1000.0/signal.samplingRate) + "ms \n" \
                  + "<b color='#99f'>End Time:</b>"+ str(indexTo*1000.0/signal.samplingRate) + "ms \n"\
                  + "<b color='#99f'>RMS: </b>"+ str(self.rms()) + "\n"\
                  + "<b color='#99f'>PeekToPeek: </b>"+ str(self.peekToPeek())
        lr.setToolTip(tooltip)
        self.visualwidgets = [text,lr]


    def computeTwoDimensionalElements(self,threshold_spectral, pxx, freqs, bins, minsize_spectral,merge_factor_spectral):
        detector = TwoDimensionalElementsDetector()
        detector.detect(self.signal,threshold_spectral, pxx,freqs,bins, minsize_spectral,merge_factor_spectral,one_dimensional_parent=self)
        for elem in detector.elements():
            self.twoDimensionalElements.append(elem)

    def distanceFromStartToMax(self):
        return np.argmax(self.signal.data[self.indexFrom:self.indexTo])

    def peakFreq(self):
        if not self._peakFreq:
            indexFrecuency = self.signal.samplingRate/(self.indexTo-self.indexFrom)*1.0
            maxindex = np.argmax(fft(self.signal.data[self.indexFrom:self.indexTo]))
            self._peakFreq = int(round((maxindex)*indexFrecuency))
        return self._peakFreq

    def peekToPeek(self):
        if not self._peekToPeek:
            self._peekToPeek = np.ptp(self.signal.data[self.indexFrom:self.indexTo])
        return self._peekToPeek

    def rms(self):
        """
        computes the root mean square of the signal.
        indexFrom,indexTo the optionally limits of the interval
        """
        if not self._rms:
            n = self.indexTo-self.indexFrom
            globalSum = 0.0
            intervalSum = 0.0
            for i in range(n):
                intervalSum += (self.signal.data[self.indexFrom+i]**2)
                if i % 10 == 0:
                    globalSum += intervalSum * 1.0 / n
                    intervalSum = 0.0

            globalSum += intervalSum * 1.0 / n
            self._rms = np.sqrt(globalSum)
        return self._rms