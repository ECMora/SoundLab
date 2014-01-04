import time

from numpy import *
import matplotlib.mlab as mlab
from numpy.lib.function_base import percentile
from Duetto_Core.AudioSignals.WavFileSignal import WavFileSignal
from Duetto_Core.SignalProcessors.SignalProcessor import envelope
from Duetto_Core.Cursors.IntervalCursor import IntervalCursor
from Duetto_Core.Detectors.Detector import Detector
from Duetto_Core.Segmentation import Element


class ElementDetector(Detector):
    def __init__(self):
        Detector.__init__(self)
        self.NOISE_MERGE_FACTOR=1/50.0
        self.MIN_INTERVAL=1

    def detect(self,signal,indexFrom=0,indexTo=-1,threshold=50):
        MS = int(1000*self.MIN_INTERVAL)
        interval_length = signal.samplingRate/MS
        return self.oscilogram_elements_detector(signal.data[indexFrom:indexTo], threshold, interval_length)

    def oscilogram_elements_detector(self, data, threshold=50,intervalSize = 1000,overlap=50):
        """
        detect intervals of dimension 1 in data
        """
        length = len(data)
        #el threshold debe ser piece wise para que no influya en la deteccion de
        #un segmento particular las caracteristicas de toda la sennal

        media = mean(abs(data))
        print([mean(abs(data[x*length/10:(x+1)*length/10])) for x in range(10)])

        #intervalos de intervalSize ms
        intervals = []
        current_interval = None
        number_of_intervals = length/intervalSize
        print(media)
        for i in range(1,number_of_intervals):
            interval_rms = sum(abs(data[(i-1)*intervalSize : i*intervalSize]))/intervalSize
            print("******************"+str(interval_rms))
            if(interval_rms > media):
                if(current_interval is not  None):
                    current_interval = (current_interval[0], current_interval[1] + intervalSize)
                else:
                    current_interval = ((i-1)*intervalSize, i*intervalSize)
            else:
                if(current_interval is not None):
                    intervals.append(current_interval)
                    current_interval = None

        if length % intervalSize != 0:
            interval_rms = sum(abs(data[number_of_intervals*intervalSize:]))
            if(interval_rms > media):
                current_interval = current_interval if current_interval is not  None else (number_of_intervals*intervalSize, length)
                current_interval = (current_interval[0], length)

        if(current_interval is not None):
            intervals.append(current_interval)
        #tratar de acortar o aumentar cada intervalo reconocido mediante una funcion de inicio y final del elemento

        #agrupar intervalos cercanos y desechar los que sean muy pequennos
        #intervals = self.mergeIntervals(intervals, 2*interval_length)
        self.intervals = [IntervalCursor(c[0], c[1]) for c in intervals]

    def specgram_elements_detector(self, signal, indexFrom=0, indexTo = -1, threshold=50, NFFT=512, overlap = 0, minLongitud = 1):
        #buscar maximos locales de frecuencia por intervalo de tiempo
        #unir los maximos locales que esten "cercanos" mediante un concepto de distancia
        #minLongitud en ms de los elementos detectados
        if(threshold<0 or threshold >=100):
            return

        Pxx, freqs, bins = mlab.specgram(signal.data[indexFrom:indexTo],
                                         NFFT, Fs=2, detrend=mlab.detrend_none, noverlap=10, sides="onesided",window=mlab.window_hanning)

        t = time.time()
        umbral = percentile(Pxx, threshold)

        distancefactor = Pxx.shape[0]*1./100  # 1 %

        #select the elements in every piece of time
        elements = array([self.mergeIntervals(mlab.contiguous_regions(Pxx[1:, col] >= umbral), distancefactor) for col in range(Pxx.shape[1])])
        print(elements)
        #build the elements by link the indices
        elements = array([[Element(signal, indexFrom, indexTo, Pxx, bins, freqs, None, [e], i) for e in col] for i, col in enumerate(elements)])

        identifiedElements = [el for el in [el2 for el2 in elements]]
        #mezclar con anteriores elementos detectados
        for column in elements:
            pass

        #remove the element that not satify the length requirements
        #identifiedElements=array([el for el in identifiedElements if (el.size() >= minLongitud)])
        print("Algortimo finalizado "+str(time.time()-t))
        return identifiedElements

    def mergeIntervals(self, a, distancefactor=2):
        """
        Merge into one interval two intervals with no more than  distance factor distance between them
        """
        b = []
        if(a is None or len(a) == 0):
            return b

        current = a[0]
        for tuple in a[1:]:
            if(tuple[0]-current[1] < distancefactor):
                current=(current[0],tuple[1])
            else:
                b.append(current)
                current=tuple
        b.append(current)
        return b





#
wav = WavFileSignal()
wav.open("..\\..\\..\\ficheros de audio\Clasif\c1.wav")
envelope(wav, decimation=10)
#detector=ElementDetector()
#el=detector.oscilogram_elements_detector(wav)
#a = range(25)
#
#b = [mean(a[i*len(a)/10:(i+1)*len(a)/10]) for i in range(10)]
#
#print(b)
arr=[10,2,10,10,10,10,10,10,10,10,1]

print([arr[0]+x*(arr[0]-arr[10])/(-10) for x in range(1,10+1)])