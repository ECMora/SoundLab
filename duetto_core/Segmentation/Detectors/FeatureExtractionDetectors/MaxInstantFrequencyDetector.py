# -*- coding: utf-8 -*-
from matplotlib import mlab
import numpy
from Duetto_Core.Segmentation.Detectors import Detector


class MaxInstantFrequencyDetector(Detector):
    def __init__(self):
        Detector.__init__(self)

    def detect(self,signal,indexFrom=0,indexTo=-1,noverlap = 0,NFFT = 512):
        self.Pxx, self.freqs, self.bins = mlab.specgram(signal.data[indexFrom:indexTo],NFFT,Fs=signal.samplingRate,noverlap=0)
        findexs = numpy.argmax(self.Pxx, axis=0)

        return self.freqs[findexs],self.bins