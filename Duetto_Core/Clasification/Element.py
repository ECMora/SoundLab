from Duetto_Core import SpecgramSettings
from Segment import Segment
class Element:
    """
    Represents the minimal piece of information to clasify
    An element is a time and spectral region of the signal that contains a superior energy that the fragment of signal
    near to it
    """
    def __init__(self,signal, indexFrom, indexTo , Pxx, bins, frecs, specgramsettings, perimeter,column):
        self.signal=signal
        self.indexFrom=indexFrom
        self.indexTo=indexTo
        self.Pxx=Pxx  # the spectrogram at wich the elements belongs
        self.bins=bins  # the middle point in samples of every col in the Pxx
        self.frecs=frecs  # the frecs of the Pxx
        self.specgramSettings=specgramsettings
        self.initColumn =column  # the column of Pxx when the element begin
        self.perimeter = perimeter  # border of the spectrogram region its an array of tuple col*fragment col*(init,end)
        if(len(perimeter)>=len(bins)):
            raise Exception()

    def segment(self):
        return Segment([self])

    def size(self):
        """
        returns the len in ms of an element
        """
        samples = (self.bins[self.initColumn+len(self.perimeter)]-self.bins[self.initColumn]) if self.initColumn < len(self.bins)-1 else self.bins[1]-self.bins[0]
        return samples*1000/self.signal.samplingRate  #ms


    def merge(self, other_element):
        """
        Merge self and the other_element in one single element. Modify the current element

        """

        last = self.perimeter[-1]
        first = other_element.perimeter[0]
        n = other_element.initColumn - self.initColumn - len(self.perimeter)
        perimeter = self.perimeter
        other_perimeter = other_element.perimeter


        if(other_element.initColumn < self.initColumn):
            # the other first
            last = other_element.perimeter[-1]
            first = self.perimeter[0]
            n = self.initColumn-other_element.initColumn-len(other_element.perimeter)
            perimeter = other_element.perimeter
            other_perimeter = self.perimeter

        #an element just could have one interval per column in the Pxx
        if(self.initColumn+len(perimeter)+ len(other_perimeter)+ n >=len(self.bins)):
            raise Exception("Could Not merge. To large element for this especgram")
        for i in range(n):
            perimeter.append((last[0]+i*(first[0]-last[0])/n,last[1] + i*(first[1]-last[1])/n))

        perimeter.extend(other_perimeter)
        self.perimeter = perimeter
