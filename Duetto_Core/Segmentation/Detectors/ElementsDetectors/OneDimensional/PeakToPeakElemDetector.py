# -*- coding: utf-8 -*-
import numpy as np
from Duetto_Core.Segmentation.Detectors.ElementsDetectors.OneDimensional import OneDimensionalElementsDetector
from Duetto_Core.Segmentation.Elements.OneDimensionalElement import OscilogramElement


class PeakToPeakElemDetector(OneDimensionalElementsDetector):
    #progress = pyqtSignal(int)

    def __init__(self, progressReporter=None):
        OneDimensionalElementsDetector.__init__(self, progressReporter)
        self.envelope = None

    def detect(self, signal, indexFrom=0, indexTo=None, threshold=None, minSize=None, minDist=None, progressReporter=None,
               specgramSettings=None, **kwargs):
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
        if self.progress:
            self.progress(5)

        # preprocess (find peaks)
        data = signal.data[indexFrom: indexTo]
        dataAbs = np.abs(data)
        if self.progress:
            self.progress(20)
        peaks = np.logical_and(dataAbs[1:-1] > dataAbs[:-2], dataAbs[1:-1] > dataAbs[2:])
        peaks = np.concatenate(([True], peaks, [True]))
        if self.progress:
            self.progress(40)
        peaksPos = np.argwhere(peaks).flatten()
        peaks = dataAbs[peaks]
        if self.progress:
            self.progress(60)

        if threshold is None:
            threshold = np.mean(peaks)# - 2 * np.std(peaks)
        if self.progress:
            self.progress(70)

        # find segments
        starts = np.logical_and(peaks[:-1] < threshold, threshold <= peaks[1:])
        starts = np.concatenate(([True if peaks[0] >= threshold else False], starts))
        starts = peaksPos[starts]
        if self.progress:
            self.progress(80)
        ends = np.logical_and(peaks[:-1] >= threshold, threshold > peaks[1:])
        ends = np.concatenate((ends, [True if peaks[-1] >= threshold else False]))
        ends = peaksPos[ends]
        if self.progress:
            self.progress(90)

        # postprocess (join and remove segments)
        joinMask = starts[1:] - ends[:-1] >= minDist
        starts = starts[np.concatenate(([True], joinMask))]
        ends = ends[np.concatenate((joinMask, [True]))]
        if self.progress:
            self.progress(93)

        removeMask = ends - starts >= minSize
        starts = starts[removeMask]
        ends = ends[removeMask]
        if self.progress:
            self.progress(96)

        self.elements = []
        for i in np.arange(len(starts)):
            self.elements.append(OscilogramElement(signal, starts[i], ends[i], i + 1,
                                                                 specgramSettings=specgramSettings))
        if self.progress:
            self.progress(100)
