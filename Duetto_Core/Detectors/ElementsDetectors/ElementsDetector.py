from Duetto_Core.Detectors.Detector import Detector


class ElementsDetector(Detector):
    def __init__(self):
        Detector.__init__(self)
        self.NOISE_MERGE_FACTOR=1/50.0
        self.MIN_INTERVAL=1

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

