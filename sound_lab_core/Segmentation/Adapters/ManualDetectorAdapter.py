# -*- coding: utf-8 -*-
from sound_lab_core.Segmentation.OneDimensional.ManualDetector import ManualDetector
from sound_lab_core.SoundLabAdapter import SoundLabAdapter


class ManualDetectorAdapter(SoundLabAdapter):
    """
    Adapter class for the manual detector.
    """

    def __init__(self):
        SoundLabAdapter.__init__(self)

        self.name = u'Manual'

    def get_instance(self, signal):
        return ManualDetector(signal)