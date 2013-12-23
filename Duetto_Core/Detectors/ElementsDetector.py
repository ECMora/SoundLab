from numpy import *
from Duetto_Core.AudioSignals.WavFileSignal import WavFileSignal
from Duetto_Core.Cursors.IntervalCursor import IntervalCursor
from Duetto_Core.Detectors.Detector import Detector
from Duetto_Core.Clasification.Element import Element
import matplotlib.mlab as mlab
from Duetto_Core.SignalProcessors.SignalProcessor import SignalProcessor
import time
from numpy.lib.function_base import percentile

class ElementDetector(Detector):
    def __init__(self):
        Detector.__init__(self)
        self.NOISE_MERGE_FACTOR=1/50.0
        self.MIN_INTERVAL=0

    def detect(self,signal,indexFrom=0,indexTo=-1,threshold=50):
        self.oscilogram_elements_detector(signal,indexFrom,indexTo,threshold)

    def oscilogram_elements_detector(self, signal,indexFrom=0,indexTo=-1,threshold=50,intervalDuration = 1):
        indexTo = indexTo if indexTo >=0 else len(signal.data)

        media = mean(abs(signal.data[indexFrom:indexTo]))
        #intervalos de 1 ms
        intervals = []
        current_interval = None
        MS = int(1000*intervalDuration)
        number_of_ms_intervals = (indexTo-indexFrom)*MS/signal.samplingRate
        interval_length = signal.samplingRate/MS

        for i in range(1,number_of_ms_intervals):
            interval_rms = sum(abs(signal.data[indexFrom + (i-1)*interval_length : indexFrom + i*interval_length]))/interval_length
            if(interval_rms > media):
                if(current_interval is not  None):
                    current_interval = (current_interval[0], current_interval[1] + interval_length)
                else:
                    current_interval = ( (i-1)*interval_length, i*interval_length)
            else:
                if(current_interval is not None):
                    intervals.append(current_interval)
                    current_interval = None

        if( number_of_ms_intervals * signal.samplingRate != (indexTo-indexFrom)*MS):
            interval_rms = sum(abs(signal.data[indexFrom + number_of_ms_intervals*interval_length : indexTo]))
            if(interval_rms > media):
                current_interval = current_interval if current_interval is not  None else (number_of_ms_intervals*interval_length, indexTo)
                current_interval = (current_interval[0], indexTo)

        if(current_interval is not None):
            intervals.append(current_interval)

        #tratar de acortar o aumentar cada intervalo reconocido mediante una funcion de inicio y final del elemento


        if(len(intervals)== 0 and intervalDuration > 0.2 ):
            self.oscilogram_elements_detector(signal,indexFrom,indexTo,threshold,intervalDuration/2)
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

        #build the elements by link the indices
        elements = array([[Element(signal, indexFrom, indexTo, Pxx, bins, freqs, None, [e], i) for e in col] for i, col in enumerate(elements)])

        identifiedElements = elements[0]
        #mezclar con anteriores elementos detectados
        for column in elements:
            pass

        #remove the element that not satify the length requirements
        identifiedElements=array([el for el in identifiedElements if (el.size() >= minLongitud)])
        print("Algortimo finalizado "+str(time.time()-t))
        return identifiedElements

    def mergeIntervals(self, a, distancefactor=2):
        """
        Merge into one interval two intervals with no more than  distance factor distance between them
        """
        b = []
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
#wav = WavFileSignal()
#wav.open("..\\..\\..\\ficheros de audio\Clasif\c2.wav")
#
#detector=ElementDetector()
#el=detector.oscilogram_elements_detector(wav)
