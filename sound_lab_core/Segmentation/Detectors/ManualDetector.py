from math import pi, sin
import matplotlib.mlab as mlab
from numpy import zeros, array, int32, mean
from sound_lab_core.Segmentation.Detectors.OneDimensional.OneDimensionalElementsDetector import \
    OneDimensionalElementsDetector
from Utils.Utils import fromdB
from sound_lab_core.Segmentation.Elements.OneDimensionalElements.OscilogramElement import OscilogramElement


class ManualDetector(OneDimensionalElementsDetector):

    def __init__(self, signal=None):
        OneDimensionalElementsDetector.__init__(self, signal)

    def detect(self, indexFrom=0, indexTo=-1):

        return []