# -*- coding: utf-8 -*-
from numpy import mean

from Duetto_Core.Cursors.PointerCursor import PointerCursor
from Duetto_Core.Segmentation.Detectors.ElementsDetectors import ElementsDetector


class MeanDetector(ElementsDetector):

    def __init__(self):
        ElementsDetector.__init__(self)

    def detect(self,signal,indexFrom=0,indexTo=-1):
        self.pointer2D=[PointerCursor()]
        self.pointer2D[0].visualOptions.vertical=False
        self.pointer2D[0].index=mean(signal.data[indexFrom:indexTo])




