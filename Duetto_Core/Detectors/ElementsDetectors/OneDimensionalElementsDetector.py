from numpy import *
import matplotlib.mlab as mlab
from Duetto_Core.Detectors.Detector import Detector
from Duetto_Core.Detectors.ElementsDetectors.ElementsDetector import ElementsDetector
from Duetto_Core.SignalProcessors.SignalProcessor import envelope
from Duetto_Core.Cursors.IntervalCursor import IntervalCursor
import time


class OneDimensionalElementsDetector(ElementsDetector):

    def __init__(self):
        ElementsDetector.__init__(self)
        self.oscilogram_elements_detector = self.one_dimensional_elements_detector
        self.threshold = 20

    def detect(self,signal, indexFrom=0, indexTo=-1, threshold=0, decay=1,minSize=0,softfactor = 5,merge_factor=0,secondThreshold=0):
            """
            decay in ms to prevent locals falls, should be as long as the min size of the separation between
            elements
            softfactor points to make a moving average in data
            merge_factor in ms
            threshold in dB from the max value
            """
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
            self.intervals = [IntervalCursor(c[0], c[1]) for c in self.one_dimensional_elements_detector(signal.data[indexFrom : indexTo],threshold, minSize=minSize, decay=decay, softfactor=softfactor, merge_factor=merge_factor,secondThreshold=secondThreshold)]

    def one_dimensional_elements_detector(self, data,threshold=0, minSize=1, decay=1, softfactor=10, merge_factor=0,secondThreshold=0):
        """
        data is a numpy array
        minSize is the min amplitude of an element
        merge_factor is the % of separation between 2 elements that is assumed as one (merge the 2 into one)
        """
        soft_data = envelope(data, decay=decay)
        #make a moving average in data to soft rising edges
        soft_data = array([mean(soft_data[i-softfactor:i]) for i,_ in enumerate(soft_data, start=softfactor)])
        max_value_above_umbral = max(soft_data)
        if max_value_above_umbral < threshold:
            threshold = int(threshold*1.1)
        regions = mlab.contiguous_regions(soft_data > threshold)
        if secondThreshold > 0:
            for i in range(len(regions)):
                left = mlab.cross_from_above(soft_data[regions[i][0]:(0 if i == 0 else regions[i-1][1]):-1], secondThreshold)
                left = 0 if len(left) == 0 else left[0]
                rigth = mlab.cross_from_above(soft_data[regions[i][1]:(-1 if i == len(regions)-1 else regions[i+1][0]-1)], secondThreshold)
                rigth = 0 if len(rigth) == 0 else rigth[0]
                print(str(left)+" "+str(rigth))
                regions[i] = (regions[i][0]-left,regions[i][1]+rigth)
            if merge_factor > 0:
                regions = self.mergeIntervals(regions, merge_factor)


        regions = [c for c in regions if (c[1]-c[0]) > minSize]

        if merge_factor > 0 >= secondThreshold:
            regions = self.mergeIntervals(regions, merge_factor)

        return regions
