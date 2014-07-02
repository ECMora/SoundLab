# -*- coding: utf-8 -*-
class ElementsDetector:
    """
    Base class for the detection hierarchy. Parent of the one
    and two dimension's elements detectors
    """

    def __init__(self):
        self.elements = []

    def detect(self, signal):
        """
        The method that detect the elements in the signal and storages into the corresponding list
        """
        pass

    def elementCount(self):
        return len(self.elements)

    def mergeIntervals(self, elements_array, distancefactor=50):
        """
        Merge into one interval two elements with no more than  distance factor distance between them
        """
        b = []
        if(elements_array is None or len(elements_array) == 0):
            return b

        current = elements_array[0]
        for tuple in elements_array[1:]:
            if (tuple[0]-current[1])*100.0/(tuple[1]-current[0]) < distancefactor:
                current = (current[0], tuple[1])

            else:
                b.append(current)
                current=tuple
        b.append(current)
        return b





