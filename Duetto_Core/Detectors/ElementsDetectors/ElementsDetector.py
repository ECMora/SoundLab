import time

from numpy import *
import matplotlib.mlab as mlab
from numpy.lib.function_base import percentile
from Duetto_Core.AudioSignals.WavFileSignal import WavFileSignal
from Duetto_Core.SignalProcessors.SignalProcessor import envelope
from Duetto_Core.Cursors.IntervalCursor import IntervalCursor
from Duetto_Core.Detectors.Detector import Detector
from Duetto_Core.Segmentation import Element


class ElementsDetector(Detector):
    def __init__(self):
        Detector.__init__(self)
        self.NOISE_MERGE_FACTOR=1/50.0
        self.MIN_INTERVAL=1

    def mergeIntervals(self, a, distancefactor=50):
        """
        Merge into one interval two intervals with no more than  distance factor distance between them
        """
        b = []
        if(a is None or len(a) == 0):
            return b

        current = a[0]
        for tuple in a[1:]:
            if (tuple[0]-current[1])*100.0/(tuple[1]-current[0]) >= distancefactor:
                current=(current[0], tuple[1])
            else:
                b.append(current)
                current=tuple
        b.append(current)
        return b





#
#wav = WavFileSignal()
#wav.open("..\\..\\..\\ficheros de audio\Clasif\c1.wav")
#envelope(wav, decimation=10)
#oscilogram_elements_detector=ElementsDetector()
#el=oscilogram_elements_detector.one_dimensional_elements_detector(wav)
#a = range(25)
#
#b = [mean(a[i*len(a)/10:(i+1)*len(a)/10]) for i in range(10)]
#
#print(b)
