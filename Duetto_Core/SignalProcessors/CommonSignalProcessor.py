from math import sin, pi

from numpy import array, zeros, concatenate

from Duetto_Core.SignalProcessors.SignalProcessor import SignalProcessor


class CommonSignalProcessor(SignalProcessor):
    mean = None

    def __init__(self, signal=None):
        SignalProcessor.__init__(self, signal)

    def setSilence(self, indexFrom=0, indexTo=-1):
        """
        Clear the signal in the specified interval.
        indexFrom indexTo  the indexes for the interval.
        indexFrom is the beginning and  indexTo is the end of the interval
        by default are indexFrom=0, indexTo=-1
        """
        if indexTo == -1:
            indexTo = len(self.signal.data)
        self.checkIndexes(indexFrom, indexTo)
        self.signal.data[indexFrom:indexTo] = 0
        return self.signal

    def reverse(self, indexFrom, indexTo=-1):
        """
        reverse the signal in the interval [indexFrom,indexTo]
         Example:
         data=[1,2,3,4,5]
         reverse data
         data=[5,4,3,2,1]
        """
        if indexTo == -1:
            indexTo = len(self.signal.data)
        self.checkIndexes(indexFrom, indexTo)
        data = self.signal.data[indexFrom:indexTo]
        self.signal.data[indexFrom:indexTo] = data[::-1]
        return self.signal

    def absoluteValue(self, indexFrom, indexTo=-1,sign=1):
        """
         the negatives(positives) values of the signal in the interval [indexFrom,indexTo] are eliminated
         Example:
         data=[1,-22,3,-4,5]
         result data
         data=[5,0,3,0,1]
        """
        if indexTo == -1:
            indexTo = len(self.signal.data)
        self.checkIndexes(indexFrom, indexTo)
        for i in range(indexFrom,indexTo):
            self.signal.data[i] = self.signal.data[i] if (self.signal.data[i] > 0 and sign > 0) or (self.signal.data[i] < 0 and sign < 0) else 0
        return self.signal

    def changeSign(self, indexFrom, indexTo=-1):
        """
         change the sign of the  values of the signal in the interval [indexFrom,indexTo]
         Example:
         data=[1,-22,3,-4,5]
         data=[-1,22,-3,4,-5]
        """
        if indexTo == -1:
            indexTo = len(self.signal.data)
        self.checkIndexes(indexFrom, indexTo)
        self.signal.data[indexFrom:indexTo] = -self.signal.data[indexFrom:indexTo]
        return self.signal


    def insertSilence(self, indexFrom=0, indexTo=-1, ms=0):
        arr = zeros(ms * self.signal.samplingRate / 1000.0, type(self.signal.data[0]))
        self.signal.data = concatenate((self.signal.data[0:indexFrom],
                                        arr,
                                        self.signal.data[indexFrom:]))
        return self.signal

    def scale(self, indexFrom=0, indexTo=-1, factor=100, function="normalize", fade="IN"):
        n = indexTo - indexFrom if indexTo != -1 else len(self.signal.data) - indexFrom

        def f(index):
            if(function=="Linear"):
                 if(fade=="OUT"):
                     return 1-(index*1.0)/n
                 elif(fade=="IN"):
                     return (index*1.0)/n
            elif(function=="sin"):
                 if(fade=="OUT"):
                     return sin((index*1.0*pi)/(n*2)+pi/2)
                 elif(fade=="IN"):
                     return sin((index*1.0*pi)/(n*2))
            elif(function=="sin-sqrt"):
                 if(fade=="OUT"):
                     return (sin((index*1.0*pi)/(n*2)+pi/2))**0.5
                 elif(fade=="IN"):
                     return (sin((index*1.0*pi)/(n*2)))**0.5
            elif(function=="sin^2"):
                if(fade=="OUT"):
                    return (sin((index*1.0*pi)/(n*2)+pi/2))**2
                elif(fade=="IN"):
                    return (sin((index*1.0*pi)/(n*2)))**2
            elif(function=="cuadratic"):
                if(fade=="IN"):
                    return (index*1.0/n)**2
                elif(fade=="OUT"):
                    return (1-(index*1.0)/n)**2
        if function == "const":
            factor = 10.0**(factor/20.0)
            self.signal.data[indexFrom:indexTo] *= factor
        elif function == "normalize":
            factor /= 100.0
            self.signal.data[indexFrom:indexTo] *= factor
        else:
            self.signal.data[indexFrom:indexTo] = [self.signal.data[indexFrom + index] * f(index) for index in range(n)]
        return self.signal
