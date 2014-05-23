# -*- coding: utf-8 -*-
import numpy as np
from Duetto_Core.Segmentation.Detectors.ElementsDetectors.OneDimensionalElementsDetector import OneDimensionalElementsDetector
from Duetto_Core.Segmentation.Elements.OneDimensionalElement import OscilogramElement


class IntervalElemDetector(OneDimensionalElementsDetector):
    #progress = pyqtSignal(int)

    def __init__(self, progressReporter=None):
        OneDimensionalElementsDetector.__init__(self, progressReporter)
        self.envelope = None
        self.functions = {'RMS': (self.RMS_prepare, self.RMS), 'meanAbs': (self.meanAbs_prepare, self.meanAbs)}
        self.procData = np.array([])

    def RMS_prepare(self, data):
        self.procData = np.cumsum(data * data)

    def RMS(self, indexFrom, indexTo):
        if indexFrom == indexTo:
            return 0
        if indexTo < indexFrom:
            indexFrom, indexTo = indexTo, indexFrom
        dataTo = self.procData[indexTo - 1]
        dataFrom = self.procData[indexFrom - 1] if indexFrom > 0 else 0
        return np.sqrt((dataTo - dataFrom) / (indexTo - indexFrom + 1))

    def meanAbs_prepare(self, data):
        self.procData = np.cumsum(np.abs(data))

    def meanAbs(self, indexFrom, indexTo):
        if indexFrom == indexTo:
            return 0
        if indexTo < indexFrom:
            indexFrom, indexTo = indexTo, indexFrom
        dataTo = self.procData[indexTo - 1]
        dataFrom = self.procData[indexFrom - 1] if indexFrom > 0 else 0
        return (dataTo - dataFrom) / (indexTo - indexFrom + 1)

    def detect(self, signal, indexFrom=0, indexTo=None, threshold=None, minDist=None, minSize=None, function='RMS',
               progressReporter=None, specgramSettings=None, **kwargs):
        if not signal:
            return
        if indexTo is None:
            indexTo = len(signal.data)
        if progressReporter is not None:
            self.progress = progressReporter
        if minDist is None:
            minDist = 250
        else:
            minDist *= signal.samplingRate / 1000.0
        if minSize is None:
            minSize = 250
        else:
            minSize *= signal.samplingRate / 1000.0
        func_prepare, function = self.functions[function]
        if threshold is None:
            threshold = np.mean(signal.data) + 2 * np.std(signal.data)
        if self.progress:
            self.progress(70)
        if self.progress:
            self.progress(5)

        self.oneDimensionalElements = []

        data = signal.data[indexFrom: indexTo]
        data = np.concatenate((np.zeros(minDist), data, np.zeros(minDist)))
        remPos = np.argwhere(data > threshold).flatten()
        already = minDist

        func_prepare(data)

        while len(remPos):
            center = remPos[0]
            start, end = center, center

            start = np.argmax([function(s, end) - function(s - minDist, s)
                               for s in np.arange(already, center)]) + already
            end = np.argmax([function(start, e + 1) - function(e, e + minDist)
                             for e in np.arange(center, len(data) - minDist)]) + center
            if end - start >= minSize:
                self.oneDimensionalElements.append(OscilogramElement(signal, start - minDist, end - minDist,
                                                                     len(self.oneDimensionalElements) + 1,
                                                                     specgramSettings=specgramSettings))
            already = end + 1
            if self.progress:
                self.progress(5 + already * 95 / len(data))
            remPos = remPos[remPos >= already]
