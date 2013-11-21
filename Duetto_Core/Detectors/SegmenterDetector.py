from numpy import array,floor
from Duetto_Core.Cursors.IntervalCursor import IntervalCursor
from Duetto_Core.Detectors.Detector import Detector

class SegmenterDetector(Detector):
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

    def noiseDetectionSegmenter(self):
        """

                """

        pass
