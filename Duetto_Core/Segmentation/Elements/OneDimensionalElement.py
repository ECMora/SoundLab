from Duetto_Core.Segmentation import Segment
from Duetto_Core.Segmentation.Elements.Element import Element


class OneDimensionalElement(Element):
    """
    Represents the minimal piece of information to clasify
    An element is a time and spectral region of the signal that contains a superior energy that the fragment of signal
    near to it
    """
    def __init__(self, signal, indexFrom, indexTo):
        super(self, signal, indexFrom, indexTo)

    def __len__(self):
        """
        returns the len in ms of an element (float)
        """
        return (self.indexTo-self.indexFrom)*1000.0/self.signal.samplingRate

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
        if (self.initColumn+len(perimeter)+ len(other_perimeter)+ n >=len(self.bins)):
            raise Exception("Could Not merge. To large element for this especgram")
        for i in range(n):
            perimeter.append((last[0]+i*(first[0]-last[0])/n,last[1] + i*(first[1]-last[1])/n))

        perimeter.extend(other_perimeter)
        self.perimeter = perimeter

