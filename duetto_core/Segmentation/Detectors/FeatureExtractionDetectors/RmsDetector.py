from Duetto_Core.Cursors.PointerCursor import PointerCursor
from Duetto_Core.Segmentation.Detectors import Detector
from Duetto_Core.SignalProcessors.SignalProcessor import SignalProcessor

class RmsDetector(Detector):

    def __init__(self):
        Detector.__init__(self)

    def detect(self,signal,indexFrom=0,indexTo=-1):
        p = PointerCursor()
        p.visualOptions.vertical=False
        s = SignalProcessor(signal.data)
        p.index = s.rms (indexFrom,indexTo)
        self.pointers=[p]


