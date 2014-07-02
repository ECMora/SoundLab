# -*- coding: utf-8 -*-
from Duetto_Core.Cursors.PointerCursor import PointerCursor
from Duetto_Core.Segmentation.Detectors.ElementsDetectors import ElementsDetector
from Duetto_Core.SignalProcessors.SignalProcessor import SignalProcessor

class RmsDetector(ElementsDetector):

    def __init__(self):
        ElementsDetector.__init__(self)

    def detect(self,signal,indexFrom=0,indexTo=-1):
        p = PointerCursor()
        p.visualOptions.vertical=False
        s = SignalProcessor(signal.data)
        p.index = s.rms (indexFrom,indexTo)
        self.pointers=[p]


