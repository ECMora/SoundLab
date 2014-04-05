from math import floor, ceil
from Duetto_Core.Segmentation.Detectors.ElementsDetectors.TwoDimensionalElementsDetector import TwoDimensionalElementsDetector
import numpy as np
from numpy.fft import fft
import pyqtgraph as pg
from Duetto_Core.Segmentation.Elements.Element import Element
from PyQt4 import QtGui

class SpectralMeasurementLocation:
    START,CENTER,END,QUARTILE25,QUARTILE75 = range(5)
    MEDITIONS = [
        [True,  QtGui.QColor(255, 0, 0, 255)],
        [True, QtGui.QColor(0, 255, 0, 255)],
        [True,  QtGui.QColor(0, 0, 255, 255)],
        [False, QtGui.QColor(255,255,255, 255)],
        [False,  QtGui.QColor(255, 255, 255, 255)]]
    #(Active computation, color)


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
        self.parameterDecimalPlaces = 4

    def startTime(self):
        #the start time in s
        return round(self.indexFrom*1.0/self.signal.samplingRate,self.parameterDecimalPlaces)

    def endTime(self):
        return round(self.indexTo*1.0/self.signal.samplingRate,self.parameterDecimalPlaces)

    def duration(self):
        """
        returns the len in s of an element (float)
        """
        return round((self.indexTo-self.indexFrom)*1.0/self.signal.samplingRate,self.parameterDecimalPlaces)


class OscilogramElement(OneDimensionalElement):

    def __init__(self, signal, indexFrom, indexTo,number=0,threshold_spectral=0, pxx=[], freqs=[], bins=[], minsize_spectral=(0,0), location = None):
        OneDimensionalElement.__init__(self,signal,indexFrom,indexTo)
        text = pg.TextItem(str(number),color=(255,255,255),anchor=(0.5,0.5))
        text.setPos(self.indexFrom/2.0+self.indexTo/2.0, 0.75*2**(signal.bitDepth-1))
        lr = pg.LinearRegionItem([self.indexFrom,self.indexTo], movable=False,brush=(pg.mkBrush(QtGui.QColor(0, 255, 0, 100)) if number%2==0 else pg.mkBrush(QtGui.QColor(0, 0, 255,100))))
        self.number = number
        self.twoDimensionalElements = []
        #the memoize pattern implemented to compute parameters functions
        self.parameters = dict(StartToMax=None, peekToPeek=None, rms=None, minFreq=None, maxFreq=None, peakFreq=None,peaksAbove=(None,0))
        self.spectralMeasurementLocation = location if location is not None else SpectralMeasurementLocation()
        if(pxx != [] and bins != [] and freqs != []):
            #spec_resolution, temp_resolution = signal.samplingRate/2.0*len(freqs),bins[1]-bins[0]
            spec_resolution, temp_resolution = 1000.0/freqs[1],(bins[1]-bins[0])*1000.0
            #minsize came with the hz, sec of min size elements and its translated to index values in pxx for comparations
            minsize_spectral = (max(1,int(minsize_spectral[0]*spec_resolution)),max(1,int(minsize_spectral[1]*temp_resolution)))
            sr = signal.samplingRate*1.0
            aux = max(0,int(floor((indexFrom-bins[0]*sr)/((bins[1]-bins[0])*sr))))
            aux2 = min(int(ceil((indexTo+bins[0]*sr)/((bins[1]-bins[0])*sr))),len(pxx[0]))
            self.matrix = pxx[:,aux:aux2]
            self.indexFromInPxx,self.indexToInPxx = aux,aux2
            self.computeTwoDimensionalElements(threshold_spectral,self.matrix,freqs,bins,minsize_spectral)


        tooltip = "Element: "+str(self.number)+"\nStart Time: "+ str(self.startTime()) + "s\n" \
                  + "End Time:"+ str(self.endTime()) + "s\n"\
                  + "RMS: "+ str(self.rms()) + "\n"\
                  + "PeekToPeek: "+ str(self.peekToPeek())
        lr.setToolTip(tooltip)
        self.visual_figures.append([lr,True])#item visibility
        self.visual_text.append([text,True])

    def sublementsPeakFreqsVisible(self,visibility=False):
        for x in self.twoDimensionalElements:
            for p in x.visual_peaksfreqs:
                p[1] = visibility
        if not visibility:
            pass


    def computeTwoDimensionalElements(self,threshold_spectral, pxx, freqs, bins, minsize_spectral):
        detector = TwoDimensionalElementsDetector()
        detector.detect(self.signal,threshold_spectral, pxx,freqs,bins, minsize_spectral,one_dimensional_parent=self,location= self.spectralMeasurementLocation)
        for elem in detector.elements():
            self.twoDimensionalElements.append(elem)

    def distanceFromStartToMax(self):
        if(self.parameters["StartToMax"] is None):
            self.parameters["StartToMax"] = round(np.argmax(self.signal.data[self.indexFrom:self.indexTo])*1.0/self.signal.samplingRate,self.parameterDecimalPlaces)
        return self.parameters["StartToMax"]

    def peekToPeek(self):
        if(self.parameters["peekToPeek"] is None):
            self.parameters["peekToPeek"] = round(np.ptp(self.signal.data[self.indexFrom:self.indexTo])*1.0/(2**self.signal.bitDepth),self.parameterDecimalPlaces)
        return self.parameters["peekToPeek"]

    def rms(self):
        """
        computes the root mean square of the signal.
        indexFrom,indexTo the optionally limits of the interval
        """
        if(self.parameters["rms"] is None):
            n = self.indexTo-self.indexFrom
            globalSum = 0.0
            intervalSum = 0.0
            for i in range(n):
                intervalSum += (self.signal.data[self.indexFrom+i]**2)
                if i % 10 == 0:
                    globalSum += intervalSum * 1.0 / n
                    intervalSum = 0.0

            globalSum += intervalSum * 1.0 / n
            self.parameters["rms"] = round(np.sqrt(globalSum)*1.0/(2**self.signal.bitDepth),self.parameterDecimalPlaces)
        return self.parameters["rms"]

    #espectral parameters

    def minFreq(self,location=None):
        if(self.parameters["minFreq"] is None):
            self.parameters["minFreq"] = 0
        return self.parameters["minFreq"]

    def maxFreq(self,location=None):
        if(self.parameters["maxFreq"] is None):
            self.parameters["maxFreq"] = 0
        return self.parameters["maxFreq"]

    def peakFreq(self,location=None):
        if(self.parameters["peakFreq"] is None):
            self.parameters["peakFreq"] = 0
        return self.parameters["peakFreq"]

    def peaksAbove(self,threshold,location=None):
        if(self.parameters["peaksAbove"][0] is None or self.parameters["peaksAbove"][1] != threshold):
            self.parameters["peekToPeek"] = (0,threshold)
        return self.parameters["peekToPeek"][0]

    def spectralElements(self):
        return len(self.twoDimensionalElements)