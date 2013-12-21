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

    def detect(self,signal,indexFrom=0,indexTo=-1,threshold=50,type="simple"):
        if("minInterval" == type):
            self.minIntervalDetect(signal,indexFrom,indexTo,threshold)
        elif("mergedIntervals" == type):
            self.mergedIntervals(signal,indexFrom,indexTo,threshold)
        else:
            self.MIN_INTERVAL=0
            self.minIntervalDetect(signal,indexFrom,indexTo,threshold)

    def minIntervalDetect(self,signal,indexFrom=0,indexTo=-1,threshold=50):
        """
        identify the elements in the signal.
        minInterval float in ms of the min interval for detected call
       """
        if(indexTo==-1):
            indexTo=len(signal.data)

        begin=-1#the index of the start of an element
        i=indexFrom
        minInterval=self.MIN_INTERVAL*signal.samplingRate/1000.0

        currentMaxPeak=abs(signal.data[i])
        monotonyAscending=currentMaxPeak<abs(signal.data[i+1])

        while(i<indexTo):
            while(i+1<indexTo and ((monotonyAscending and currentMaxPeak<=abs(signal.data[i+1])) or
                 (not monotonyAscending and currentMaxPeak>=abs(signal.data[i+1])))):#get the next peak
                i+=1
                currentMaxPeak=abs(signal.data[i])
                if(begin==-1 and currentMaxPeak>threshold):#found a first point above threshold
                    begin=i

            if(begin!=-1 and currentMaxPeak<threshold and monotonyAscending and (i-begin)>minInterval):#the end of a peak
                #all the calls has at least ms size
                self.intervals.append(IntervalCursor(begin,i))
                begin=-1
            if(i+1<indexTo):
                monotonyAscending=currentMaxPeak<abs(signal.data[i+1])
            i+=1
        if(begin!=-1):
            self.intervals.append(IntervalCursor(begin,i))

    def mergedIntervals(self,signal,indexFrom=0,indexTo=-1,threshold=50):
        aux=self.MIN_INTERVAL
        self.MIN_INTERVAL=0
        self.minIntervalDetect(signal,indexFrom,indexTo,threshold)
        self.MIN_INTERVAL=1
        newIntervals=[]
        if(len(self.intervals)==0):
            return
        current=self.intervals[0]
        i=1
        length=len(self.intervals)
        msSize=self.MIN_INTERVAL*signal.samplingRate/1000


        while(i<length):
            while(i<length and self.intervals[i].min-current.max<self.NOISE_MERGE_FACTOR*(self.intervals[i].max-self.intervals[i].min)):
                current.max=self.intervals[i].max
                i+=1
            if(i<length):
                newIntervals.append(current)
                current=self.intervals[i]
                i+=1
        newIntervals.append(current)
        self.intervals=[x for x in newIntervals if(x.max-x.min>msSize)]


    def specgram_elements_detector(self, signal, indexFrom=0, indexTo = -1, threshold=50, NFFT=512, overlap = 0, minamplitud = 1, minLongitud = 1):
        #buscar maximos locales de frecuencia por intervalo de tiempo
        #unir los maximos locales que esten "cercanos" mediante un concpto de distancia
        #asume calculado el psd
        #minamplitud en Hz
        #minLongitud en ms
        if(threshold<0 or threshold >=100):
            return

        Pxx, freqs, bins = mlab.specgram(signal.data[indexFrom:indexTo],
                                         NFFT, Fs=2, detrend=mlab.detrend_none, noverlap=10, sides="onesided",window=mlab.window_hanning)

        t = time.time()
        umbral = percentile(Pxx, threshold)

        distancefactor = Pxx.shape[0]*1./100  # 1 %
        elements = array([self.mergeIntervals(mlab.contiguous_regions(Pxx[1:, col] >= umbral),distancefactor) for col in range(Pxx.shape[1])])

        #build the elements by link the indices
        elements = array([[Element(signal, indexFrom, indexTo, Pxx, bins, freqs, None, [e], i) for e in col] for i, col in enumerate(elements)])

        identifiedElements = []

        for arr in elements:
            pass

        #mergeIntervals

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




#wav = WavFileSignal()
#wav.open("..\\..\\..\\ficheros de audio\Clasif\c2.wav")
#print(str(len(wav.data))+" "+str(wav.samplingRate))
#print(wav.data)
#wav.resampling(wav.samplingRate/3.3)
#print(wav.data)
#print(str(len(wav.data))+" "+str(wav.samplingRate))

#detector=ElementDetector()
#el=detector.specgram_elements_detector(wav)
#
#for x in el:
#    #print("New Column")
#    print(x.perimeter)
    #for ele in x:
    #    print(ele.size())
#a= array([[1,2,3],[4,5,6],[7,8,9]])
#print(a[:,1])