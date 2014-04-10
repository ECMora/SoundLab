from numpy import inf
from numpy.ma import arctan
from Duetto_Core.Cursors.PointerCursor import PointerCursor
from Duetto_Core.Segmentation.Detectors import Detector


class InflectionPointDetector(Detector):
    def __init__(self):
        Detector.__init__(self)

    def detect(self, signal, indexFrom, indexTo):
        self.pointer2D = [PointerCursor()]
        self.pointer2D[0].visualOptions.vertical = True
        self.pointer2D[0].visualOptions.oscilogramCursor = False
        mfd = MaxFreqDetector()
        mfd.detect(signal, indexFrom, indexTo)
        data = [p.indexes[1] for p in mfd.pointers2D]
        self.pointer2D[0].index = self._getInflectionPosition2(data)

    def _getInflectionPosition(self, data):
        imax = (0, 0)
        l = len(data)
        for i in range(1, l-2):
            p1 = 1. * (data[i]-data[0]) / i
            p2 = 1. * (data[-1]-data[i]) / (l-i-1)
            inflection = abs(arctan(p1) - arctan(p2))
            if inflection > imax[1]:
                imax = (i, inflection)
        return imax

    def _getInflectionPosition2(self, data):
        imax = (0, -inf)
        l = len(data)
        for i in range(2, l-3):
            _, infl1 = self.get_inflection_position(data[0: i+1])
            _, infl2 = self.get_inflection_position(data[i: l])
            p1 = 1. * (data[i]-data[0]) / i
            p2 = 1. * (data[-1]-data[i]) / (l-i-1)
            inflection = abs(arctan(p1) - arctan(p2))
            inflection2 = inflection - (infl1 + infl2)
            if inflection2 > imax[1]:
                imax = (i, inflection2)
        return imax
