class Detector:

    def __init__(self):
        self.pointer2D = []
        self.oneDimensionalElements = []
        self.twodimensionalElements = []

    def detect(self, signal):
        """
        The method that detect the elements in the signal and storages into the corresponding list
        """
        pass

    def elementCount(self):
        return len(self.pointer2D)+len(self.oneDimensionalElements)+len(self.twodimensionalElements)

    def elements(self):
        for c in self.oneDimensionalElements:
            yield c
        for c in self.pointer2D:
            yield c
        for c in self.twodimensionalElements:
            yield c

