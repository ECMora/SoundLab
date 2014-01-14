from numpy import *
import matplotlib.mlab as mlab
from Duetto_Core.Detectors.ElementsDetectors.ElementsDetector import ElementsDetector
from Duetto_Core.Detectors.ElementsDetectors.OneDimensionalElementsDetector import OneDimensionalElementsDetector
from Duetto_Core.Segmentation.Elements import Element


class TwoDimensionalElementsDetector(ElementsDetector):

    def __init__(self):
        ElementsDetector.__init__(self)
        self.one_dimensional_elements_detector = OneDimensionalElementsDetector()
        self.specgram_elements_detector = self.two_dimensional_elements_detector

    def detect(self, signal, indexFrom=0, indexTo=-1, threshold=50, decay=1, minsize=2):
            pass

    def two_dimensional_elements_detector(self, signal, indexFrom=0, indexTo = -1, threshold=50, NFFT=256):
            #buscar maximos locales de frecuencia por intervalo de tiempo
            #unir los maximos locales que esten "cercanos" mediante un concepto de distancia
            #minLongitud en ms de los elementos detectados

            Pxx, freqs, bins = mlab.specgram(range(1000,2000)*sin(range(1000)),
                                             NFFT, noverlap=128, sides="onesided",window=mlab.window_hanning)

            distancefactor = Pxx.shape[0]*1./100  # 1 %
            #select the elements in every piece of time
            elements = array([[self.one_dimensional_elements_detector.one_dimensional_elements_detector(Pxx[1:, col])] for col in range(Pxx.shape[1])])
            print(elements)
            #build the elements by link the indices


            elements = array([[Element(signal, indexFrom, indexTo, Pxx, bins, freqs, None, [e], i) for e in col] for i, col in enumerate(elements)])

            identifiedElements = [el for el in [el2 for el2 in elements]]

            return identifiedElements


from Duetto_Core.AudioSignals.WavFileSignal import WavFileSignal

wav = WavFileSignal()
wav.open("..\\..\\ficheros de audio\\Clasif\c2.wav")
d = TwoDimensionalElementsDetector()
d.two_dimensional_elements_detector(wav)


