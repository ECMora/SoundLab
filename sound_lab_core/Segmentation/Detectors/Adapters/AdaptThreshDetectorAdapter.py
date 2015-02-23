# -*- coding: utf-8 -*-
from sound_lab_core.Segmentation.Detectors.Adapters.ImageDetectorAdapter import ImageDetectorAdapter
from sound_lab_core.Segmentation.Detectors.OneDimensional.Image.AdaptThreshDetector import \
    AdaptThreshDetector

class AdaptThreshDetectorAdapter(ImageDetectorAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self):
        ImageDetectorAdapter.__init__(self)

    def get_instance(self,signal):
        """
        Gets a new get_instance of the corresponding parameter measurement.
        :return: A new get_instance of the corresponding parameter measurement class
        """
        self.update_instance_variables()
        return AdaptThreshDetector(signal, self.min_size_ms, self.min_size_kHz)
