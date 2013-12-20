from Duetto_Core import SpecgramSettings
from Segment import Segment
class Element:
    """
    Represents the minimal piece of information to clasify
    An element is a time and spectral region of the signal that contains a superior energy that the fragment of signal
    near to it
    """
    def __init__(self, Pxx, bins, frecs, specgramsettings, perimeter,column):
        self.Pxx=Pxx  # the spectrogram at wich the elements belongs
        self.bins=bins  # the middle point in samples of every col in the Pxx
        self.frecs=frecs  # the frecs of the Pxx
        self.specgramSettings=specgramsettings
        self.initColumn =column  # the column of Pxx when the element begin
        self.perimeter = perimeter  # border of the spectrogram region its an array of tuple col*fragment col*(init,end)

    def segment(self):
        return Segment([self])

    def __len__(self):
        """
        returns the len in ms of an element
        """
        return 0

    def merge(self, other_element):
        """
        Merge self and the other_element in one single element. Modify the current element
        """
        pass

