from sound_lab_core.Segmentation.Detectors.OneDimensional.OneDimensionalElementsDetector import \
    OneDimensionalElementsDetector


class ManualDetector(OneDimensionalElementsDetector):
    """
    Implementation of manually segmentation
    """

    def __init__(self, signal=None):
        OneDimensionalElementsDetector.__init__(self, signal)