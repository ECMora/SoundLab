from Duetto_Core.Cursors.IntervalCursor import IntervalCursor
from Duetto_Core.Detectors.Detector import Detector
from matplotlib import mlab
class MinMaxFrequencyDetector(Detector):

    def __init__(self):
        Detector.__init__(self)

    def detect(self,signal,indexFrom=0,indexTo=-1,threshold = 0,freq = 0):
        if indexTo == -1:
            indexTo = signal.data.size
        pxx,freqs = mlab.psd(signal.data[indexFrom:indexTo],Fs=signal.samplingRate,NFFT=512)
        value = pxx[freq] - threshold
        l = freq
        r = freq
        size = len(freqs)
        for i in range(freq + 1, size):
            if pxx[i] < value:
                r = i - 1
                break

        for i in range(freq - 1, -1, -1):
            if pxx[i] < value:
                l = i + 1
                break

        p1 = IntervalCursor(freqs[l],freqs[r])
        p1.visualOptions.vertical=False
        self.oneDimensionalElements = [p1]

