from Duetto_Core.Segmentation.Elements import Element


class Segment:
    """
    Defines a group of elements for their classification
    The Segment is a group of elements or/and a list of segments
    """
    def __init__(self, elements=[], segments=[]):
        for el in elements:
            if type(el) is not Element:
                raise TypeError()
        for s in segments:
            if type(s) is not Segment:
                raise TypeError()
        self.elements = elements
        self.segments = segments