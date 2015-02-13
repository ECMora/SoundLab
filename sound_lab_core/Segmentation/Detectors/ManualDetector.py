from sound_lab_core.Segmentation.Detectors.OneDimensional.OneDimensionalElementsDetector import \
    OneDimensionalElementsDetector


class ManualDetector(OneDimensionalElementsDetector):

    def __init__(self, signal=None):
        OneDimensionalElementsDetector.__init__(self, signal)

    def detect(self, indexFrom=0, indexTo=-1):

        return []