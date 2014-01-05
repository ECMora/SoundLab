from Duetto_Core.Cursors.PointerCursor import PointerCursor
from Duetto_Core.Detectors.Detector import Detector
from numpy import mean
class MeanDetector(Detector):

    def __init__(self):
        Detector.__init__(self)

    def detect(self,signal,indexFrom=0,indexTo=-1):
        self.pointers=[PointerCursor()]
        self.pointers[0].visualOptions.vertical=False
        self.pointers[0].index=mean(signal.data[indexFrom:indexTo])




