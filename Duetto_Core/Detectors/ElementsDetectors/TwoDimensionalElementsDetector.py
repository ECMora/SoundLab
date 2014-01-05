from numpy import *
import matplotlib.mlab as mlab
from numpy.lib.function_base import percentile
from Duetto_Core.Detectors.ElementsDetectors.ElementsDetector import ElementsDetector
from Duetto_Core.Detectors.ElementsDetectors.OneDimensionalElementsDetector import OneDimensionalElementsDetector


class TwoDimensionalElementsDetector(ElementsDetector):

    def __init__(self):
        ElementsDetector.__init__(self)
        self.one_dimensional_elements_detector = OneDimensionalElementsDetector()
        self.specgram_elements_detector = self.two_dimensional_elements_detector

    def detect(self,signal,indexFrom=0,indexTo=-1,threshold=50,decay=1, minsize=2):
            pass

    def two_dimensional_elements_detector(self, signal, indexFrom=0, indexTo = -1, threshold=50, NFFT=512):
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
            elements = numpy.array([self.mergeIntervals(mlab.contiguous_regions(Pxx[1:, col] >= umbral), distancefactor) for col in range(Pxx.shape[1])])
            print(elements)
            #build the elements by link the indices
            elements = numpy.array([[Element(signal, indexFrom, indexTo, Pxx, bins, freqs, None, [e], i) for e in col] for i, col in enumerate(elements)])

            identifiedElements = [el for el in [el2 for el2 in elements]]
            #mezclar con anteriores elementos detectados
            for column in elements:
                pass

            #remove the element that not satify the length requirements
            #identifiedElements=numpy.array([el for el in identifiedElements if (el.size() >= minLongitud)])

            return identifiedElements