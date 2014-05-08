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

    def mergeIntervals(self, a, distancefactor=50):
        """
        Merge into one interval two oneDimensionalElements with no more than  distance factor distance between them
        """
        b = []
        if(a is None or len(a) == 0):
            return b

        current = a[0]
        for tuple in a[1:]:
            if (tuple[0]-current[1]) < distancefactor:
                current = (current[0], tuple[1])
            else:
                b.append(current)
                current=tuple
        b.append(current)
        return b
