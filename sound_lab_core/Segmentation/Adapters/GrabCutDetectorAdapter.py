# -*- coding: utf-8 -*-
from sound_lab_core.Segmentation.Adapters.ImageDetectorAdapter import ImageDetectorAdapter
from sound_lab_core.Segmentation.OneDimensional.Image.GrabCutDetector import GrabCutDetector


class GrabCutDetectorAdapter(ImageDetectorAdapter):
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

        return GrabCutDetector(signal, self.min_size_ms, self.min_size_kHz)
