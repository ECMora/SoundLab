from Duetto_Core.Segmentation.Detectors.Detector import Detector


class ElementsDetector(Detector):
    def __init__(self):
        Detector.__init__(self)
        self.NOISE_MERGE_FACTOR=1/50.0
        self.MIN_INTERVAL=1



