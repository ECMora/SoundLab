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

    def detect(self,signal, indexFrom=0, indexTo=-1, threshold=0, decay=1,minSize=0,softfactor = 5,merge_factor=0):
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
            if threshold == 0:
                threshold = mean(signal.data[indexFrom : indexTo])/2
                self.threshold = 20*log10(threshold*1000.0/(2**signal.bitDepth))
            else:
                #translate the threshold from dB scale to V value
                threshold = (10.0**(threshold/20.0))*(2**signal.bitDepth)/1000.0

            if merge_factor != 0:
                merge_factor = merge_factor*signal.samplingRate/1000.0
            if minSize != 0:
                minSize = minSize*signal.samplingRate/1000.0
            self.intervals = [IntervalCursor(c[0], c[1]) for c in self.one_dimensional_elements_detector(signal.data[indexFrom : indexTo],threshold, minSize=minSize, decay=decay, softfactor=softfactor, merge_factor=merge_factor)]



    def one_dimensional_elements_detector(self, data,threshold=0, minSize=1, decay=1, softfactor=10, merge_factor=0, above_threshold_precent = 10):
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
        regions = [c for c in regions if (c[1]-c[0]) > minSize]
        if merge_factor > 0:
            regions = self.mergeIntervals(regions, merge_factor)
        return regions


class SegmentsDetector(Detector):
    """This abstract class represents diferent ways to split an audio signal"""
    UNIFORM_SEGMENTER,PSEUDOUNIFORM_SEGMENTER,NOICE_DETECTION_SEGMENTER=range(3)

    def __init__(self):
        Detector.__init__(self)

    def detect(self,signal,noiseThreshold=0,segment_mode=UNIFORM_SEGMENTER,params=[]):
        segments=[]
        if(segment_mode==self.UNIFORM_SEGMENTER):
            segments=self.uniformSegmenter(signal.data,10)
        if(segment_mode==self.PSEUDOUNIFORM_SEGMENTER):
            segments=self.pseudoUniformSegmenter(signal.data,10)
        if(segment_mode==self.NOICE_DETECTION_SEGMENTER):
            pass
        for x in segments:
            self.intervals.append(IntervalCursor(x[0],x[1]))


    def uniformSegmenter(self,userData=[],numberOfIntervals=1):
        """naive implementation
         Returns an array with numberOfIntervals elements each one is a tuple
        with the index of the original array that were in the section
        [i*numberOfIntervals:(i+1)*numberOfIntervals]
        """
        if(len(userData)<1):
            return array([])
        if(numberOfIntervals==1):
            return array(userData)
        data=[]
        intervalWidth =int(floor(len(userData)/numberOfIntervals))
        for i in range(numberOfIntervals-1):
            data.append((i*intervalWidth,(i+1)*intervalWidth))
        data.append(((numberOfIntervals-1)*intervalWidth,len(userData)))
        return data

    def pseudoUniformSegmenter(self,userData=[],numberOfIntervals=1,threshold=0):
        """
        returns the result of  uniform Segmenter where each element is
        trimmed at the beginning and at the end. deleting the values lower than the threshold.
        """
        if(len(userData)<1):
            return array([])
        data=self.uniformSegmenter(userData,numberOfIntervals)
        #arreglar
        return data

    def trim(self,data,threshold=0):
        """
        Trim the leading and/or trailing numbers from a 1-D array or sequence that are lower
        than threshold

        """
        first = 0
        for i in data:
            if i >threshold: break
            else: first = first + 1
        last = len(data)
        for i in data[::-1]:
            if i >threshold: break
            else: last = last - 1
        return data[first:last]

