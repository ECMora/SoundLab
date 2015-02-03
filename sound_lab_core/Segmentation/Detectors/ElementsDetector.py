# -*- coding: utf-8 -*-
class ElementsDetector:
    """
    Base class for the detection hierarchy. Parent of the one
    and two dimension's elements detectors
    """

    def __init__(self, signal):
        self.elements = []
        self.signal = signal

    def detect(self):
        """
        The method that detect the elements in the signal and storages into the corresponding list
        """
        pass

    def elementCount(self):
        return len(self.elements)





