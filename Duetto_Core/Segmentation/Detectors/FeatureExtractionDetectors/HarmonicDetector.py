# -*- coding: utf-8 -*-
from matplotlib import mlab

from Duetto_Core.Segmentation.Detectors.MinMaxFrequencyDetector import MinMaxFrequencyDetector
from Duetto_Core.Segmentation.Detectors.ElementsDetectors import ElementsDetector
from Duetto_Core.Segmentation.Detectors.FeatureExtractionDetectors import FrequencyPeeksDetector
from Duetto_Core.Segmentation.Elements.OneDimensionalElement import OneDimensionalElement


class HarmonicDetector(ElementsDetector):
    def __init__(self):
        ElementsDetector.__init__(self)

    def detect(self,signal,indexFrom=0,indexTo=-1,thresholdAbs = 0,thresholdRel = 0,hysteresis = 0):
        fpeeksd = FrequencyPeeksDetector()
        fpeeksd.detect(signal,indexFrom,indexTo,thresholdAbs,hysteresis)
        if indexTo == -1:
            indexTo = signal.data.size
        pxx,freqs = mlab.psd(signal.data[indexFrom:indexTo],Fs=signal.samplingRate,NFFT=512)
        self.oneDimensionalElements = []
        minmaxfreqd = MinMaxFrequencyDetector()
        for p in fpeeksd.pointers:
            minmaxfreqd.detect(signal,indexFrom,indexTo,thresholdRel,p.index)
            interval = minmaxfreqd.intervals[0]
            self.oneDimensionalElements.append(OneDimensionalElement(signal,interval.min,interval.max))

