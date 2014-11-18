# -*- coding: utf-8 -*-
from sound_lab_core.Cursors.PointerCursor import PointerCursor
from sound_lab_core.SignalProcessors.SignalProcessor import SignalProcessor
from sound_lab_core.Segmentation.Detectors.ElementsDetectors import ElementsDetector


class RmsDetector(ElementsDetector):

    def __init__(self):
        ElementsDetector.__init__(self)

    def detect(self,signal,indexFrom=0,indexTo=-1):
        p = PointerCursor()
        p.visualOptions.vertical=False
        s = SignalProcessor(signal.data)
        p.index = s.rms (indexFrom,indexTo)
        self.pointers=[p]


