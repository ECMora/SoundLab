from Duetto_Core.Segmentation import Segment


class Element:
    """
    Represents the minimal piece of information to clasify
    An element in an N dimensional transform of the signal is an N dimensional region
    that contains a superior energy that the fragment of signal near to it.
    Ej of 1 dimensional Transform : scale, normalize, oscilogram
    Ej of 2 dimensional Transform : spectrogram
    """
    def __init__(self, signal, indexFrom, indexTo):
        #the signal in wich this elements is defined
        self.signal=signal
        #the temporal interval in the signal in wich is located this element
        self.indexFrom=indexFrom
        self.indexTo=indexTo
        #the optional data interesting for the transform ej name, parameters, etc
        self.transformData = {"name": "", "transformDimension": 0}

    def segment(self):
        """
        The segment that only contains this element
        """
        return Segment([self])

    def __len__(self):
        """
        returns the len in ms of an element (float)
        """
        raise NotImplemented()

    def merge(self, other_element):
        raise NotImplemented()
