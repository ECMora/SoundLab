# -*- coding: utf-8 -*-
from matplotlib import mlab

from sound_lab_core.Cursors.IntervalCursor import IntervalCursor
from sound_lab_core.Segmentation.Detectors.ElementsDetectors import ElementsDetector


class MinMaxFrequencyDetector(ElementsDetector):

    def __init__(self):
        ElementsDetector.__init__(self)

    def detect(self,signal,indexFrom=0,indexTo=-1,threshold = 0,freq = 0):
        if indexTo == -1:
            indexTo = signal.data.size
        pxx,freqs = mlab.psd(signal.data[indexFrom:indexTo],Fs=signal.samplingRate,NFFT=512)
        value = pxx[freq] - threshold
        l = freq
        r = freq
        size = len(freqs)
        for i in range(freq + 1, size):
            if pxx[i] < value:
                r = i - 1
                break

        for i in range(freq - 1, -1, -1):
            if pxx[i] < value:
                l = i + 1
                break

        p1 = IntervalCursor(freqs[l],freqs[r])
        p1.visualOptions.vertical=False
        self.oneDimensionalElements = [p1]

