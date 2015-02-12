# -*- coding: utf-8 -*-
from sound_lab_core.Segmentation.Detectors.ManualDetector import ManualDetector
from sound_lab_core.SoundLabAdapter import SoundLabAdapter
from pyqtgraph.parametertree import Parameter


class ManualDetectorAdapter(SoundLabAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self, parent):
        SoundLabAdapter.__init__(self, parent)

        self.settings = Parameter.create(name=u'Settings', type=u'group')

    @property
    def instance(self):
        return ManualDetector()

    def get_settings(self):
        """
        :type parameter:
        """
        return ["manual seg"]

    def apply_settings_change(self, transform, change):
        pass