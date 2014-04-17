from PyQt4.QtCore import pyqtSignal
from numpy import *
import matplotlib.mlab as mlab
from Duetto_Core.Segmentation.Detectors.ElementsDetectors.ElementsDetector import ElementsDetector
from Duetto_Core.SignalProcessors.SignalProcessor import envelope

from Duetto_Core.Segmentation.Elements.OneDimensionalElement import OscilogramElement


class OneDimensionalElementsDetector(ElementsDetector):
    #progress = pyqtSignal(int)

    def __init__(self,progress=None):
        ElementsDetector.__init__(self)
        self.oscilogram_elements_detector = self.one_dimensional_elements_detector
        self.threshold = 20
        self.progress = progress
        self.envelope = array([])

    def detect(self,signal, indexFrom=0, indexTo=-1, threshold=0, decay=1,minSize=0,softfactor = 5,merge_factor=0,secondThreshold=0,
               threshold_spectral=95, pxx=[], freqs=[], bins=[], minsize_spectral=(0, 0),location = None,progress=None,findSpectralSublements = False,overlap=0):
            """
            decay in ms to prevent locals falls, should be as long as the min size of the separation between
            elements
            softfactor points to make a moving average in data
            merge_factor in ms
            threshold in dB from the max value
            """
            if progress is not None:
                self.progress = progress
            if(signal is None):
                return
            if indexTo == -1:
                indexTo = len(signal.data)
            decay = int(decay*signal.samplingRate/1000)  #salto para evitar caidas locales
            if abs(threshold) < 0.01:  # to prevent numeric errors
                threshold = mean(signal.data[indexFrom : indexTo])/2
                self.threshold = 20*log10(threshold*1000.0/(2**signal.bitDepth))
            else:
                #translate the threshold from dB scale to V value
                #maxThreshold is 60 when you simplify --> 20*log10((2**signal.bitDepth)*1000.0/(2**signal.bitDepth))
                threshold = (10.0**((60-threshold)/20.0))*(2**signal.bitDepth)/1000.0
            if secondThreshold > 0:
                secondThreshold = (10.0**((60-secondThreshold)/20.0))*(2**signal.bitDepth)/1000.0
            if merge_factor != 0:
                merge_factor = merge_factor*signal.samplingRate/1000.0
            if minSize != 0:
                minSize = minSize*signal.samplingRate/1000.0
            if progress is not None:
                self.progress(2)
            if findSpectralSublements:
                threshold_spectral = percentile(pxx,threshold_spectral)

            if progress is not None:
                self.progress(5)

            elems = self.one_dimensional_elements_detector(signal.data[indexFrom : indexTo],threshold, minSize=minSize, decay=decay, softfactor=softfactor, merge_factor=merge_factor,secondThreshold=secondThreshold)
            #print(len(elems)+str("LENNNNN"))
            l = len(elems)
            progress_size = l/10 if l > 10 else 3
            stepsize = 50/(10 if l > 10 else 3)
            self.oneDimensionalElements = [None for _ in elems]
            for i,c in enumerate(elems):
                self.oneDimensionalElements[i] = OscilogramElement(signal,c[0], c[1],number=i+1,threshold_spectral= threshold_spectral, pxx=pxx, freqs=freqs, bins=bins, minsize_spectral=minsize_spectral,location=location,findSpectralSublements = findSpectralSublements,overlap=overlap)
                 #descartar elemento si no posee informacion espectral suficiente
                if progress is not None and i % progress_size == 0:
                    self.progress(40 + (i/progress_size)*stepsize)

    def one_dimensional_elements_detector(self, data,threshold=0, minSize=1, decay=1, softfactor=10, merge_factor=0,secondThreshold=0):
        """
        data is a numpy array
        minSize is the min amplitude of an element
        merge_factor is the % of separation between 2 elements that is assumed as one (merge the 2 into one)
        """
        self.envelope = envelope(data, decay=decay, progress = self.progress, position= (5,15))
        if self.progress is not None:
            self.progress(16)

        #make a moving average in data to soft rising edges
        self.envelope = array([mean(self.envelope[i-softfactor:i]) for i,_ in enumerate(self.envelope, start=softfactor)])
        
        regions = mlab.contiguous_regions(self.envelope > threshold)
        if self.progress is not None:
            self.progress(20)
        if secondThreshold > 0:
            for i in range(len(regions)):
                left = mlab.cross_from_above(self.envelope[regions[i][0]:(0 if i == 0 else regions[i-1][1]):-1], secondThreshold)
                left = 0 if len(left) == 0 else left[0]
                rigth = mlab.cross_from_above(self.envelope[regions[i][1]:(-1 if i == len(regions)-1 else regions[i+1][0]-1)], secondThreshold)
                rigth = 0 if len(rigth) == 0 else rigth[0]
                regions[i] = (regions[i][0]-left,regions[i][1]+rigth)
        if self.progress is not None:
            self.progress(30)
        if merge_factor > 0:
            regions = self.mergeIntervals(regions, merge_factor)
        if self.progress is not None:
            self.progress(38)
        regions = [c for c in regions if (c[1]-c[0]) > minSize]
        if self.progress is not None:
            self.progress(40)
        return regions

