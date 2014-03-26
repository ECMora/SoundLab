from Duetto_Core.Cursors.IntervalCursor import IntervalCursor
from Duetto_Core.Detectors.Detector import Detector
from matplotlib import mlab
import numpy

class MaxInstantFrequencyDetector(Detector):
    def __init__(self):
        Detector.__init__(self)

    def detect(self,signal,indexFrom=0,indexTo=-1,noverlap = 0,NFFT = 512):
        self.Pxx, self.freqs, self.bins = mlab.specgram(signal.data[indexFrom:indexTo],NFFT,Fs=signal.samplingRate,noverlap=0)
        findexs = numpy.argmax(self.Pxx, axis=0)

        print len(self.freqs[findexs])
        print len(self.bins)

        return self.freqs[findexs],self.bins