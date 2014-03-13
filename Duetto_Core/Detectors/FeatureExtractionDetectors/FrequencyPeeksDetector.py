from Duetto_Core.Cursors.PointerCursor import PointerCursor
from Duetto_Core.Detectors.Detector import Detector
from Duetto_Core.SignalProcessors.SignalProcessor import SignalProcessor
from matplotlib import mlab

class FrequencyPeeksDetector(Detector):
    def __init__(self):
        Detector.__init__(self)

    def detect(self,signal,indexFrom=0,indexTo=-1,threshold = 0,hysteresis = 0):
        if indexTo == -1:
            indexTo = signal.data.size
        pxx,freqs = mlab.psd(signal.data[indexFrom:indexTo],Fs=signal.samplingRate,NFFT=512)
        self.pointer2D = []
        size = freqs.size
        minLast = 0
        for i in range(1,size):
            if pxx[i] >= threshold and pxx[i] >= minLast + hysteresis:
                self.pointer2D.append(PointerCursor(freqs[i]))
                minLast = pxx[i]
            else:
                minLast = min(minLast,pxx[i])

