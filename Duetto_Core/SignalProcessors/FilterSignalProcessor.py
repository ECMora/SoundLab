from math import *
from numpy import real,concatenate, array
from numpy.fft import *
from Duetto_Core.SignalProcessors.SignalProcessor import SignalProcessor

class FILTER_TYPE():
    BAND_PASS,BAND_STOP,LOW_PASS,HIGH_PASS=range(4)


class FilterSignalProcessor(SignalProcessor):

    def __init__(self,signal=None):
        SignalProcessor.__init__(self,signal)

    def movingAverageFilter(self,numberOfPoints=10,indexFrom=0,indexTo=-1):
        """
        executes a moving average filter of size numberOfPoints in the signal
                """
        if(indexTo==-1):
            indexTo=len(self.signal.data)-numberOfPoints
        for i in range(indexFrom,indexTo):
            self.signal.data[i] = sum(self.signal.data[i:i+numberOfPoints])*1./numberOfPoints
        return self.signal


    def filter(self,indexFrom=0,indexTo=-1,filterType=FILTER_TYPE().LOW_PASS,Fc=0,Fl=0,Fu=0):
        indexFrom=int(indexFrom)
        indexTo=int(indexTo)
        if(indexTo==-1):
            indexTo=len(self.signal.data)

        #self.signal.data[indexFrom:indexTo]=convolve(self.signal.data[indexFrom:indexTo],[0,0,0,0,0,0,1,0,0,0])
        n = int(ceil(log(indexTo-indexFrom,2)))

        data_frec=fft(self.signal.data[indexFrom:indexTo],2**n)
        n=2**n
        indexFrecuency=(n*1.0)/self.signal.samplingRate
        Fl,Fu=int(round(Fl*indexFrecuency)),int(round(Fu*indexFrecuency))
        Fc=int(Fc*indexFrecuency)
        size = len(data_frec)

        if(filterType==FILTER_TYPE().BAND_PASS):
            data_frec[Fu:size-Fu+1]=complex(0,0)
            data_frec[:Fl+1]=complex(0,0)
            data_frec[-Fl:]=complex(0,0)


        elif(filterType==FILTER_TYPE().BAND_STOP):
            data_frec[Fl:Fu+1]=complex(0,0)
            data_frec[-Fu:size-Fl+1]=complex(0,0)

        elif(filterType==FILTER_TYPE().HIGH_PASS):
            if(Fc<n/2):
                data_frec[:Fc]=complex(0,0)
                data_frec[-Fc:]=complex(0,0)
            elif(Fc==n/2):
                data_frec[:]=complex(0,0)

        elif(filterType==FILTER_TYPE().LOW_PASS):
            if(Fc != 0 and Fc < n / 2):
                data_frec[Fc:size-Fc+1]=complex(0,0)
            elif(Fc == 0):
                data_frec[:]=complex(0,0)

        if(indexFrom==0 and indexTo==len(self.signal.data)):
             self.signal.data=array(real(ifft(data_frec)[0:indexTo-indexFrom]),self.signal.data.dtype)
        else:
            self.signal.data=concatenate((self.signal.data[0:indexFrom],array(real(ifft(data_frec)[0:indexTo-indexFrom]),self.signal.data.dtype),self.signal.data[indexTo:]))



