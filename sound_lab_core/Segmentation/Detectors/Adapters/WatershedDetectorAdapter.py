# -*- coding: utf-8 -*-
from sound_lab_core.Segmentation.Detectors.OneDimensional.Image.WaterShedDetector import \
    WatershedDetector
from sound_lab_core.SoundLabAdapter import SoundLabAdapter
from pyqtgraph.parametertree import Parameter


class WatershedDetectorAdapter(SoundLabAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self, parent):
        SoundLabAdapter.__init__(self, parent)

        settings = [
            {u'name': unicode(self.tr(u'Min Size (ms)')), u'type': u'float', u'value': 2.00, u'step': 1, u'limits': (0, 30000)},
            {u'name': unicode(self.tr(u'Min Size (kHz)')), u'type': u'float', u'value': 2.00, u'step': 1, u'limits': (0, 30000)}]
        self.min_size_ms = 2
        self.min_size_kHz = 2
        self.settings = Parameter.create(name=u'Settings', type=u'group', children=settings)

        self.settings.sigTreeStateChanged.connect(self.apply_settings_change)

    def get_settings(self):
        """
        returns a Parameter Tree with the options of the abs decay detector
        """
        return self.settings

    def get_instance(self):
        """
        Gets a new get_instance of the corresponding parameter measurement.
        :return: A new get_instance of the corresponding parameter measurement class
        """
        min_size_ms = 2
        min_size_kHz = 2
        try:
            min_size_ms = self.settings.param(unicode(self.tr(u'Min Size (ms)'))).value()
            min_size_kHz = self.settings.param(unicode(self.tr(u'Min Size (kHz)'))).value()

        except Exception as e:
            min_size_ms = 2
            min_size_kHz = 2

        self.min_size_ms = min_size_ms
        self.min_size_kHz = min_size_kHz

        return WatershedDetector(None, self.min_size_ms, self.min_size_kHz)

    def apply_settings_change(self,parameter, changes):
        print(changes)