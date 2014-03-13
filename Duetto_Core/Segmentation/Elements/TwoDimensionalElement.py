from Duetto_Core.Segmentation.Elements.Element import Element


class TwoDimensionalElement(Element):
    """
    In an acoustic procesing transform of 2 dimensional as spectrogram an element is a 2 dimensional region
    of local maximum in the rectangular matrix of specgram
    """
    def __init__(self, signal,matrix):
        Element.__init__(self,signal)
        self.matrix = matrix


class SpecgramElement(TwoDimensionalElement):

    def __init__(self,signal,matrix,freqs,bins):
        TwoDimensionalElement.__init__(self,signal,matrix)
        self.bins = bins
        self.freqs = freqs

    def startTime(self):
        return self.bins[0]

    def endTime(self):
        return self.bins[-1]

    def minFreq(self):
        return self.freqs[0]

    def maxFreq(self):
        return self.freqs[-1]

    def PeakFreq(self,meditionTime = 0.0):
        return 0





