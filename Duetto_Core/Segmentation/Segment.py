# -*- coding: utf-8 -*-
from Duetto_Core.Segmentation.Elements.Element import Element


class Segment:
    """
    The Segment is a  non empty set of elements.
     Is the smallest piece of classification
    """
    def __init__(self, elements=[]):

        """
        @param elements: the elements that  belong to the  segment
        @raise TypeError:
        """
        for el in elements:
            if not isinstance(el,Element):
                raise TypeError(u"The object has unfamiliar "+unicode(type(el))+u" were Element are expected")
        self.elements = elements

    @staticmethod
    def groupByTrainAnalysis(elements):
        return Segment(elements=elements)

